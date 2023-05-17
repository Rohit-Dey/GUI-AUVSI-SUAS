import math
from aStarV2 import geofenceband


def getNeighbours(cell):
    neighbour_cord = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]
    currX=cell.pos[0]
    currY=cell.pos[1]
    n = []

    for i in neighbour_cord:
        x = currX + i[0]
        y = currY + i[1]

        if x < 0 or y < 0:
            continue
        n.append(Node((x,y),cell,None,None))

    return n


def dictionarySort(dict1):
    sortedVal = sorted(dict1.values())
    sortedDict = {}
    for i in sortedVal:
        for k in dict1.keys():
            if dict1[k] == i:
                sortedDict[k] = dict1[k]
                break

    return sortedDict

def calculateDistance(a,b,o):
    x1=o[0]
    y1=o[1]
    x2=a[0]
    y2=a[1]
    x3=b[0]
    y3=b[1]
    L = (x3-x2)*y1 - (y3-y2)*x1 + (y3-y2)*x2 - (x3-x2)*y2
    p = math.sqrt((y3-y2)**2 + (x3-x2)**2)
    if p != 0:
        d = ((x3-x2)*y1 - (y3-y2)*x1 + (y3-y2)*x2 - (x3-x2)*y2)/p
    else:
        d = ((x3-x2)*y1 - (y3-y2)*x1 + (y3-y2)*x2 - (x3-x2)*y2)/0.00000000000000001
    if d < 0:
        d=d*(-1)

    return d

class Node():
    def __init__(self,pos,parent,pathcost,f):
        self.pos = pos
        self.parent = parent
        self.pathcost = pathcost
        self.f = f

def asli_astar(st, ed, obs, geo):
    p=[]
    # st = (x,y) 0, None
    openl = {st:0}
    closedl = {}
    while openl:
        #finding minimum f
        openl = dictionarySort(openl)
        #popping minimum f
        q = [list(openl.keys())[0], None]
        q[1] = openl.pop(list(openl.keys())[0])
        #generating bhailog
        # print(q[0].f)
        # print("neighbours")
        nb = getNeighbours(q[0])
        for n in nb:
            # print(n.pos)
            #checking if reached goal
            if n.pos == ed.pos:
                # print(n.pos)
                # p.append(n.pos)
                return n

            #calc path cost heur and f
            n.pathcost = n.parent.pathcost + ((n.pos[0]-n.parent.pos[0])**2 + (n.pos[1]-n.parent.pos[1])**2)**0.5
            heur = ((n.pos[0]-ed.pos[0])**2 + (n.pos[1]-ed.pos[1])**2)**0.5
            # print(obs)

            for o in range(len(obs)):
                # print(obs[o])
                # print("obstacle",obs[o][2])
                ox = obs[o][0]
                oy = obs[o][1]
                radiuscheck = ((ox-n.pos[0])**2 + (oy-n.pos[1])**2)**0.5
                # print("dist",radiuscheck)
                if radiuscheck <= (obs[o][2]+3):
                    # print("if")
                    heur = 9999999999
                    break

                # print("iteration over")
            # print(len(geo))
            for g in range(len(geo)):
                if g+1 == len(geo):
                    p1 = geo[g]
                    p2 = geo[0]
                else:
                    p1 = geo[g]
                    p2 = geo[g+1]

                geocheck = geofenceband.geoband(n.pos,p1,p2)   
                if geocheck == False:  
                    # print("hit geofence","      ")  
                    heur = 9999999999999999
                    break

            n.f = n.pathcost + heur
            # print(n.f)
            flag = True
            #op checks
            for i in openl:
                if (i.pos == n.pos) & (i.f < n.f):
                    flag = False

            # print(flag)
            for i in closedl:
                if (i.pos == n.pos) & (i.f < n.f):
                    flag = False
            # print(flag)
            
            if flag:
                openl[n] = n.f
        
        closedl[q[0]]= q[0].f
        # print(closedl)

    # p.append(st)
    # p.reverse
    
    # return p
        

if __name__ == "__main__":
    import numpy
    start = Node((0,0),None,0,0)
    end = Node((10,10),None,None,None)
    final = asli_astar(start, end,[[5,5,1]],[(-20,-20),(20,-20),(20,20),(-20,20)])
    
    # print(final)


    i = final 
    path = []
    while i.parent != None:
        path.append(i.pos)
        i = i.parent
    path.append((0,0))
    path.reverse()
    print(path)

    a = numpy.zeros((15,15))
    for i in path:
        a[i[0]][i[1]] = 1

    # print(a)
