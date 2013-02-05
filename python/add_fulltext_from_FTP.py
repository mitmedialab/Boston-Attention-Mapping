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
newFile = config_file = open('urls.txt', 'w')
matches = 0
missingURL = 0
noMatches = 0
for infile in listing:
    docs +=1
    try:
        xml = etree.parse(docDir + infile)
    except lxml.etree.XMLSyntaxError:
        print "Couldn't parse document: " + infile
        errors += 1
    urls = xml.findall("//CanonicalUrl")
    if len(urls) == 0:
        missingURL += 1

    for url in urls:
        if (url != None and url.text != None):
            url = url.text
            if (url == "http://www.bostonglobe.com/metro/regionals/south/2011/11/13/some-voice-concerns-and-hope-over-new-congressional-map/rt5rrSX64xjWO53YjM078J/story.html"):
                print "found the edited one"                
                import pdb; pdb.set_trace()
            newFile.write(url + "\n")
            try:
                doc = conn.documentByURL(url)
                if (doc != None):
                    matches += 1
                else:
                    noMatches += 1
            except couchdb.http.ResourceNotFound:
                noMatches += 1

newFile.close()
print str(docs) + " total docs"
print str(errors) + " Parse Errors"
print str(missingURL) + " docs have no canonical url"
print str(matches) + " matches"
print str(noMatches) + " not matches"

