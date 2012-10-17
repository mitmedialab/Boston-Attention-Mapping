#########################################################################
#																		#		
# Downloads the whole Boston Globe article DB and puts it in a couchDB 	#
#																		#		
#########################################################################


import couchdb
import simplejson as json
import urllib2
import gdal,ogr,osr
import os
import csv

#db_metadata stores info about the whole DB, including # articles, filtered articles, reasons for filtering,etc
db_metadata = {}
db_metadata["type"] = "metadata"
db_metadata["point_in_boston_but_no_census_tract_available"]=0

def getNeighborhoodFromLatLong(latitude, longitude):
	
	#iterate through features
	for x in range(0,layer.GetFeatureCount()):
		feature=layer.GetFeature(x)
		poly=feature.GetGeometryRef()
		tractNumber=feature.GetFieldAsString(2)
		poly.Transform(transformObject)

		WGSPoint =ogr.Geometry(ogr.wkbPoint)
		WGSPoint.SetPoint(0,longitude,latitude)
		if poly.Contains(WGSPoint):
			try:
				neighborhood = CENSUS_TRACTS_TO_NEIGHBORHOOD[tractNumber]
			except KeyError:
				print "censusTract # "+tractNumber + " doesn't exist in the mapping file"
				db_metadata["point_in_boston_but_no_census_tract_available"]+=1
				return ""
			print "Point is in " + neighborhood

			return neighborhood
   	return ""

DATABASE_NAME = "boston-globe-articles"
MAX_NUM_ARTICLES = 45000
ARTICLES_AT_A_TIME = 500
PATH_TO_CENSUS_TRACTS_DIR="../data/Boston_Census_Tracts_2010"
CENSUS_SHAPE_NAME="tl_2010_25025_tract10.shp"
CENSUS_PRJ_NAME="tl_2010_25025_tract10.shp"

#these lat-longs are filtered because bad data or else from people typing "boston,ma"
EXCLUDED_LAT1K_LONG1K={
"42354":"71066",
"42341":"71063",
"42315":"71052",
"42358":"71059"}


#these mappings are from BRA data
CENSUS_TRACTS_TO_NEIGHBORHOOD = {"010405":"Fenway",
"010404":"Fenway",
"010801":"Back Bay",
"010702":"Back Bay",
"010204":"Fenway",
"010802":"Back Bay",
"010104":"Fenway",
"000703":"Allston",
"000504":"Brighton",
"000704":"Allston",
"010103":"Fenway",
"000803":"Allston",
"980300":"Roxbury",
"120201":"Jamaica Plain",
"120104":"Jamaica Plain",
"110607":"Roslindale",
"000302":"Brighton",
"000301":"Brighton",
"140400":"Hyde Park",
"140300":"Hyde Park",
"140201":"Hyde Park",
"140202":"Hyde Park",
"140102":"Hyde Park",
"130402":"West Roxbury",
"130300":"West Roxbury",
"130200":"West Roxbury",
"130100":"West Roxbury",
"120700":"Jamaica Plain",
"120600":"Jamaica Plain",
"120500":"Jamaica Plain",
"120400":"Jamaica Plain",
"110601":"West Roxbury",
"110502":"Roslindale",
"110501":"Roslindale",
"110401":"Roslindale",
"101102":"Mattapan",
"101101":"Mattapan",
"101002":"Mattapan",
"101001":"Mattapan",
"100900":"Mattapan",
"100800":"Dorchester",
"100601":"Dorchester",
"100500":"Dorchester",
"100400":"Dorchester",
"100300":"Dorchester",
"981300":"East Boston",
"981201":"South Boston",
"990101":"",
"981501":"Allston",
"981700":"Beacon Hill",
"981800":"Longwood Medical Area",
"100200":"Dorchester",
"100100":"Dorchester",
"092400":"Dorchester",
"092300":"Dorchester",
"092200":"Dorchester",
"092000":"Dorchester",
"091900":"Dorchester",
"091800":"Dorchester",
"091700":"Dorchester",
"091600":"Dorchester",
"981100":"Mattapan",
"140105":"Hyde Park",
"980700":"Hyde Park",
"120105":"Jamaica Plain",
"120301":"Jamaica Plain",
"071201":"South End",
"091001":"Dorchester",
"091500":"Dorchester",
"091400":"Dorchester",
"091300":"Dorchester",
"091200":"Dorchester",
"091100":"Dorchester",
"090700":"Dorchester",
"090600":"Roxbury",
"090400":"Roxbury",
"090300":"Dorchester",
"090200":"Dorchester",
"980101":"Harbor Islands",
"040801":"Charlestown",
"010203":"Fenway",
"110403":"Roslindale",
"110201":"Roslindale",
"981000":"Jamaica Plain",
"090100":"Dorchester",
"082100":"Roxbury",
"082000":"Roxbury",
"081900":"Roxbury",
"081800":"Roxbury",
"081700":"Roxbury",
"081500":"Roxbury",
"081400":"Roxbury",
"081300":"Roxbury",
"110103":"Jamaica Plain",
"110301":"Roslindale",
"140106":"Roslindale",
"010701":"Back Bay",
"010408":"Fenway",
"000503":"Brighton",
"081200":"Jamaica Plain",
"081100":"Mission Hill",
"080900":"Mission Hill",
"080801":"Mission Hill",
"080601":"Roxbury",
"080500":"Roxbury",
"080401":"Roxbury",
"080300":"Roxbury",
"071101":"South End",
"070900":"South End",
"140107":"Hyde Park",
"130404":"West Roxbury",
"130406":"West Roxbury",
"120103":"Jamaica Plain",
"100700":"Dorchester",
"100603":"Dorchester",
"092101":"Dorchester",
"061101":"South Boston",
"070800":"South End",
"070700":"South End",
"070600":"South End",
"070500":"South End",
"070300":"Bay Village",
"070200":"Downtown",
"070101":"Leather District",
"061200":"South Boston",
"061000":"South Boston",
"060800":"South Boston",
"060700":"South Boston",
"080100":"Roxbury",
"060301":"South Boston",
"090901":"Dorchester",
"060101":"South Boston",
"981502":"East Boston",
"060600":"South Boston Waterfront",
"060400":"South Boston",
"060200":"South Boston",
"051200":"East Boston",
"050700":"East Boston",
"050600":"East Boston",
"050500":"East Boston",
"050400":"East Boston",
"050300":"East Boston",
"050200":"East Boston",
"040300":"Charlestown",
"040200":"Charlestown",
"030500":"North End",
"981600":"East Boston",
"051101":"East Boston",
"051000":"East Boston",
"030400":"North End",
"030300":"Downtown",
"030200":"North End",
"030100":"North End",
"020200":"Beacon Hill",
"010600":"Back Bay",
"010500":"Back Bay",
"010300":"Longwood Medical Area",
"000802":"Allston",
"000701":"Brighton",
"050101":"East Boston",
"050901":"East Boston",
"060501":"South Boston",
"981202":"South Boston Waterfront",
"040100":"Charlestown",
"040600":"Charlestown",
"000602":"Brighton",
"000601":"Brighton",
"000502":"Brighton",
"000402":"Brighton",
"000401":"Brighton",
"000202":"Brighton",
"000201":"Brighton",
"040401":"Charlestown",
"020303":"Downtown",
"070402":"South End",
"020302":"Beacon Hill",
"020301":"West End",
"020101":"Beacon Hill",
"081001":"Mission Hill",
"010403":"Fenway",
"000100":"Brighton"}



#Read in Neighborhood metadatafile to memory
neighborhoodMetaData = csv.reader(open("../data/Boston_Neighborhood.csv", "rU"))
neighborhoodMetaData_list = []
neighborhoodMetaData_list.extend(neighborhoodMetaData)
neighborhoods ={}
for row in neighborhoodMetaData_list:
	metadata = {	
					'neighborhood_population_2010': row[3],
					'neighborhood_percent_non_white':row[5],
					'neighborhood_median_household_income':row[7],
					'neighborhood_per_capita_income':row[9],
					'neighborhood_percent_unemployed':row[11],
					'neighborhood_percent_below_poverty_line':row[13],

				}
	neighborhoods[row[0]] = metadata

#Set up some of the geo stuff
os.chdir(PATH_TO_CENSUS_TRACTS_DIR)
# load the shape file as a layer
drv = ogr.GetDriverByName('ESRI Shapefile')
shape = drv.Open(CENSUS_SHAPE_NAME)
layer = shape.GetLayer(0)

spatialRef = osr.SpatialReference()
#set projection & geo coord system - this comes from metadata in neighborhood files
#spatialRef.SetLCC(41.716667,42.683333,41.000000,-71.500000,200000.000000,750000.000000)
spatialRef.SetWellKnownGeogCS("NAD83")
#wktFromPrj = open(CENSUS_PRJ_NAME, 'r').read()
#spatialRef.ImportFromWkt(wktFromPrj);
#translate to WGS84 which is lat/long
spatialRef2=osr.SpatialReference()
spatialRef2.SetWellKnownGeogCS("WGS84")
transformObject=osr.CoordinateTransformation( spatialRef,spatialRef2)



#get couchDB
couch = couchdb.Server() # Assuming localhost:5984

#delete DB if it exists
try:
	del couch[DATABASE_NAME]
except couchdb.http.ResourceNotFound:
   	print "Database doesn't exist. We'll go ahead and create it."

# create & select DB
db = couch.create(DATABASE_NAME)

#Make a number of http requests to download all the data. Too many at one time leads to 500 error
size = 0
db_metadata["filtered_articles_no_geodata"] = 0
db_metadata["filtered_articles_bad_geodata"] =0
db_metadata["total_articles_added"] = 0
db_metadata["total_articles_available"] = 0
while size<MAX_NUM_ARTICLES:
	req = urllib2.Request(	"http://50.17.92.83/s?key=catherine&bq=printpublicationdate:20000401..20130500&return-fields="+
							"catherine_dignazio,"+
							"id,"+
							"headline,"+
							"subheadline,"+
							"subhead,"+
							"tagline,"+
							"latitude,"+
							"longitude,"+
							"latitude_1k,"+
							"longitude_1k,"+
							"summary,"+
							"content,"+
							"keywords,"+
							"address,"+
							"city,"+
							"state,"+
							"zip,"+
							"country,"+
							"canonicalurl,"+
							"byname,"+
							"bysource,"+
							"printproduct,"+
							"printedition,"+
							"printbook,"+
							"printsection,"+
							"printpagenumber,"+
							"printpublicationdate,"+
							"publicationstartdate,"+
							"reviewtype,"+
							"&size="+str(ARTICLES_AT_A_TIME)+"&"+
							"start="+str(size)+
							"&rank=-printpublicationdate")
	print req.get_full_url()
	opener = urllib2.build_opener()
	f = opener.open(req)

	try:
		data = json.load(f)
	except:
		print "JSONDecodeError\nEither there was no data found or some other parsy thing happened"
		break

	print str(data["hits"]["found"]) + " articles found"

	db_metadata["total_articles_available"] = data["hits"]["found"]

	if MAX_NUM_ARTICLES > int(data["hits"]["found"]):
		MAX_NUM_ARTICLES = data["hits"]["found"]
		print "Resetting max articles to " + str(data["hits"]["found"])
	
	#add articles to DB
	allArticles = data["hits"]["hit"]
	
	if len(allArticles) == 0:
		break
	
	for article in allArticles:
		if size == 0 and allArticles[0] == article :
			db_metadata["last_article_date"]=article["data"]["printpublicationdate"]
		
		#create a document and insert it into the db:
		article["_id"] = article["id"]
		
		#If article has geocoding AND it doesn't have excluded lat longs then include in data set
		if len(article["data"]["latitude"]) > 0 :
			if EXCLUDED_LAT1K_LONG1K.has_key(str(article["data"]["latitude_1k"][0])) and EXCLUDED_LAT1K_LONG1K[str(article["data"]["latitude_1k"][0])] == str(article["data"]["longitude_1k"][0]):
				db_metadata["filtered_articles_bad_geodata"]+=1
				print "Filtering the point " + str(article["data"]["latitude"][0]) + ", "+ str(article["data"]["longitude"][0]) 
				continue
			else : 
				#Now apply various processing to data, add metadata for neighborhoods to record and save to DB
				#GET NEIGHBORHOOD
				neighborhood = getNeighborhoodFromLatLong(float(article["data"]["latitude"][0]), float(article["data"]["longitude"][0]))
				article["data"]["neighborhood"]=neighborhood

				#ADD FULL TEXT AND WORD COUNT
				fullText = str(article["data"]["catherine_dignazio"])
				article["data"]["fulltext"]=article["data"]["catherine_dignazio"]
				article["data"]["catherine_dignazio"]=None
				
				#FIX HERE
				
				fullTextSplit = fullText.split(None)
				article["data"]["wordcount"] = len(fullTextSplit)
				print fullText
				print  len(fullTextSplit)	

				#ADD NEIGHBORHOOD METADATA
				if (len(neighborhood) > 0):
					metadata = neighborhoods[neighborhood]

					article["data"]['neighborhood_population_2010'] = metadata['neighborhood_population_2010']
					article["data"]['neighborhood_percent_non_white'] = metadata['neighborhood_percent_non_white']
					article["data"]['neighborhood_median_household_income'] = metadata['neighborhood_median_household_income']
					article["data"]['neighborhood_per_capita_income'] = metadata['neighborhood_per_capita_income']
					article["data"]['neighborhood_percent_unemployed'] = metadata['neighborhood_percent_unemployed']
					article["data"]['neighborhood_percent_below_poverty_line'] = metadata['neighborhood_percent_below_poverty_line']

				db_metadata["first_article_date"]= article["data"]["printpublicationdate"]
				article["type"] = "article"
				db.save(article)
				db_metadata["total_articles_added"]+=1
		else: 
			db_metadata["filtered_articles_no_geodata"]+=1
			print "Filtering this article because there's no geodata. "
			continue
	
	print "Article count " + str(db_metadata["total_articles_added"]) + " articles"
	print "Filtered " + str(db_metadata["filtered_articles_no_geodata"]) + " articles because no geodata"
	print "Filtered " + str(db_metadata["filtered_articles_bad_geodata"]) + " articles because bad geodata (excluded lat longs)"
	size += ARTICLES_AT_A_TIME



db.save(db_metadata)

print "All done, master\n"


