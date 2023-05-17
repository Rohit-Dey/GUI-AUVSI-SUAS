from aStarV2 import grid, imprtntpts, geofenceband, pathPlotting, inputs
#import inputs
from math import *
import geopy
import time

startTime = time.time()

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
    #targetList=(target_li[0],target_li[1],h)        ############# tuple by JHA2
    targetList = [target_li[0], target_li[1], h]   

    return targetList

def obstacleMergeList(a,b):
    ob = []
    for i in range(len(a)):
        ob.append((a[i][0],a[i][1],b[i]))
    
    return ob

# def perpendicularpt(a,b,o):
#     x1 = a[0]
#     y1 = a[1]
#     x2 = b[0]
#     y2 = b[1]
#     x3 = o[0]
#     y3 = o[1]
#     dx = x2 - x1
#     dy = y2 - y1
#     mag = sqrt(dx*dx + dy*dy)
#     if mag == 0:
#         mag =0.00000000000001
#     dx /= mag
#     dy /= mag

#     Lambda = (dx * (x3 - x1)) + (dy * (y3 - y1))
#     x4 = (dx * Lambda) + x1
#     y4 = (dy * Lambda) + y1
#     # k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)^2 + (x2-x1)^2)
#     # x4 = x3 - k * (y2-y1)
#     # y4 = y3 + k * (x2-x1)
#     return (x4,y4)

def line(p1, p2):
    a = (p1[1] - p2[1])
    b = (p2[0] - p1[0])
    c = (p1[0]*p2[1] - p2[0]*p1[1])
    return a, b, c

def findFoot(a, b, c, x1, y1):
 
    temp = (-1 * (a * x1 + b * y1 + c)
                  (a * a + b * b))
    x = temp * a + x1
    y = temp * b + y1
    return (x, y)

# def displacement(a,b):
#     d = ((a[0]-b[0])**2 + (a[1]-b[1])**2)**(0.5)
#     return d

def ifobs(start, end, ob):
    #print(start,' perp bis bw', end)
    for i in range(len(ob)):
        # a,b,c = pathPlotting.line(start, end)
        dist = pathPlotting.calculateDistance(start, end, ob[i])
        a,b,c=line(start, end)
        #perp  = findFoot(a,b,c,ob[i][0],ob[i][1])
        perp = geofenceband.perpendicularpt(start,end,ob[i])
        #print('bisector',perp)
        #print((displacement(start, perp) + displacement(end, perp)))
        if (geofenceband.displacement(start, perp) + geofenceband.displacement(end, perp)) > geofenceband.displacement(start, end):
            dist = 9999999
        #print('rasta',dist)
        #print('radi',ob[i][2])
        if dist <= ob[i][2]:
                return True
    return False

def estimate_path(bin_path,ob):
    # print(bin_path)
    # print("################################")
    # print("################################")
    # print("################################")

    
    # print('starting etmn')
    final_path = [bin_path[0]]
    end_waypoint= bin_path[-1]
    # print(final_path[0],"                ",end_waypoint)
    # print("################################")
    # print('LOOP STARTED')
    while final_path[-1] != bin_path[-1]:
        if not ifobs(final_path[-1], bin_path[-1],ob):
            # print("no obstacle")
            final_path.append(bin_path[-1])
            continue
        sliced_array = bin_path[bin_path.index(final_path[-1]):bin_path.index(end_waypoint)]
        # print(sliced_array)
        # print("length of the sliced array: ",len(sliced_array))
        # print("################################")

        mid_point = sliced_array[len(sliced_array)//2]
        # print("mid point of the sliced array is: ",mid_point)
        # print((len(bin_path[bin_path.index(final_path[-1]):bin_path.index(end_waypoint)])//2))
        # print('$%&#$^&',final_path[-1],'^^^',mid_point,' end ',end_waypoint)
        
        if ifobs(final_path[-1],mid_point,ob):
            # print("executing if")
            # print(final_path[-1],'lol',mid_point)
            end_waypoint = mid_point
            
        else:
            # print("executing else")
            final_path.append(mid_point)
            # print('sory no fuc u')
            end_waypoint = bin_path[-1]
        # print("iteration over")
        # print("################################")
        # print("################################")
        # print("################################")
        # print("################################")
        # print("################################")
        
    # print('finsih estm')
    return final_path
        


def gotopath(wp,ob,geo):
    path = []
    for i in range(len(wp)):
        if i == len(wp)-1:
            break

        start = wp[i]
        end = wp[i+1]
        # print('runing for', start,' ', end)
        # if ifobs(start, end, ob):

            # print('bhaiya astar')
        p = []
        if i+1 == len(wp):
            start = pathPlotting.Node(wp[i],None,0,0)
            end = pathPlotting.Node(wp[0],None,None,None)

        else:
            start = pathPlotting.Node(wp[i],None,0,0)
            end = pathPlotting.Node(wp[i+1],None,None,None) 

        final = pathPlotting.asli_astar(start, end,ob,geo)        
        # print(final.pos)
        j = final
        while j.parent != None:
            p.append(j.pos)
            j = j.parent
        # print('pp',p)
        p.append(wp[i])
        p.reverse()
        bin_path = p
        bin_path = estimate_path(bin_path,ob)
        # else:       
        #     # print('direct path founf')
        #     bin_path = [start,end]
        path.extend(bin_path)
        # print('sexy',path)
    return path

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
    # for i in range(len(wpc)):
    i = 0
    while True:
        # print("lalala")
        if i == len(wpc):
            return newP 
        for j in range(len(p)):
            if p[j] != wpc[i]:
                # print("if")
                a = [p[j][0],p[j][1],c[i][2]]
                newP.append(a)
            else:
                # print("else")
                a = [p[j][0],p[j][1],c[i][2]]
                newP.append(a)
                i+=1

def obsmerger(a,b):
    ob = []
    for i in range(len(a)):
        ob.append([a[i][0],a[i][1], b[i]])

    return ob

# cartesianObstacle, cartesianObstacleRadius = obstacleCheckList(imprtntpts.obstacleCartesian,imprtntpts.obstacleRadius)

# ob = obstacleMergeList(imprtntpts.obstacleCartesian,imprtntpts.obstacleRadius)
# for i in range(len(cartesianObstacle)):
    # ob.append([cartesianObstacle[i][0],cartesianObstacle[i][1], cartesianObstacleRadius[i]])

# generatedPath = gotopath(imprtntpts.waypointCartesian,ob,imprtntpts.geofenceCartesian)
# Path = removeDuplicate(generatedPath)
# path = addHeight(Path,imprtntpts.waypointCartesian,inputs.Waypoints)
# Waypoints = wayptCoor(path,grid.cellDimension,minCorner,maxCorner)

timeElapsed = startTime - time.time()

def jSonOutput(a):
    D = {}
    l = []
    d = {}

    for i in a:
        # d["latitude"] = i[0]
        # d["longitude"] = i[1]
        # d["altitude"] = i[2]
        l.append({"latitude":i[0] , "longitude":i[1], "altitude":i[2]})
        # d.clear()

    D["obstacleFreePath"] = l

    return D

def findPath(a,b,c,d,e,f,g):
    generatedPath = gotopath(a,b,c)
    Path = removeDuplicate(generatedPath)
    path = addHeight(Path,a,d)
    Waypoints = wayptCoor(path,e,f,g)

    return Waypoints

# waypointList = findPath(imprtntpts.waypointCartesian,ob,imprtntpts.geofenceCartesian,inputs.Waypoints,grid.cellDimension)

# waypointDictionary = jSonOutput(waypointList) 

# if __name__ == "__main__":
#     print(waypointList)
#     print("#######################################")
#     print(timeElapsed,"    seconds")
#     print("#######################################")
#     print("#######################################")
#     print(waypointDictionary)
