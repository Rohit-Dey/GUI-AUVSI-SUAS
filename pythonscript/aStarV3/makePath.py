import geopy
from math import *
from aStarV3 import geofenceband,pathGenerating

def compute_gps(x,y,centLat,centLon,bear,h):
    if y==0:
        y=0.00000001

    theta = atan(x/y)
    theta = degrees(theta)
    newbear=bear

    if y<0:
        newbear=bear-theta
    if y>0:
        newbear=bear+180-theta
    if newbear > 360:
        newbear-=360
    if newbear < 0:
        newbear+=360
    
    dist = sqrt(pow(x,2)+pow(y,2))
    dist/=1000
    pt = geopy.Point(centLat,centLon)
    obj = geopy.distance.distance(kilometers=dist)
    target_li = list(obj.destination(point=pt,bearing=newbear))
    targetList=(target_li[0],target_li[1],h)

    return targetList

def ifobs(start,end,ob):
    for i in range(len(ob)):
        dist = geofenceband.calculateDistance(start, end, ob[i])
        perp = geofenceband.perpendicularpt(start,end,ob[i])

        if (geofenceband.displacement(start,perp) + geofenceband.displacement(end, perp)) - 3 > geofenceband.displacement(start,end):
            dist = 999999

        if dist <= ob[i][2]:
            return True
    return False

def estimate_path(bin_path,ob):
    final_path = [bin_path[0]]
    end_waypoint= bin_path[-1]

    while final_path[-1] != bin_path[-1]:
        if not ifobs(final_path[-1],bin_path[-1],ob):
            final_path.append(bin_path[-1])
            continue
        sliced_array = bin_path[bin_path.index(final_path[-1]):bin_path.index(end_waypoint)]
        mid_point = sliced_array[len(sliced_array)//2]

        if ifobs(final_path[-1],mid_point,ob):
            end_waypoint = mid_point

        else:
            final_path.append(mid_point)
            end_waypoint = bin_path[-1]

    return final_path

def gotopath(wp,ob,geo,rows,cols):
    path = []
    # print(len(wp))
    for i in range(len(wp)):
        # print(i)
        if i == len(wp)-1:
            break
        # print("##########################################################################")
        # print("going for waypoint no. :", i+1)
        # print("##########################################################################")
        st = wp[i]
        ed = wp[i+1]

        if ifobs(st,ed,ob):
            # print("if")
            p = []

            world = pathGenerating.Gridworld((rows,cols))
            #   stat position and Goal
            start = pathGenerating.Cell()
            end = pathGenerating.Cell()
            # goal.position = (10, 10)
            if i+1 == len(wp):
                #Cell = (x,y),parent,g,h,f
                start.position = wp[i]
                end.position = wp[0]
            else:
                start.position = wp[i]
                end.position = wp[i+1]

            p = pathGenerating.astar(world,start,end,ob,geo)
            bin_path = p
            bin_path = estimate_path(bin_path,ob)
        else:
            # print("else")
            bin_path = [st,ed]
        path.extend(bin_path)

    return path
    # s = astar(world, start, goal, [(7,7,1)], [(0,0),(0,15),(15,15),(15,0)])

def removeDuplicate(a):
    b = []
    for i in a:
        if i not in b:
            b.append(i)

    return b

def wayptCoor(f,g,l,k):
    h=[]
    a=l[0]
    b=l[1]
    c=k[0]
    d=k[1]
    for i in f:
        if c<a and d<b:
            X2=i[0]*g*(1)
            Y2=i[1]*g*(-1)
        elif c>a and d<b:
            X2=i[0]*g*(-1)
            Y2=i[1]*g*(-1)
        elif c<a and d>b:
            X2=i[0]*g*(1)
            Y2=i[1]*g*(1)
        else:
            X2=i[0]*g*(-1)
            Y2=i[1]*g*(1)
            Z=i[2]

        coor = compute_gps(Y2,X2,a,b,0,Z)
        h.append(coor)

    return h

def addHeight(p,wpc,c):
    newP = []
    wpc.reverse
    i = 0
    while True:
        if i == len(wpc):
            return newP 
        for j in range(len(p)):
            if p[j] != wpc[i]:
                a = [p[j][0],p[j][1],c[i][2]]
                newP.append(a)
            else:
                a = [p[j][0],p[j][1],c[i][2]]
                newP.append(a)
                i+=1

def obsmerger(a,b):
    ob = []
    for i in range(len(a)):
        ob.append([a[i][0],a[i][1], b[i]])

    return ob

def findPath(wayptCart,ob,geofCart,wayptGeo,cd,minCoor,maxCoor,rows,columns):
    generatedPath = gotopath(wayptCart,ob,geofCart,rows,columns)
    Path = removeDuplicate(generatedPath)
    path = addHeight(Path,wayptCart,wayptGeo)
    Waypoints = wayptCoor(path,cd,minCoor,maxCoor)

    return Waypoints

def jSonOutput(a):
    D = {}
    l = []
    d = {}
    for i in a:
        l.append({"latitude":i[0] , "longitude":i[1], "altitude":i[2]})

    D["obstacleFreePath"] = l

    return D
