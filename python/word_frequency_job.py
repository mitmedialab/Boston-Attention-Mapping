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
    self.tokenizer = nltk.WordPunctTokenizer()#nltk.RegexpTokenizer("[\w]", flags=re.UNICODE)
    self.process_articles()

  # fetch cities which have more than one article
  def fetch_article_keys(self):
    city_tuples = [(a.key, a.value) for a in self.db.view("nltk/cities_or_neighborhoods", group=True)]
    cities = [city for city in sorted(city_tuples, key=lambda city:city[1], reverse=True) if city[1] > 1 ]
    return cities

  def process_articles(self):
    stopwords = nltk.corpus.stopwords.words('english')
    for city in self.fetch_article_keys():
      self.articles = nltk.TextCollection([ nltk.Text([token.lower() 
                                                      for token in self.tokenizer.tokenize(a.value[0]) 
                                                      if(token.lower() not in stopwords and
                                                         token not in string.punctuation)]) 
                                            for a in self.db.view("nltk/fulltext_by_city_or_neighborhood", key=city[0]) 
                                            if len(a.value) > 0 ])
      freq = self.articles.vocab()
      place_frequency = {"type": "place_frequency",
                        "city_or_neighborhood": city[0],
                        "articles": city[1],
                        "date": time.ctime(),
                        "words": freq.items()[0:50]}
      self.db.save(place_frequency)

w = WordFreqencyJob()
