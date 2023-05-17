from math import *
#from typing import Final
from geopy import distance
from shapely.geometry import LineString
from shapely.geometry import Point as Poi

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

# def stayInPolygon(initialWp, finalWp, polygon):
#     pointsOnPlygon = []
#     for i in range(len(initialWp)):
#         line1 = (initialWp[i], finalWp[i])
#         for j in range(len(polygon)-1):
#             line2 = (polygon[j], polygon[j+1])
#             p1 = Point(initialWp[i][0], initialWp[i][1])
#             q1 = Point(finalWp[i][0], finalWp[i][1])
#             p2 = Point(polygon[j][0], polygon[j][1])
#             q2 = Point(polygon[j+1][0], polygon[j+1][1])
            
#             if doIntersect(p1, q1, p2, q2):
#                 #print("Yes")
#                 pointOfIntersect = line_intersection(line1, line2)
#                 if pointOfIntersect != (None, None):
#                     #print("Bravo!! \n")
#                     pointsOnPlygon.append(pointOfIntersect)
#                 else:
#                     continue
#                     #print("No!! \n")
#             else:
#                 continue
#                 #print("No")
#     return pointsOnPlygon

def rectangle(m,n,lat,lon,head):
    heading=float(head)
    heading=radians(heading)
    e=pointRadialDistance(lat,lon,heading,n)
    rheading=heading+pi/2
    lheading=heading-pi/2
    p1=pointRadialDistance(lat,lon,lheading,m/2)
    p2=pointRadialDistance(lat,lon,rheading,m/2)
    p3=pointRadialDistance(e[0],e[1],rheading,m/2)
    p4=pointRadialDistance(e[0],e[1],lheading,m/2)
    return p1,p2,p3,p4

# def get_distance(lat1,lon1,lat2,lon2):
#     print("DISTANCE", distance(lat1,lon1,lat2,lon2)) 
#     return distance(lat1,lon1,lat2,lon2)*1000

####################MAIN#######################################################

# def saruAvoidance(wpList, jsonMission):

#     obstacleList = jsonMission["stationaryObstacles"]
#     for i in range(len(wpList) - 1):
#         for j in obstacleList:
#             p = Point(j["latitude"], j["longitude"])
#             c = p.buffer(j["radius"] + 5).boundary
#             #print(p, c)
#             distX = Point(wpList[i][0], wpList[i][1]).distance(p)
#             distY = Point(wpList[i+1][0], wpList[i+1][1]).distance(p)
#             l = LineString([(wpList[i][0], wpList[i][1]), (wpList[i+1][0], wpList[i+1][1])])
#             try:
#                 if distX <= j["radius"] + 5:
#                     k = c.intersection(l)
#                     wpList[i][0], wpList[i][1] = k.geoms[0].coors[0][0], k.geoms[0].coors[0][1]
#                     wpDict[i]["latitude"], wpDict[i]["longitude"] = k.geoms[0].coors[0][0], k.geoms[0].coors[0][1]
#                 elif distY <= j["radius"] + 5:
#                     print(k)
#                     k = c.intersection(l)
#                     wpList[i+1][0], wpList[i+1][1] = k.geoms[0].coors[0][0], k.geoms[0].coors[0][1]
#                     wpDict[i+1]["latitude"], wpDict[i+1]["longitude"] = k.geoms[0].coors[0][0], k.geoms[0].coors[0][1]
#             except Exception as err:
#                 print("Skipping Obstacle: ", err)
#                 pass
#     return wpList, wpDict

def cartesianDistance(a, b):
    d = ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
    return d

def polygonGenerator(p1, p2, p3, p4, obstacles):
    corners = [p1, p2, p3, p4]
    coor = []
    line = []
    total = []
    print(obstacles)
    print(p1, p2, p3, p4)
    coor.append(Poi(p1[0], p1[1]))
    coor.append(Poi(p2[0], p2[1]))
    coor.append(Poi(p3[0], p3[1]))
    coor.append(Poi(p4[0], p4[1]))
    line.append(LineString([(p1[0], p1[1]),(p2[0], p2[1])]))
    line.append(LineString([(p2[0], p2[1]),(p3[0], p3[1])]))
    line.append(LineString([(p3[0], p3[1]),(p4[0], p4[1])]))
    line.append(LineString([(p4[0], p4[1]),(p1[0], p1[1])]))
    for i in corners:
        for j in obstacles:
            p = [j[0], j[1]]
            v = Poi(j[0], j[1])
            print(p)
            r = j[2] * 0.3048
            print(r)
            print(v, type(v))
            c = v.buffer(r).boundary
            dist = distance(i[0], i[1], p[0], p[1])
            if dist < r:
                intersect = c.intersection(line[corners.index(i)])
                total.append(intersect.geoms[0].coords[0])
    print(total)
    print("@#@#@#@#@")
    exit(0)



def waypointGenerator(SAL, SAB, center_coord, obstacles, fov_x, fov_y, n = 1, heading = 0):
    finalWpList = []
    loop_count = 0
    p1, p2, p3, p4 = rectangle(SAL, SAB, center_coord[0], center_coord[1], heading)
    print("Check")
    print(p1)
    #polygonGenerator(p1, p2, p3, p4, obstacles)
    # print("RECTANGLE COORDINATES : ")
    # print(p1, p2, p3, p4)
    heading = bearing(p1[0], p1[1], p2[0], p2[1])
    #print("Heading is: ", heading)
    wp_initial = intialwaypoints(int(ceil(SAL/fov_x)), p1, p2, p3, p4, heading)
    wp_final = finalwaypoints(int(ceil(SAL/fov_x)), p1, p2, p3, p4, heading)
    for i in range(0, len(wp_initial), 2):
        finalWpList.append([wp_initial[i][0], wp_initial[i][1]])
        finalWpList.append([wp_final[i][0], wp_final[i][1]])
        if ((i+1) < len(wp_initial)):
            finalWpList.append([wp_final[i+1][0], wp_final[i+1][1]])
            finalWpList.append([wp_initial[i+1][0], wp_initial[i+1][1]])
            loop_count += 2
    # print(loop_count)
    return finalWpList