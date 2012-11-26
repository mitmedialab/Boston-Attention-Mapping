################################################################################
# CONVENIENCE WRAPPER FOR CONNECTING TO COUCHDB
################################################################################

import couchdb,os
import ConfigParser

class CouchConnect:
  
  APP_ROOT_DIR=os.path.dirname(os.path.dirname( os.path.abspath(__file__) ) )+ "/"

  def __init__(self):
   

    self.config = ConfigParser.ConfigParser()
    self.config.read(self.APP_ROOT_DIR + 'python/globe.config')
    self.connect()
    
  
  def connect(self):
    serverURL = self.config.get('db','host') + ':' + self.config.get('db','port')
    

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


    
    self.db = self.server[self.config.get('db','db_name')]   
    print "Connected to CouchDB at " + serverURL

  #Will throw ResourceNotFound if DB doesn't exist
  def deleteDB(self):
    del self.server[self.config.get('db','db_name')]
    self.db = None

  def createDB(self):
    self.db = self.server.create(self.config.get('db','db_name'))
    return self.db
