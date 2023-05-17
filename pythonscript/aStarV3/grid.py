import geopy
import geopy.distance
from geopy.distance import great_circle
import math

def cornerCoordinates(a):
    lat=[]
    lon=[]
    for i in a:
        lat.append(i[0])
        lon.append(i[1])

    x1 = min(lat)
    y1 = min(lon)
    x2 = max(lat)
    y2 = max(lon)

    m = (x1,y1)
    n = (x2,y2)

    return m,n

def makeBoundary(a,b):        
    latitude1 = [a[0],0]
    latitude2 = [b[0],0]     
    avg = (a[0] + b[0])/2
    longitude1 = [avg,a[1]]
    longitude2 = [avg,b[1]]
    l = (great_circle(latitude1,latitude2).m)
    w = (great_circle(longitude1,longitude2).m)

    return l,w

def getDimensions(cd,l,w):
    r = l/cd
    c = w/cd
    if l%cd < cd/2:
        r=math.floor(r)
    else:
        r=math.ceil(r)
    if w%cd < cd/2:
        c=math.floor(c)
    else:
        c=math.ceil(c)

    return r,c