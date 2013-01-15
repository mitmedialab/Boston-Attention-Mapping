################################################################################
# Processes articles to check lat/longs against shape files and verify city data
################################################################################

import osgeo.gdal as gdal, osgeo.ogr as ogr, osgeo.osr as osr
import ConfigParser, os, csv, simplejson as json
from titlecase import titlecase
import utils


class Geoprocessor:
    APP_ROOT_DIR = utils.getAppRootDir()

    ################################################################################
    # These things are not happening in an init method because GDAL throws segfaults
    # when the layers & transforms are instance variables. Not sure why.
    ################################################################################

    config = ConfigParser.ConfigParser()
    config.read(APP_ROOT_DIR + 'python/globe.config')
    path_to_census_tracts_dir = APP_ROOT_DIR + config.get('geo', 'path_to_census_tracts_dir')
    census_shape_name = config.get('geo','census_shape_name')
    path_to_towns_dir = APP_ROOT_DIR + config.get('geo','path_to_towns_dir')
    towns_shape_name = config.get('geo','towns_shape_name')
    excluded_lat1k_long1k = json.loads(config.get('geo','excluded_lat1k_long1k'))

    censusTracts = csv.reader(open(APP_ROOT_DIR + config.get('geo','census_tracts_to_neighborhood'), "rU"))
    censusTracts_list = []
    censusTracts_list.extend(censusTracts)
    census_tracts_to_neighborhood ={}
    for row in censusTracts_list:
        census_tracts_to_neighborhood[row[0]] = row[1]
    
    ################################################################################
    #LOAD CENSUS SHP FILE
    ################################################################################
    os.chdir(path_to_census_tracts_dir)
    drv = ogr.GetDriverByName('ESRI Shapefile')
    neighborhoodShape = drv.Open(census_shape_name)
    neighborhoodLayer = neighborhoodShape.GetLayer(0)

    spatialRef = osr.SpatialReference()

    #set projection & geo coord system - this comes from metadata in neighborhood files
    spatialRef.SetWellKnownGeogCS("NAD83")

    #translate to WGS84 which is lat/long
    spatialRef2=osr.SpatialReference()
    spatialRef2.SetWellKnownGeogCS("WGS84")
    neighborhoodTransformObject=osr.CoordinateTransformation( spatialRef,spatialRef2)

    ################################################################################
    #LOAD TOWNS SHP FILE
    ################################################################################
    os.chdir(path_to_towns_dir)
    drv = ogr.GetDriverByName('ESRI Shapefile')
    townShape = drv.Open(towns_shape_name)
    townsLayer = townShape.GetLayer(0)

    spatialRef3 = osr.SpatialReference()
    #set projection & geo coord system - this comes from metadata in neighborhood files
    spatialRef3.SetLCC(41.716667,42.683333,41.000000,-71.500000,200000.000000,750000.000000)
    spatialRef3.SetWellKnownGeogCS("NAD83")

    #translate to WGS84 which is lat/long
    spatialRef4=osr.SpatialReference()
    spatialRef4.SetWellKnownGeogCS("WGS84")
    townTransformObject=osr.CoordinateTransformation( spatialRef3,spatialRef4)


    def getNeighborhoodFromLatLong(self, latitude, longitude):
        
        for x in range(0,self.neighborhoodLayer.GetFeatureCount()):

            feature=self.neighborhoodLayer.GetFeature(x)
            poly=feature.GetGeometryRef()
            tractNumber=feature.GetFieldAsString(2)
            
            poly.Transform(self.neighborhoodTransformObject)
            
            WGSPoint =ogr.Geometry(ogr.wkbPoint)
            WGSPoint.SetPoint(0,longitude,latitude)
            if poly.Contains(WGSPoint):
                try:
                    neighborhood = self.census_tracts_to_neighborhood[tractNumber]
                except KeyError:
                    print "censusTract # "+tractNumber + " doesn't exist in the mapping file"
                    return ""
                print "Point is in " + neighborhood

                return neighborhood
        return ""

    def getCityFromLatLong(self, latitude, longitude):

        for x in range(0,self.townsLayer.GetFeatureCount()):
            feature=self.townsLayer.GetFeature(x)
            poly=feature.GetGeometryRef()
            city=feature.GetFieldAsString(1)
            poly.Transform(self.townTransformObject)

            WGSPoint =ogr.Geometry(ogr.wkbPoint)
            WGSPoint.SetPoint(0,longitude,latitude)
            if poly.Contains(WGSPoint):
            
                city = titlecase(city)
                print "Point is in " + city
                return city
        return ""

    def filterAndCleanArticles(self, allArticles, conn):
        db = conn.db
        
        cleanedArticles = []

        for article in allArticles:
            if conn.documentExists(article["id"]):
                print "document id " + article['id'] + " already exists - discarding..." 
                continue
            
            conn.db_metadata["last_article_date"]=article["data"]["printpublicationdate"]
            conn.db_metadata["last_article_id"]=article["id"]

            #create a document and insert it into the db:
            article["_id"] = article["id"]
            
            #If article has geocoding AND it doesn't have excluded lat longs then include in data set
            if len( article["data"]["latitude"] ) > 0 :
                latlong1k = [ article["data"]["latitude_1k"][0], article["data"]["longitude_1k"][0] ]

                if latlong1k in self.excluded_lat1k_long1k:
                    conn.db_metadata["filtered_articles_bad_geodata"]+=1
                    print "Filtering the point " + str(article["data"]["latitude"][0]) + ", "+ str(article["data"]["longitude"][0]) 
                    continue
                else : 

                    #Now apply various processing to data, add metadata for neighborhoods to record and save to DB
                    #GET NEIGHBORHOOD
                    neighborhood = self.getNeighborhoodFromLatLong(float(article["data"]["latitude"][0]), float(article["data"]["longitude"][0]))
                    article["data"]["neighborhood"]=neighborhood

                    #GET CITY & change it if it's entered improperly from Globe

                    cityFromLatLong = self.getCityFromLatLong(float(article["data"]["latitude"][0]), float(article["data"]["longitude"][0]))    
                    if article["data"]["city"] == None or len(article["data"]["city"]) ==0:
                        article["data"]["city"] = [""];
                    
                    #Fix up state declarations to MA instead of Mass, Massachusetts and all manner of whatnot
                    if len(cityFromLatLong) > 0:
                        if article["data"]["state"] == None or len(article["data"]["state"]) ==0:
                            article["data"]["state"] = [""];
                        
                        oldState = article["data"]["state"][0]

                        if "MA" != article["data"]["state"][0]:
                            article["data"]["state"][0]="MA"
                            print "Changed state to MA from Globe entered state " + oldState + " for city " + cityFromLatLong
     
                    if cityFromLatLong != article["data"]["city"][0] and len(cityFromLatLong) > 0 :                     
                        print "Changing Globe entered city " + article["data"]["city"][0] + " to verified city " + cityFromLatLong
                        conn.db_metadata["number_of_updated_MA_city_names"]+=1
                        #save the city data as entered by the Globe
                        article["data"]["city_OLD"]=article["data"]["city"][0]

                        article["data"]["city"][0]=cityFromLatLong
                        
                    if (len(article["data"]["city"]) > 0):
                        city = str(article["data"]["city"][0])
                    else :
                        city = ""
                    
                    
                    article["type"] = "article"
                    cleanedArticles.append(article)
                    conn.db_metadata["total_articles_added"]+=1
            else: 
                conn.db_metadata["filtered_articles_no_geodata"]+=1
                print "Filtering this article because there's no geodata. "
                continue
                
        return cleanedArticles