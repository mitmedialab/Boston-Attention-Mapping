################################################################################
# Module that connects to Globe API and to Globe FTP data sources
# Gets latest data
################################################################################
import simplejson
import urllib2
import utils
import ConfigParser
from datetime import date


def fetchLatestArticlesFromAPI(conn, startIdx, lastArticleDate):

	APP_ROOT_DIR=utils.getAppRootDir()
	config = ConfigParser.ConfigParser()
	config.read(APP_ROOT_DIR + 'python/globe.config')

	articles_at_a_time=config.getint('boston_globe','articles_at_a_time')
	api_fields=config.get('boston_globe','api_fields')

	today = date.today()
	todayStr = today.strftime('%Y%m%d')

	allArticles = []
	
	req = urllib2.Request(	"http://50.17.92.83/s?key=catherine&bq=printpublicationdate:" +
							lastArticleDate +".."+todayStr+"&return-fields="+
							api_fields+
							"&size="+str(articles_at_a_time)+"&"+
							"start="+str(startIdx)+
							"&rank=printpublicationdate")
	print req.get_full_url()
	opener = urllib2.build_opener()

	#try and then basically try again
	#sometimes server returns 500 error, so just try the same request again to see if that will catch these cases
	try:
		f = opener.open(req)
	except:
		f = opener.open(req)

	try:
		data = simplejson.load(f)
	except:
		print "JSONDecodeError\nEither there was no data found or some other parsy thing happened"

	print str(data["hits"]["found"]) + " articles found"

	conn.db_metadata["total_articles_available"] = data["hits"]["found"]
	
	allArticles.extend(data["hits"]["hit"])

	return allArticles
