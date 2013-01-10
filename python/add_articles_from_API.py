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

db_metadata = {}
db_metadata["type"] = "metadata"

#Connect to Couch
conn = DBManager();

if (args.delete) :
	#delete DB if it exists
	try:
		conn.deleteDB()
		db = conn.createDB()
	except couchdb.http.ResourceNotFound:
	   	print "Database doesn't exist. We'll go ahead and create it."
	   	db = conn.createDB()

latestArticles = boston_globe.fetchLatestArticlesFromAPI(db)

db_metadata["total_articles_available"] = len(latestArticles)

geoprocessor = Geoprocessor()
articlesAndMetadata = geoprocessor.filterAndCleanArticles(latestArticles, db_metadata)
cleanArticles = articlesAndMetadata[0]
db_metadata = articlesAndMetadata[1]

conn.saveAll(cleanArticles, db_metadata)
conn.saveAllViews()

print "Done - Yay"