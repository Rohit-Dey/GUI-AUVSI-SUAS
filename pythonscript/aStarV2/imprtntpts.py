from aStarV2 import grid
# import inputs

def findCartesian(a,b):
    i,j=grid.makeBoundary(a,b)
    k,l=grid.getDimensions(grid.cellDimension,i,j)
    coor=(k-1,l-1)

    return coor

# def findCartesianL(a,b):
#     i,j=grid.makeBoundary(a,b)
#     k,l=grid.getDimensions(grid.cellDimension,i,j)
#     coor=[k-1,l-1]

#     return coor

def wayptCart(wp,b):
    wpc=[]
    for i in range(len(wp)):
        a = (wp[i][0],wp[i][1])
        coor = findCartesian(b,a)
        wpc.append(coor)
    
    return wpc

def obsCart(ob,cd,b):
    obCoor=[]
    obr=[]
    for i in ob:
        a=(i[0],i[1])
        coor = findCartesian(b,a)
        obCoor.append(coor)
    
        if i[2]%cd==0:
            obr.append((i[2]/cd))
        elif i[2]%cd!=0 and i[2]%cd<(cd/2):
            obr.append((i[2]//cd))
        else:
            obr.append(i[2]//cd+1)

    return obCoor, obr

def geoCart(gf,b):
    gfc=[]
    for i in gf:
        coor = findCartesian(b,i)
        gfc.append(coor)
       
    return gfc

# waypointCartesian = wayptCart(inputs.Waypoints,grid.minCorner)
# obstacleCartesian, obstacleRadius = obsCart(inputs.Obstacles,grid.cellDimension,grid.minCorner)
# geofenceCartesian = geoCart(inputs.inclusionGeofence,grid.minCorner)

# if __name__ == "__main__":
#     print(geofenceCartesian)
#     print(" ")
#     print("###########################################################")
#     print(" ")
#     print(waypointCartesian)
#     print(" ")
#     print("###########################################################")
#     print(" ")
#     print(obstacleCartesian)
#     print(" ")
#     print("###########################################################")
#     print(" ")
#     print(obstacleRadius)    
