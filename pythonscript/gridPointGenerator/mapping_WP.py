from math import *
import math
import geopy
import geopy.distance
from gridPointGenerator import MAPPING_grid


def compute_gps(x, y,  cent_lat, cent_lon, bear):

        theta = math.atan(x / y)
        theta = degrees(theta)
        newbear=bear
        if (y < 0):
            newbear = bear - theta
        if (y > 0):
            newbear = bear + 180 - theta
        if (newbear > 360):
            newbear -= 360
        if (newbear < 0):
            newbear += 360
        dist = sqrt(pow(x, 2) + pow(y, 2))
        dist /= 1000

        pt = geopy.Point(cent_lat,cent_lon)
        obj = geopy.distance.distance(kilometers=dist)
        target_li = list(obj.destination(point=pt, bearing=newbear))
        # print(target_li)
        return target_li#[0],target_li[1]


def center(height, width, lat, lon):
	centerCoordinates = []
	x = 0
	y = height/2
	output = compute_gps(x, y, lat, lon, bear = 0)
	centerCoordinates.append([output[0], output[1]])
	return centerCoordinates


def finalMappingWaypoints(SAB, center_lat, center_lon, obstacles, mapping_alt = 100, fov_x = 56.71524, fov_y = 44.35683):  ## mapping alt in meter
    SAB = 0.3048 * SAB ######### feet to meter 
    SAL = 16*(SAB/9)
    # fov_xm = math.tan(fov_x/2) * 2 * mapping_alt
    # fov_ym = math.tan(fov_y/2) * 2 * mapping_alt
    fov_xm = 0.53974 * 2 * mapping_alt   ### in meter
    fov_ym = 0.40765 * 2 * mapping_alt  ### in meter
    centerBelowMapLine = center(SAB, SAL, center_lat, center_lon)
    getWPList = MAPPING_grid.waypointGenerator(SAL = SAL, SAB = SAB, center_coord = centerBelowMapLine[0], obstacles = obstacles, fov_x = fov_xm, fov_y = fov_ym)
    D = {}
    wpList = []
    wpDict = []
    for i, val in enumerate(getWPList):
        boom = {}
        boom["latitude"] = val[0]
        boom["longitude"] = val[1]
        boom["altitude"] = mapping_alt
        wpDict.append(boom)
        wpList.append([val[0], val[1], mapping_alt])
    D["obstacleFreePath"] = wpDict
    return wpList, D
    # print(wpDict)
    # exit(0)


#################### TESTING #######################
# anunay = finalMappingWaypoints(150, 28.75364020, 77.11607497, 100)
# print(anunay)
