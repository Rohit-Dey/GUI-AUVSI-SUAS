from aStarV3 import grid

def findCartesian(a,b,cd):
    i,j=grid.makeBoundary(a,b)
    k,l=grid.getDimensions(cd,i,j)
    coor=(k-1,l-1)

    return coor

def wayptCart(wp,b,cd):
    wpc=[]
    for i in range(len(wp)):
        a = (wp[i][0],wp[i][1])
        coor = findCartesian(b,a,cd)
        wpc.append(coor)
    
    return wpc

def obsCart(ob,cd,b):
    obCoor=[]
    for i in ob:
        a=(i[0],i[1])
        coor = findCartesian(b,a,cd)
        coorLst = list(coor)
        obCoor.append(coorLst)
    
        if i[2]%cd==0:
            coorLst.append((i[2]/cd))
        elif i[2]%cd!=0 and i[2]%cd<(cd/2):
            coorLst.append((i[2]//cd))
        else:
            coorLst.append(i[2]//cd+1)

    return obCoor

def geoCart(gf,b,cd):
    gfc=[]
    for i in gf:
        coor = findCartesian(b,i,cd)
        gfc.append(coor)
        
    return gfc