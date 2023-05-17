from aStarV2 import pathPlotting
import math

def lines(p1, p2):
    a = (p1[1] - p2[1])
    b = (p2[0] - p1[0])
    c = (p1[0]*p2[1] - p2[0]*p1[1])
    return a, b, -c

def calcDist(o,a,b,c):
    x=(math.sqrt(a**2 + b**2))
    if x==0:
        x=0.000000000000000000000001
    d = ((a*(o[0]) + b*(o[1]) + c)/x)

    if d<0:
        d*=(-1)

    return d

def displacement(a,b):
    d = ((a[0]-b[0])**2 + (a[1]-b[1])**2)**(0.5)
    return d

def perpendicularpt(a,b,o):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    x3 = o[0]
    y3 = o[1]
    dx = x2 - x1
    dy = y2 - y1
    mag = math.sqrt(dx*dx + dy*dy)
    if mag == 0:
        mag =0.00000000000001
    dx /= mag
    dy /= mag

    Lambda = (dx * (x3 - x1)) + (dy * (y3 - y1))
    x4 = (dx * Lambda) + x1
    y4 = (dy * Lambda) + y1
    # k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)^2 + (x2-x1)^2)
    # x4 = x3 - k * (y2-y1)
    # y4 = y3 + k * (x2-x1)
    return (x4,y4)


def geoband(a,p1,p2):

    # A,B,C = lines(p1,p2)
    # dist = calcDist(a,A,B,C)
    # # print(dist)

    dist = pathPlotting.calculateDistance(p1,p2,a)
    perp = perpendicularpt(p1,p2,a)
    if (displacement(p1, perp) + displacement(p2, perp)) > displacement(p1, p2):
        dist = 999999

    if dist <= 3:
        return False
    else:
        return True
