#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
# USES NLTK TO ADD WORD FREQUENCY DATA ABOUT ARTICLES BY CITY OR NEIGHBORHOOD TO COUCHDB
################################################################################

import couchdb
import nltk
from nltk import Text
from nltk import TextCollection
import math
import re
import time
import string
import sys
import datetime
from datetime import datetime
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import timeit
#import couch_connect


class WordFreqencyJob:

    def __init__(self):
        #self.conn = couchdb.Server('')
        #self.db = self.conn['']
        #conn = couch_connect.CouchConnect()
        #self.db = conn.db
        self.conn = couchdb.Server('http://66.228.45.37:5984')
        self.db = self.conn['boston-globe-articles']
        self.articles = []
        self.city_word_incidence = {}
        self.cities = {}
        self.tokenizer = nltk.WordPunctTokenizer()#nltk.RegexpTokenizer("[\w]", flags=re.UNICODE)
        self.stopwords = self.getStopWordList('stop-words-english4.txt')
        #https://gist.github.com/alexbowe/
        self.sentence_re = r'''(?x)
              ([A-Z])(\.[A-Z])+\.?
            | \w+(-\w+)*
            | \$?\d+(\.\d+)?%?
            | \.\.\.
            | [][.,;"'?():-_`]
        '''
        # Grammar from this paper http://lexitron.nectec.or.th/public/COLING-2010_Beijing_China/PAPERS/pdf/PAPERS065.pdf
        self.grammar = r"""
            NBAR:
                {<NN.*|JJ>*<NN.*>}  #

            NP:
                {<NBAR>}
                {<NBAR><IN><NBAR>}
        """
        self.chunker = nltk.RegexpParser(self.grammar)
        self.toks = ""
        self.postoks = ""
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.tree = ""
        #self.print_cities()
        self.getTimeStamp("start:")
        self.process_articles()
        self.calculate_results()
        self.getTimeStamp("end:")
        self.db.view("nltk/place_frequency", limit=1)

    def leaves(self,tree):
        #NP leaf node of tree
        for childtree in tree.subtrees(filter = lambda t: t.node=='NP'):
            yield childtree.leaves()

    def lemmatize_word(self,word):
        # this results in unsusual words, thistl instead of thistle
        #word = self.stemmer.stem_word(word)
        word = re.sub('cq ', ' ', word.lower())
        word = self.lemmatizer.lemmatize(word)
        return word

    def filterStopWords(self,word):
        blnIncludeWord = bool( len(word) > 1
            and word.lower().decode('utf-8') not in self.stopwords)
        return blnIncludeWord

    def get_terms(self):
        for leaf in self.leaves(self.tree):
            term = [ self.lemmatize_word(w) for w,t in leaf if self.filterStopWords(w)]
            yield term

    #this will generate a noune phrase term string
    def get_str_entities(self,txtPassString):
        self.toks = nltk.regexp_tokenize(txtPassString, self.sentence_re)
        self.postoks = nltk.tag.pos_tag(self.toks)
        self.tree = self.chunker.parse(self.postoks)
        strTermsString = ""
        arrayterms = self.get_terms()
        for singlearray in arrayterms:
            for oneterm in xrange(len(singlearray)):
                strTermsString = strTermsString + " " + re.sub('cq$', '', re.sub('[-,.?!\t\n\_\%\$ ]+', '', singlearray[oneterm]))
        #print strTermsString
        return strTermsString

    #to track the history of the run
    def getTimeStamp(self, inputstartend):
        FORMAT = '%Y-%m-%d %H:%M:%S'
        data = "\n" + inputstartend + ' ' + datetime.now().strftime(FORMAT)
        with open("trackhistoryfile.txt", "a") as trackfile:
            trackfile.write(data)

    #get the cities
    def fetch_article_keys(self):
        city_tuples = [(a.key, a.value) for a in self.db.view("nltk/cities_or_neighborhoods", group=True)]
        cities = [city for city in sorted(city_tuples, key=lambda city:city[1], reverse=True) if city[1] > 1 ]
        return cities

    #print cities Example: (u'Talladega', 4)
    def print_cities(self):
        for city in self.fetch_article_keys():
            print city

    def process_city_articles(self, nltk_text_list):
        self.articles.extend(nltk_text_list)
        # takes in multiple texts = nltk.TextCollection([t1, t2, t3])
        #print "@nltk.TextCollection(nltk_text_list):"
        return nltk.TextCollection(nltk_text_list)

    # inverse collection frequency
    def term_icf(self, term):
        if term not in self.city_word_incidence:
          return 0
        return math.log(len(self.cities) / self.city_word_incidence[term])

    # return the term frequency * inverse collection frequency for all terms in a city
    def tf_icf(self, city):
        return sorted([(tf[0], tf[1]*self.term_icf(tf[0])) for tf in self.cities[city]["freqdist"]], key=lambda term: term[1], reverse=True)

    def calculate_results(self):
        vocab = nltk.TextCollection(self.articles).vocab().items()
        overall_freqdist = [(fd[0], float(fd[1])/float(vocab[0][1])) for fd in vocab]
        for city in self.cities:
          self.cities[city]["freqdist"] =  self.tf_icf(city)[0:100]
          self.db.save(self.cities[city])

    def add_city_word_incidence(self, word):
        if word in self.city_word_incidence:
          self.city_word_incidence[word] += 1
        else:
          self.city_word_incidence[word] = 1
        return word

    def process_articles(self):
        count = 0
        for city in self.fetch_article_keys():
                    print city[0]
                    articles = self.process_city_articles([ nltk.Text([token
                                                              for token in self.tokenizer.tokenize(self.get_str_entities(a.value[0]))
                                                              ])
                                                    for a in self.db.view("nltk/fulltext_by_city_or_neighborhood", key=city[0])
                                                    if a.value != None and len(a.value) > 0 ])
                    count = count + 1
                    vocab = articles.vocab().items()
                    [self.add_city_word_incidence(fd[0]) for fd in vocab]
                    freq = [(fd[0], float(fd[1])/float(vocab[0][1])) for fd in vocab]
                    self.cities[city[0]] = {"type": "place_frequency",
                                               "city_or_neighborhood": city[0],
                                               "articles": city[1],
                                               "date": time.ctime(),
                                               "wordcount": sum([len(text) for text in articles]),
                                               "freqdist": freq}
        print "process_articles finished %s" % count
        self.getTimeStamp("process_articles finished:[" + str(count) + "]")

    def getStopWordList(self,stopWordListFileName):
        #read the stopwords file and build a list
        stopWords = []
        stopWords.append('Boston.com')
        stopWords.append('Your Town')
        stopWords.append('Boston Globe')
        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word.decode('utf-8'))
            line = fp.readline()
        fp.close()
        if stopWords:
            stopWords.sort()
            last = stopWords[-1]
            for i in range(len(stopWords)-2, -1, -1):
                if last == stopWords[i]:
                    del stopWords[i]
                else:
                    last = stopWords[i]
        return stopWords

    def getStopWords(self):
        return self.stopwords

w = WordFreqencyJob()
