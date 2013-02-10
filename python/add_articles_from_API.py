################################################################################
# Adds new BG articles from API to DB
# Does geoprocessing on data
################################################################################

import boston_globe
from Geoprocessor import Geoprocessor
from DBManager import DBManager
import argparse,os,sys
import utils
import ConfigParser
from datetime import date, timedelta
import couchdb

geoprocessor = Geoprocessor()
parser = argparse.ArgumentParser()
conn = DBManager()

#config file
APP_ROOT_DIR=utils.getAppRootDir()
config = ConfigParser.ConfigParser()
config.read(APP_ROOT_DIR + 'python/globe.config')

#parse command line args
parser.add_argument("-d","--delete", action="store_true", default=False, help="delete the existing database and download all new data from the API")
args = parser.parse_args()

if(args.delete):
	print 'You have specified delete so I will delete and re-create the database'


#delete DB if it exists & they told us to
if (args.delete):
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

max_num_articles=config.getint('boston_globe','max_num_articles')
articles_at_a_time=config.getint('boston_globe','articles_at_a_time')
size = 0
lastArticleDate=""
results = db.view('globe/last_article_date')
for row in results:       
 	lastArticleDate = row['value']

if (lastArticleDate ==""):
	lastArticleDate = "20100101"

while size<max_num_articles:
	latestArticles = boston_globe.fetchLatestArticlesFromAPI(conn, size, lastArticleDate)
	if (len(latestArticles) ==0):
		break
	cleanArticles = geoprocessor.filterAndCleanArticles(latestArticles, conn)

	conn.saveAll(cleanArticles)
	size += articles_at_a_time


print "Done adding articles from the API"