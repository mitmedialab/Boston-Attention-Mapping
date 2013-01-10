################################################################################
# CONVENIENCE WRAPPER FOR CONNECTING TO COUCHDB
################################################################################

import couchdb,os
import ConfigParser
import utils, globe_views

class DBManager:
  
  APP_ROOT_DIR=utils.getAppRootDir()

  def __init__(self):
   

    self.config = ConfigParser.ConfigParser()
    self.config.read(self.APP_ROOT_DIR + 'python/globe.config')
    self.connect()
    
  
  def connect(self):
    serverURL = self.config.get('db','host') + ':' + self.config.get('db','port')
    print serverURL

    if ((self.config.get('db','host') == 'localhost' or self.config.get('db','host') == '127.0.0.1') and self.config.get('db','port') == '5984' and len(self.config.get('db','user')) == 0 ):
      self.server = couchdb.Server() 
    else:
      try:  
        if (len(self.config.get('db','user')) > 0):
          self.server = couchdb.Server(url=serverURL) 
          self.server.resource.credentials = (self.config.get('db','user'), self.config.get('db','password'))
        else:
          self.server = couchdb.Server(url=serverURL) 
      except:
        print "error connecting to the couch server at " + serverURL + ' with credentials user = ' + self.config.get('db','user')
        print "exiting now"
        sys.exit()


    try:
      self.db = self.server[self.config.get('db','db_name')]   
    except:
      print "error selecting database " + self.config.get('db','db_name') + ". Is your CouchDB server running?"
    print "Connected to CouchDB at " + serverURL

  #Will throw ResourceNotFound if DB doesn't exist
  def deleteDB(self):
    del self.server[self.config.get('db','db_name')]
    self.db = None

  def createDB(self):
    self.db = self.server.create(self.config.get('db','db_name'))
    return self.db

  #Saves all articles to DB
  def saveAll(self, articleList, db_metadata):
    # iterate through articles
    # save each to DB
    for article in articleList:
      self.db.save(article)
    
    self.db.save(db_metadata)

  def saveAllViews(self):
    self.db.save(GlobeViews.getAllGlobeViews())
    self.db.save(GlobeViews.getNLTKViews())

  def saveAllFullText(self, articleList):
    # iterate through articles
    # save each to DB
    return self

  #matches fulltext to existing article record & saves with that record in DB
  def saveFullText(self, article):
    return self

  def getLastArticleDate(self):
    #return date
    return self

