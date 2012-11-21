import couchdb
import nltk
from nltk import Text
from nltk import TextCollection
import math
import re
import time
import string

class ArticleProcessingJob:

  def __init__(self, database_name="boston-globe-articles"):
    self.server = couchdb.Server()
    self.db = self.server[database_name]  
    self.tokenizer = nltk.WordPunctTokenizer()#nltk.RegexpTokenizer("[\w]", flags=re.UNICODE)
    self.process_articles()

  # fetch cities which have more than one article
  def fetch_article_keys(self):
    city_tuples = [(a.key, a.value) for a in self.db.view("globe/cities", group=True)]
    cities = [city[0] for city in sorted(city_tuples, key=lambda city:city[1], reverse=True) if city[1] > 1 ]
    return cities

  def process_articles(self):
    stopwords = nltk.corpus.stopwords.words('english')
    for city in self.fetch_article_keys():
      self.articles = nltk.TextCollection([ nltk.Text([token.lower() 
                                                      for token in self.tokenizer.tokenize(a.value[0]) 
                                                      if(token.lower() not in stopwords and
                                                         token not in string.punctuation)]) 
                                            for a in self.db.view("globe/fulltext_by_city", key=city) 
                                            if len(a.value) > 0 ])
      freq = self.articles.vocab()
      city_frequency = {"type": "city_frequency",
                        "city": city,
                        "date": time.ctime(),
                        "words": freq.items()[0:50]}
      self.db.save(city_frequency)

a = ArticleProcessingJob()
