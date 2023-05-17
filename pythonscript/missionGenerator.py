import json
import os

if not os.path.exists("missionPlanner"):
    os.mkdir("missionPlanner")

def feetToMeter(x):
    x = x*0.3048
    return x 

def geofencePlotter(jsonData):
    file = open("missionPlanner/noFlyZone.waypoints","w")
    file.write('QGC' + ' ' + 'WPL' + ' ' + '110' + '\n')
    b = jsonData["flyZones"][0]
    p = 1
    h = jsonData["lostCommsPos"]
    hLat = h["latitude"]
    hLon = h["longitude"]
    file.write(str(0) + '\t' + str(1) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0)+ '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(hLat) + '\t' + str(hLon) + '\t' + str(0) + '\t' + str(1) + "\n")

    for i in b["boundaryPoints"]:
      size=len(b["boundaryPoints"])-1     
      file.write(str(p) + '\t' + str(0) + '\t' + str(3) + '\t' + str(5001) + '\t' + str(size) + ".00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + str(i["latitude"]) + '\t' + str(i["longitude"]) + '\t' + str(p-1) + ".00000000" + '\t' + str(1) + "\n")
      p = p + 1
      
    file.close()
    obstaclePlotter(p, jsonData)
    
def obstaclePlotter(count, jsonData):
    file = open("missionPlanner/noFlyZone.waypoints","a")
    b = jsonData["stationaryObstacles"]
    p = count
    # h = jsonData["lostCommsPos"]
    # hLa = h["latitude"]
    # hLon = h["longitude"]
    # file.write(str(0) + '\t' + str(1) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0)+ '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(hLat) + '\t' + str(hLon) + '\t' + str(0) + '\t' + str(1) + "\n")

    for i in b:
      size = feetToMeter(i["radius"]) + 5
      print(i["radius"], type(i["radius"]))
      file.write(str(p) + '\t' + str(0) + '\t' + str(3) + '\t' + str(5004) + '\t' + str(size) + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + str(i["latitude"]) + '\t' + str(i["longitude"]) + '\t' + str(0) + ".00000000" + '\t' + str(1) + "\n")
      p = p + 1 
      
    file.close()
    
def wpPlotter(jsonData):
    file = open("missionPlanner/wp.waypoints","w")
    file.write('QGC' + ' ' + 'WPL' + ' ' + '110' + '\n')
    b = jsonData["waypoints"]
    p = 1
    h = jsonData["lostCommsPos"]
    hLat = h["latitude"]
    hLon = h["longitude"]
    file.write(str(0) + '\t' + str(1) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0)+ '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(hLat) + '\t' + str(hLon) + '\t' + str(0) + '\t' + str(1) + "\n")

    for i in b:
      altitude = feetToMeter(i["altitude"] - 142)  ## msl in feet
      file.write(str(p) + '\t' + str(0) + '\t' + str(3) + '\t' + str(16) + '\t' + str(0)+".00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + str(i["latitude"]) + '\t' + str(i["longitude"]) + '\t' + str(altitude) + '\t' + str(1) + "\n")
      p = p + 1
      
    file.close()
    
def gridPlotter(jsonData, gridPoints):
    file = open("missionPlanner/odlc.waypoints","w")
    file.write('QGC' + ' ' + 'WPL' + ' ' + '110' + '\n')
    b = gridPoints["obstacleFreePath"]
    p = 1
    h = jsonData["lostCommsPos"]
    hLat = h["latitude"]
    hLon = h["longitude"]
    file.write(str(0) + '\t' + str(1) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0)+ '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(hLat) + '\t' + str(hLon) + '\t' + str(0) + '\t' + str(1) + "\n")

    for i in b:
      altitude = i["altitude"] #feetToMeter(i["altitude"])
      file.write(str(p) + '\t' + str(0) + '\t' + str(3) + '\t' + str(16) + '\t' + str(0)+".00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + str(i["latitude"]) + '\t' + str(i["longitude"]) + '\t' + str(altitude) + '\t' + str(1) + "\n")
      p = p + 1
      
    file.close()
      
def mapPlotter(jsonData, gridPoints):
    file = open("missionPlanner/map.waypoints","w")
    file.write('QGC' + ' ' + 'WPL' + ' ' + '110' + '\n')
    b = gridPoints["obstacleFreePath"]
    p = 1
    h = jsonData["lostCommsPos"]
    hLat = h["latitude"]
    hLon = h["longitude"]
    file.write(str(0) + '\t' + str(1) + '\t' + str(0) + '\t' + str(16) + '\t' + str(0)+ '\t' + str(0) + '\t' + str(0) + '\t' + str(0) + '\t' + str(hLat) + '\t' + str(hLon) + '\t' + str(0) + '\t' + str(1) + "\n")

    for i in b:
      altitude = i["altitude"] #feetToMeter(i["altitude"])
      file.write(str(p) + '\t' + str(0) + '\t' + str(3) + '\t' + str(16) + '\t' + str(0)+".00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + "0.00000000" + '\t' + str(i["latitude"]) + '\t' + str(i["longitude"]) + '\t' + str(altitude) + '\t' + str(1) + "\n")
      p = p + 1
      
    file.close()

def jSonOutput(a):
    D = {}
    D["obstacleFreePath"] = a
    return D
   
def readMission():
    odlcDict = []
    odlcList = []
    wpDict = []
    wpList = []
    mapDict = []
    mapList = []
    with open('missionPlanner/oaOdlc.waypoints') as f:
        lines = f.readlines()
        for line in lines[1:]:
            boom = {}
            newLine = line.split('\t')
            lat = newLine[8:9]
            lon = newLine[9:10]
            alt = newLine[10:11]
            boom["latitude"] = lat[0]
            boom["longitude"] = lon[0]
            boom["altitude"] = alt[0]
            odlcDict.append(boom)
            lat[0] = float(lat[0])
            lon[0] = float(lon[0])
            alt[0] = float(alt[0])
            odlcList.append([lat[0], lon[0], alt[0]])
            # print(lat[0],lon[0],alt[0])
    
    with open('missionPlanner/oaWp.waypoints') as f:
        lines = f.readlines()
        for line in lines[1:]:
            boom = {}
            newLine = line.split('\t')
            lat = newLine[8:9]
            lon = newLine[9:10]
            alt = newLine[10:11]
            boom["latitude"] = lat[0]
            boom["longitude"] = lon[0]
            boom["altitude"] = alt[0]
            wpDict.append(boom)
            lat[0] = float(lat[0])
            lon[0] = float(lon[0])
            alt[0] = float(alt[0])
            wpList.append([lat[0], lon[0], alt[0]])
            # print(lat[0],lon[0],alt[0])
            
    with open('missionPlanner/oaMap.waypoints') as f:
        lines = f.readlines()
        for line in lines[1:]:
            boom = {}
            newLine = line.split('\t')
            lat = newLine[8:9]
            lon = newLine[9:10]
            alt = newLine[10:11]
            boom["latitude"] = lat[0]
            boom["longitude"] = lon[0]
            boom["altitude"] = alt[0]
            mapDict.append(boom)
            lat[0] = float(lat[0])
            lon[0] = float(lon[0])
            alt[0] = float(alt[0])
            mapList.append([lat[0], lon[0], alt[0]])
            # print(lat[0],lon[0],alt[0])


    return jSonOutput(odlcDict), odlcList, jSonOutput(wpDict), wpList, jSonOutput(mapDict), mapList
    
    
    
      
# def driver():
#     file = open("fenceV1.waypoints","w")
#     file.write('QGC' + ' ' + 'WPL' + ' ' + '110' + '\n')
#     # file.write('#saved by APM Planner 1.3.74'+'\n')
#     geofenceList(jsonData)
#     file.close()