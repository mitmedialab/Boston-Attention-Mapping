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
import couch_connect

class WordFreqencyJob:

  def __init__(self):
    conn = couch_connect.CouchConnect()
    self.db = conn.db
    self.articles = []
    self.city_word_incidence = {}
    self.cities = {}
    self.tokenizer = nltk.WordPunctTokenizer()#nltk.RegexpTokenizer("[\w]", flags=re.UNICODE)
    self.process_articles()
    self.calculate_results()

  # fetch cities which have more than one article
  def fetch_article_keys(self):
    city_tuples = [(a.key, a.value) for a in self.db.view("nltk/cities_or_neighborhoods", group=True)]
    cities = [city for city in sorted(city_tuples, key=lambda city:city[1], reverse=True) if city[1] > 1 ]
    return cities

  def proces_city_articles(self, nltk_text_list):
    self.articles.extend(nltk_text_list)
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
    stopwords = nltk.corpus.stopwords.words('english')
    contains_letter = re.compile('[a-z]')
    for city in self.fetch_article_keys():
      articles = self.proces_city_articles([ nltk.Text([token.lower() 
                                                      for token in self.tokenizer.tokenize(a.value[0]) 
                                                      if(len(token) > 1 and 
                                                         token.lower() not in stopwords and
                                                         contains_letter.search(token))]) 
                                            for a in self.db.view("nltk/fulltext_by_city_or_neighborhood", key=city[0]) 
                                            if len(a.value) > 0 ])

      vocab = articles.vocab().items()
      [self.add_city_word_incidence(fd[0]) for fd in vocab]
      freq = [(fd[0], float(fd[1])/float(vocab[0][1])) for fd in vocab]

      self.cities[city[0]] = {"type": "place_frequency",
                           "city_or_neighborhood": city[0],
                           "articles": city[1],
                           "date": time.ctime(),
                           "wordcount": sum([len(text) for text in articles]),
                           "freqdist": freq}

    

w = WordFreqencyJob()
