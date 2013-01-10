################################################################################
# little utils stuff
################################################################################
import os

def getAppRootDir():
	return os.path.dirname(os.path.dirname( os.path.abspath(__file__) ) )+ "/"