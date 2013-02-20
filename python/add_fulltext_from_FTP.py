################################################################################
# Adds new fulltext articles to DB
# Matches articles to those that exist with metadata already in DB
################################################################################

import ConfigParser
import couchdb
import utils
import os
import lxml
from lxml import etree
from DBManager import DBManager

conn = DBManager()
APP_ROOT_DIR = utils.getAppRootDir()

config = ConfigParser.ConfigParser()
config.read(APP_ROOT_DIR + 'python/globe.config')

docDir = config.get('boston_globe', 'local_ftp_dir')

listing = os.listdir(docDir)
errors = 0
docs = 0
newFile = config_file = open('uuids.txt', 'w')
matches = 0
missingUUID = 0
noMatches = 0
for infile in listing:
    docs +=1
    try:
        xml = etree.parse(docDir + infile)
    except:
        print "Couldn't parse document: " + infile
        errors += 1
    uuids = xml.findall("//masterUUID")
    if len(uuids) == 0:
        missingUUID += 1

    for uuid in uuids:
        if (uuid != None and uuid.text != None):
            uuid = uuid.text
            date = xml.findall("//PublicationStartDate")
           
            
            if (date != None and len(date) > 0 and date[0] != None and date[0].text != None):
                newFile.write(uuid + "," + date[0].text + "\n")
                print "wrote " + uuid + "," + date[0].text
            else:
                newFile.write(uuid + "\n")
                print "wrote " + uuid
            '''try:
                doc = conn.documentByUUID(uuid)
                if (doc != None):
                    matches += 1
                else:
                    noMatches += 1
            except couchdb.http.ResourceNotFound:
                noMatches += 1
            '''
newFile.close()
print str(docs) + " total docs"
print str(errors) + " Parse Errors"
print str(missingUUID) + " docs have no UUID"
print str(matches) + " matches"
print str(noMatches) + " not matches"

