# import dronekit
# import geopy
# from math import radians, cos, sin, asin, sqrt,atan2
# from shapely.wkt import loads
# from shapely.geometry import LineString
from math import *
import math
from geopy import distance
#from typing import Final

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        # Clockwise orientation
        return 1
    elif (val < 0):
        # Counterclockwise orientation
        return 2
    else: 
        # Collinear orientation
        return 0
# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1,q1,p2,q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True
    # Special Cases
    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
    return False
 
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       #print("Sad Life")
       return (None, None)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def bearing(lat1,lon1,lat2,lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = abs(lon2-lon1)
    bearing = atan2(sin(dlon) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon))
    return (degrees(bearing))

def distance(lat1,lon1,lat2,lon2): 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    dlon = lon2-lon1  
    dlat = lat2-lat1 
    a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
    c = 2 * asin(sqrt(a))
    R = 6371 
    return(c * R)

def pointRadialDistance(lat1,lon1,angle,d):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    R = 6371
    d = d/1000
    ad = d/R
    lat2 = asin(sin(lat1)*cos(ad) +cos(lat1)*sin(ad)*cos(angle))
    lon2 = lon1 + atan2(sin(angle)*sin(ad)*cos(lat1),cos(ad)-sin(lat1)*sin(lat2))
    lat = degrees(lat2)
    lon = degrees(lon2)
    b = [lat,lon]
    return b

def intialwaypoints(n,p1,p2,p3,p4,x):
    x = float(x)
    x = radians(x)
    dis = 1000*float(distance(p1[0],p1[1],p2[0],p2[1])/n)
    a = []
    for i in range(n):
        if i == 0:
            u = pointRadialDistance(p1[0],p1[1],x,(dis/2))
            #print(u)
            a.append(u)
        else:
            nmmm = pointRadialDistance(a[i-1][0],a[i-1][1],x,(dis))
            #print(nmmm)
            a.append(nmmm)
    return a

def finalwaypoints(n,p1,p2,p3,p4,x):
    x = float(x)
    x = radians(x)
    b = []
    dis = 1000*float(distance(p1[0],p1[1],p2[0],p2[1])/n)
    for i in range(n):
        if i == 0:
            u = pointRadialDistance(p4[0],p4[1],x,(dis/2))
            #print(u)
            b.append(u)
        else:
            nmmm = pointRadialDistance(b[i-1][0],b[i-1][1],x,(dis))
            #print(nmmm)
            b.append(nmmm)
    return b

def stayInPolygon(initialWp, finalWp, polygon):
    pointsOnPlygon = []
    for i in range(len(initialWp)):
        line1 = (initialWp[i], finalWp[i])
        for j in range(len(polygon)-1):
            line2 = (polygon[j], polygon[j+1])
            p1 = Point(initialWp[i][0], initialWp[i][1])
            q1 = Point(finalWp[i][0], finalWp[i][1])
            p2 = Point(polygon[j][0], polygon[j][1])
            q2 = Point(polygon[j+1][0], polygon[j+1][1])
            
            if doIntersect(p1, q1, p2, q2):
                #print("Yes")
                pointOfIntersect = line_intersection(line1, line2)
                if pointOfIntersect != (None, None):
                    #print("Bravo!! \n")
                    pointsOnPlygon.append(pointOfIntersect)
                else:
                    continue
                    #print("No!! \n")
            else:
                continue
                #print("No")
    return pointsOnPlygon

def get_distance(lat1,lon1,lat2,lon2): 
    # lon1=radians(lon1) 
    # lon2=radians(lon2)
    # lat1=radians(lat1) 
    # lat2=radians(lat2) 
    # dlon=lon2-lon1  
    # dlat=lat2-lat1 
    # a=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    # c=2*asin(sqrt(a))
    # R=6371 
    # return(c*R*1000)
    return distance(lat1,lon1,lat2,lon2)*1000

####################MAIN#######################################################
# polygon = [
#     [-72.2801900, 42.9286432],
#     [-72.2802436, 42.9285647],
#     [-72.2847176, 42.9273706],
#     [-72.2839344, 42.9241025],
#     [-72.2820246, 42.9244324],
#     [-72.2802544, 42.9236468],
#     [-72.2782266, 42.9241810],
#     [-72.2778404, 42.9257130],
#     [-72.2779799, 42.9275591],
#     [-72.2801900, 42.9286432] 
# ]

def finalODLCWaypoints(polygon, altitude, fov_x = 56.71524, fov_y = 44.35683, n = 1, heading = 0):
    lat_list = []
    lon_list = []
    finalWpList = []
    loop_count = 0
    polygonList = []
    lastPolyElement = {"latitude": polygon[0]["latitude"], "longitude" : polygon[0]["longitude"]}
    polygon.append(lastPolyElement)
    # print(polygon)
    # exit(0)
    # fov_xm = math.tan(fov_x/2) * 2 * altitude
    # fov_ym = math.tan(fov_y/2) * 2 * altitude
    fov_xm = 0.53974 * 2 * altitude  ## altitude in meters
    fov_ym = 0.40765 * 2 * altitude  ## altitude in meters
    for i in polygon:
        polygonList.append([i["latitude"], i["longitude"]])
        lat_list.append(i["latitude"])
        lon_list.append(i["longitude"])

    searchAreaToRectangle = [
        [max(lat_list), max(lon_list)],
        [min(lat_list), max(lon_list)],
        [min(lat_list), min(lon_list)],
        [max(lat_list), min(lon_list)]
    ]
    p1, p2, p3, p4 = searchAreaToRectangle[0], searchAreaToRectangle[1], searchAreaToRectangle[2], searchAreaToRectangle[3]
    SAL = get_distance(p3[0], p3[1], p4[0], p4[1])
    heading = bearing(p1[0], p1[1], p2[0], p2[1])
    Initial_waypoints = intialwaypoints(int(ceil(SAL/fov_xm)), p1, p2, p3, p4, heading)
    Final_waypoints = finalwaypoints(int(ceil(SAL/fov_xm)), p1, p2, p3, p4, heading)
    odlcWaypoints = stayInPolygon(Initial_waypoints, Final_waypoints, polygonList)
    
    i = 0
    while (i < len(odlcWaypoints)):
        finalWpList.append([odlcWaypoints[i][0], odlcWaypoints[i][1]])
        if i + 1 == len(odlcWaypoints):
            break
        i = i + 1
        print(i)
        finalWpList.append([odlcWaypoints[i][0], odlcWaypoints[i][1]])
        if i + 2 == len(odlcWaypoints):
            break
        i = i + 2
        print(i) 

    D = {}
    wpList = []
    wpDict = []
    for i, val in enumerate(finalWpList):
        boom = {}
        boom["latitude"] = val[0]
        boom["longitude"] = val[1]
        boom["altitude"] = altitude
        wpDict.append(boom)
        wpList.append([val[0], val[1], altitude])
    # print(wp)
    # exit(0)
    D["obstacleFreePath"] = wpDict
    return wpList, D



# polygon = [[28.75300761, 77.11609657],
#             [28.75298162, 77.11644927],
#             [28.75345193, 77.11647595],
#             [28.75348571, 77.11570535],
#             [28.75332721, 77.11582094],
#             [28.75300241, 77.11578834]]



############################## TESTING ##########################
# anunay = finalODLCWaypoints(polygon = polygon, altitude = 25, fov_x = 56.71524, fov_y = 44.35683, n = 1, heading = 0)
# print(anunay)
##################################################################
##################################################################
##################################################################
# lat_list = []
# lon_list = []
# heading = 0 # not used
# fov_x = 26.98
# fov_y = 20.38
# n = 1

# for i in polygon:
#     lat_list.append(i[0])
#     lon_list.append(i[1])

# searchAreaToRectangle = [
#     [max(lat_list), max(lon_list)],
#     [min(lat_list), max(lon_list)],
#     [min(lat_list), min(lon_list)],
#     [max(lat_list), min(lon_list)]
# ] 
# # Considering heading a 0
# #   p2-------------p1
# #    |             |
# #    |             |
# #   p3-------------p4
# #print(searchAreaToRectangle)

# p1, p2, p3, p4 = searchAreaToRectangle[0], searchAreaToRectangle[1], searchAreaToRectangle[2], searchAreaToRectangle[3]
# SAL = get_distance(p3[0], p3[1], p4[0], p4[1])
# print("SAL: ", SAL)
# print("Start")
# print(p1,p2,p3,p4)
# heading = bearing(p1[0], p1[1], p2[0], p2[1])
# print("Heading is: ", heading)
# Initial_waypoints = intialwaypoints(int(ceil(SAL/fov_x)), p1, p2, p3, p4, heading)
# Final_waypoints = finalwaypoints(int(ceil(SAL/fov_x)), p1, p2, p3, p4, heading)
# print("Start")
# ans = stayInPolygon(Initial_waypoints, Final_waypoints, polygon)
# # A = Initial_waypoints[0]
# # B = Final_waypoints[0]
# # C = polygon[5]
# # D = polygon[6]
# # print("Check: ", A,B,C,D)
# # ans = line_intersection((A, B), (C, D))
# print(ans)
# print("Ended")