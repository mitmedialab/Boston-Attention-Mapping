################################################################################
# Adds new BG articles from API to DB
# Does geoprocessing on data
################################################################################

import boston_globe
from Geoprocessor import Geoprocessor
from DBManager import DBManager
import argparse,os,sys


parser = argparse.ArgumentParser()
parser.add_argument("-d","--delete", action="store_true", default=False, help="delete the existing database and download all new data from the API")
args = parser.parse_args()

if(args.delete):
	print 'You have specified delete so I will delete and re-create the database'

#Connect to Couch
conn = DBManager();

#delete DB if it exists
if (args.delete) :
	try:
		conn.deleteDB()
		db = conn.createDB()
		conn.saveAllViews()
	except couchdb.http.ResourceNotFound:
	   	print "Database doesn't exist. We'll go ahead and create it."
	   	db = conn.createDB()
	   	conn.saveAllViews()
else:
	db = conn.db

latestArticles = boston_globe.fetchLatestArticlesFromAPI(conn)

geoprocessor = Geoprocessor()
cleanArticles = geoprocessor.filterAndCleanArticles(latestArticles, conn)

conn.saveAll(cleanArticles)


print "Done adding articles from the API"