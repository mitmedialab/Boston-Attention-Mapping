################################################################
# The purpose of this script is to generate neighborhood shapes from the census files downloaded
# from the BRA which they mapped to neighborhoods.
#
# Once you have a *.shp file you can use ogr2ogr to convert it to GeoJSON and display
# it on the map. 
#
################################################################

import osgeo.gdal as gdal, osgeo.ogr as ogr,osgeo.osr as osr
import os

#CENSUS FILE PATHS
PATH_TO_CENSUS_TRACTS_DIR="../data/Boston_Census_Tracts_2010"
CENSUS_SHAPE_NAME="tl_2010_25025_tract10.shp"

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



################################################################################
#LOAD CENSUS FILE
################################################################################
os.chdir(PATH_TO_CENSUS_TRACTS_DIR)

# load the shapes files 
drv = ogr.GetDriverByName('ESRI Shapefile')
neighborhoodShape = drv.Open(CENSUS_SHAPE_NAME)
neighborhoodLayer = neighborhoodShape.GetLayer(0)

spatialRef = osr.SpatialReference()
#set projection & geo coord system - this comes from metadata in neighborhood files
#spatialRef.SetLCC(41.716667,42.683333,41.000000,-71.500000,200000.000000,750000.000000)
spatialRef.SetWellKnownGeogCS("NAD83")
#wktFromPrj = open(CENSUS_PRJ_NAME, 'r').read()
#spatialRef.ImportFromWkt(wktFromPrj);
#translate to WGS84 which is lat/long
spatialRef2=osr.SpatialReference()
spatialRef2.SetWellKnownGeogCS("WGS84")
neighborhoodTransformObject=osr.CoordinateTransformation( spatialRef,spatialRef2)

geometriesByNeighborhood = {}

#set up new shape file for our neighborhoods
# create a new data source and layer
if os.path.exists('test.shp'):
	drv.DeleteDataSource('test.shp') 
ds = drv.CreateDataSource('test.shp')

if ds is None:
	print 'Could not create file'
	sys.exit(1)
layer = ds.CreateLayer('test', geom_type=ogr.wkbPolygon)

# add an id field to the output
fieldDefn = ogr.FieldDefn('id', ogr.OFTInteger)
layer.CreateField(fieldDefn)
# add an name field to the output
fieldDefn = ogr.FieldDefn('name', ogr.OFTString)
layer.CreateField(fieldDefn)


#iterate through features
for x in range(0,neighborhoodLayer.GetFeatureCount()):
	feature=neighborhoodLayer.GetFeature(x)
	poly=feature.GetGeometryRef()
	tractNumber=feature.GetFieldAsString(2)
	
	try:
		neighborhood = CENSUS_TRACTS_TO_NEIGHBORHOOD[str(tractNumber)]
	except KeyError:
		print "No neighborhood for tract #" + tractNumber
		continue
	print neighborhood
	if len(neighborhood) > 0:
		poly.Transform(neighborhoodTransformObject)
		if neighborhood not in geometriesByNeighborhood:
			geometriesByNeighborhood[neighborhood] = []
	
		geometriesByNeighborhood[neighborhood].append(poly.Clone())
		print "putting " + tractNumber + " in poly" 
	
print geometriesByNeighborhood

newGeometry = None
featureId = 1
for neighborhood in geometriesByNeighborhood.keys():
	print "in neighborhood " + neighborhood 
	polyArray = geometriesByNeighborhood[neighborhood]
	
	for polygon in polyArray:

		if newGeometry is None:
			newGeometry = polygon
			print "setting new geo to this polygon"
		else:
			
			newGeometry = newGeometry.Union(polygon) 
			print "joined geometry"
	
	# get the FeatureDefn for the output layer
	featureDefn = layer.GetLayerDefn() 
	# create a new feature
	feature = ogr.Feature(featureDefn)
	feature.SetGeometry(newGeometry)
	feature.SetField('id', featureId)
	feature.SetField('name', neighborhood)
	# add the feature to the output layer
	layer.CreateFeature(feature)
	
	newGeometry = None
	featureId=featureId+1

print layer
print "all done"