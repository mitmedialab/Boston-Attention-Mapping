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

    self.loadMetadata()

    print "Connected to CouchDB at " + serverURL + " and loaded DB metadata"

  #Will throw ResourceNotFound if DB doesn't exist
  def deleteDB(self):
    del self.server[self.config.get('db','db_name')]
    self.db = None

  def createDB(self):
    self.db = self.server.create(self.config.get('db','db_name'))
    return self.db

  #Saves all articles to DB
  def saveAll(self, articleList):
    # iterate through articles
    # save each to DB
    for article in articleList:
      self.db.save(article)
    self.db.save(self.db_metadata)
    print "Saved all data and metadata"

  def saveAllViews(self):
    self.db.save(globe_views.getAllGlobeViews())
    self.db.save(globe_views.getNLTKViews())

  #TODO - turn this into a file that then gets deleted after being run once
  def saveNewViews(self):
    newViews = globe_views.getNewViews()
    if newViews != "":
      self.db.save(newViews)

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

  def getMetadata(self):
    return self.db_metadata

  def loadMetadata(self):
    self.db_metadata = ""
    md = self.db.view('globe/metadata')  
    for row in md:       
        self.db_metadata = row['value']
    if(self.db_metadata ==""):
      self.db_metadata = {}
      self.db_metadata["type"] = "metadata"
      self.db_metadata["filtered_articles_no_geodata"] = 0
      self.db_metadata["filtered_articles_bad_geodata"] =0
      self.db_metadata["total_articles_added"] = 0
      self.db_metadata["number_of_updated_MA_city_names"] =0

  def documentExists(self, id):
    doc = self.db.get(id)
    if (doc == None):
      return False
    else:
      return True

