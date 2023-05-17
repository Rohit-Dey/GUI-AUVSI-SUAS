import base64
import json
from logging import exception
import multiprocessing
from tkinter.tix import Tree
from urllib import response
from auvsi_suas.client.client import Client, AsyncClient
from auvsi_suas.proto import interop_api_pb2
import os
from missionGenerator import geofencePlotter, gridPlotter, mapPlotter, readMission, wpPlotter
import socketio
import threading
import time
import socket
from google.protobuf import json_format
from gcsApi import fetchFromLocalDb, updateDb, updateEmergentDb
from tools.mavlink_proxy import MavlinkProxy
from pymavlink import mavutil
import dronekit as dk
from aStarV3.inputs import plannedPath
from aStarV2.inputs import geofenceList, obstaclelist, plannedPath as aStar2
from gridPointGenerator import mapping_WP, ODLC_grid
from datetime import datetime
from shapely.geometry import LineString
from shapely.geometry import Point
creation = str(datetime.now())
# from json import JSONEncoder

live = True

if live:
    client = Client(url='http://10.10.130.10:80',
                        username='dehli-technological-university',
                        password='8255874853')

    async_client = AsyncClient(url='http://10.10.130.10:80',
                        username='dehli-technological-university',
                        password='8255874853')

else:
    client = Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

    async_client = AsyncClient(url='http://127.0.0.1:8000',
                        username='testuser',
                        password='testpass')

client_service = 0 # 0: AsyncClient 1: Client
jetsonMission = {}
task = []
global sio
sio = socketio.Client()
global telemStarted, vehicle, telem_to_interop, telem_to_react, vehicleJson, globalVehicleJson, globalMissionId
globalMissionId = 1
telemStarted = False
vehicleJson = False
globalVehicleJson = "No Telem"

swarm_send_ip = "192.168.0.103"  ###### Jetson Ip
#swarm_send_ip = "127.0.0.1"
swarm_send_port = 10005
swarm_pause_port = 10003
swarm_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
swarm_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# teams = client.get_teams()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    sio.disconnect()
    print('disconnected from server')

@sio.event
def joined(data):
    print(data)
    

@sio.event
def sendtopython(data):
    print(data)

@sio.event
def sendtoteamreact(data):
    if client_service:
        teams = client.get_teams()
    else:
        teams = async_client.get_teams().result()
    teams_en = json_format.MessageToJson(teams)
    sio.emit('messagetoreact',json.loads(teams_en))

#@sio.event
def telemToInterop(device):
    device =  device.split(":")
    port = int(device[1]) + 1
    device = device[0] + ':' + str(port)
    print("Interop Device", device)
    #def sendTelem(device):
    if not client_service:
        proxy = MavlinkProxy(device, async_client)
        proxy.proxy()
    else:
        print("Error in Client")
    #telem_to_interop = threading.Thread(target = sendTelem, args=(device,))
    #telem_to_interop.start()
    print("Telem Transmission Started")

@sio.event
def controlUavTelem(device):
    global telemStarted, telem_to_interop, telem_to_react, vehicle
    if device == None or device == False or device == "STOP":
        print("Paused")
        sio.emit("uavTelem", "Paused")
        telemStarted = False
        try:
            vehicle.close()
            print("Stopping")
            telem_to_interop.terminate()
            telem_to_react.join()
        except:
            pass
        #if telemStarted:
    else:
        telem_to_interop = multiprocessing.Process(target = telemToInterop, args=(device,))
        telem_to_react = threading.Thread(target = telemToReact, args=(device,))
        telemStarted = True
        telem_to_react.start()
        telem_to_interop.start()

#@sio.event
def telemToReact(device = None):
    global telemStarted, vehicle, sio, globalVehicleJson
    connectedOnce = False
    while True:
        if device == None or device == False or device == "STOP" or telemStarted == False:
            print("Paused")
            sio.emit("uavTelem", "Paused")
            break
        else:
            try:
                if not connectedOnce:
                    print("Connecting")
                    vehicle = dk.connect(device)
                    print("Connected")
                    connectedOnce = True
                mav = vehicle.location.global_relative_frame
                mav2 = vehicle.location.global_frame
                vehicleJson = {
                    "uavLat" : mav.lat,
                    "uavLon" : mav.lon,
                    "uavAlt" : mav.alt,
                    "uavMslAlt": mav2.alt,
                    "uavHeading" : vehicle.heading,
                    "uavMode" : vehicle.mode.name,
                    "uavSpeed" : vehicle.airspeed,
                    "uavArmed" : vehicle.armed,
                    "uavBattery" : {
                        "voltage" : vehicle.battery.voltage,
                        "current" : vehicle.battery.current
                    }
                }
                #print(sio)
                sio.emit("uavTelem", vehicleJson)
                globalVehicleJson = vehicleJson
                time.sleep(0.2)
            except Exception as err:
                print("Error (telemToReact): ", err)
                #sio.emit("uavTelem", globalVehicleJson)  
                time.sleep(1)
                pass

@sio.event
def uploadMap(reactsCombinedData = None):
    reactsCombinedData = reactsCombinedData.split('base64,')
    imgFolder = "/home/" + os.getlogin() + "/stichedSentMapping/"
    if not os.path.exists(imgFolder):
        os.mkdir(imgFolder)
    img_path = imgFolder + str("gcsMap") + ".jpg" 
    with open(img_path ,"wb") as Imagefile:
            Imagefile.write(base64.decodebytes(bytes(reactsCombinedData[1], 'utf-8')))
    print("Image saved at: ", img_path)
    print("Mission: ", globalMissionId)
    missionId = globalMissionId #data[0]
    uploadMapApi(missionId, img_path)
    downloadMap(missionId)

def uploadMapApi(mission_id = globalMissionId, image = None):
    mission_id = int(mission_id)
    if os.path.exists(image):
        with open(image, 'rb') as stichedMap:
            mapData = stichedMap.read()
        if client_service:
            client.put_map_image(mission_id, mapData)
        else:
            async_client.put_map_image(mission_id, mapData).result()
        print("Uploaded Successfully")
        sio.emit('mapUploadStatus',"Success")
    else:
        print("No image found")
        sio.emit('mapUploadStatus',"Error")

def downloadMap(mission_id):
    mission_id = int(mission_id)
    if client_service:
        stichedMap = client.get_map_image(mission_id)
    else:
        stichedMap = async_client.get_map_image(mission_id).result()
    mapFolder = "/home/" + os.getlogin() + "/Interop_Map/" 
    if not os.path.exists(mapFolder):
        os.mkdir(mapFolder)
    map_path = mapFolder + str(mission_id) + ".jpg"
    with open(map_path ,"wb") as Imagefile:
            Imagefile.write(stichedMap)
    print("Map saved at: ", map_path)

def enumerator(Odlc_Input = None):
    Odlc_Input = Odlc_Input.upper()
    if Odlc_Input == 'STANDARD':
        return interop_api_pb2.Odlc.STANDARD
    if Odlc_Input == 'EMERGENT':
        return interop_api_pb2.Odlc.EMERGENT
    if Odlc_Input == 'CIRCLE':
        return interop_api_pb2.Odlc.CIRCLE
    if Odlc_Input == 'SEMICIRCLE':
        return interop_api_pb2.Odlc.SEMICIRCLE
    if Odlc_Input == 'QUARTER_CIRCLE':
        return interop_api_pb2.Odlc.QUARTER_CIRCLE
    if Odlc_Input == 'TRIANGLE':
        return interop_api_pb2.Odlc.TRIANGLE
    if Odlc_Input == 'SQUARE':
        return interop_api_pb2.Odlc.SQUARE
    if Odlc_Input == 'RECTANGLE':
        return interop_api_pb2.Odlc.RECTANGLE
    if Odlc_Input == 'TRAPEZOID':
        return interop_api_pb2.Odlc.TRAPEZOID
    if Odlc_Input == 'PENTAGON':
        return interop_api_pb2.Odlc.PENTAGON
    if Odlc_Input == 'HEXAGON':
        return interop_api_pb2.Odlc.HEXAGON
    if Odlc_Input == 'HEPTAGON':
        return interop_api_pb2.Odlc.HEPTAGON
    if Odlc_Input == 'OCTAGON':
        return interop_api_pb2.Odlc.OCTAGON
    if Odlc_Input == 'STAR':
        return interop_api_pb2.Odlc.STAR
    if Odlc_Input == 'CROSS':
        return interop_api_pb2.Odlc.CROSS
    if Odlc_Input == 'N':
        return interop_api_pb2.Odlc.N
    if Odlc_Input == 'NE':
        return interop_api_pb2.Odlc.NE
    if Odlc_Input == 'E':
        return interop_api_pb2.Odlc.E
    if Odlc_Input == 'SE':
        return interop_api_pb2.Odlc.SE
    if Odlc_Input == 'S':
        return interop_api_pb2.Odlc.S
    if Odlc_Input == 'SW':
        return interop_api_pb2.Odlc.SW
    if Odlc_Input == 'W':
        return interop_api_pb2.Odlc.W
    if Odlc_Input == 'NW':
        return interop_api_pb2.Odlc.NW
    if Odlc_Input == 'WHITE':
        return interop_api_pb2.Odlc.WHITE
    if Odlc_Input == 'BLACK':
        return interop_api_pb2.Odlc.BLACK
    if Odlc_Input == 'GRAY':
        return interop_api_pb2.Odlc.GRAY
    if Odlc_Input == 'RED':
        return interop_api_pb2.Odlc.RED
    if Odlc_Input == 'BLUE':
        return interop_api_pb2.Odlc.BLUE
    if Odlc_Input == 'GREEN':
        return interop_api_pb2.Odlc.GREEN
    if Odlc_Input == 'YELLOW':
        return interop_api_pb2.Odlc.YELLOW
    if Odlc_Input == 'PURPLE':
        return interop_api_pb2.Odlc.PURPLE
    if Odlc_Input == 'BROWN':
        return interop_api_pb2.Odlc.BROWN
    if Odlc_Input == 'ORANGE':
        return interop_api_pb2.Odlc.ORANGE

@sio.event
def deleteFromDb(response = None):
    try:
        odlcId = response['odlcid']
        delete_odlc(odlcId)
    except Exception as err:
        print("Error (deleteFromDb): ", err)
        pass
    
@sio.event
def addToDb(response = None):
    imgChunk, json = fetchFromLocalDb(response['fileid'])
    # print(json)
    # upload_odlc(odlcJson=json, odlcImageChunk=imgChunk)
    imgFolder = "/home/" + os.getlogin() + "/newOdlctoAdd/"
    if not os.path.exists(imgFolder):
        os.mkdir(imgFolder)
    img_path = imgFolder + str(response['fileid']) + ".jpg" 
    with open(img_path ,"wb") as Imagefile:
            Imagefile.write(base64.decodebytes(imgChunk))
    print("Image saved at: ", img_path)
    odlcId = upload_odlc(odlcJson = json, odlcImage = img_path, isAutonomous = False)
    # print("@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(get_odlc(odlcId))
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    try:
        if json["Type"] == "STANDARD":
            updatedJson = get_odlc(odlcId)
            updatedJson = updatedJson[0]
            updateDb(updatedJson, response['fileid'])
        else:
            updatedJson = get_odlc(odlcId)
            updateEmergentDb(updatedJson[0].id, updatedJson[0].description, response['fileid'])
    except Exception as err:
        print(get_odlc(odlcId))
        print("Error (addToDb): ", err)
        pass
    

def upload_odlc(odlcJson = None, odlcImage = None, odlcImageChunk = None, isAutonomous = True):
    odlc = interop_api_pb2.Odlc()
    odlc.mission = globalMissionId
    odlc.type = enumerator(odlcJson["Type"])                                          #interop_api_pb2.Odlc.STANDARD
    if odlcJson["Type"] == "EMERGENT":
        odlc.description = odlcJson["Description"]
    else:
        odlc.latitude = float(odlcJson["Latitude"])                                  #38
        odlc.longitude = float(odlcJson["Longitude"])                                #-76
        odlc.orientation = enumerator(odlcJson["Orientation"].upper())                #interop_api_pb2.Odlc.N
        odlc.shape = enumerator(odlcJson["Shape"])                            #interop_api_pb2.Odlc.STAR
        odlc.shape_color = enumerator(odlcJson["Shape_Color"])                #interop_api_pb2.Odlc.RED
        odlc.alphanumeric = odlcJson["Alphanumeric"].upper()                          #'A'
        odlc.alphanumeric_color = enumerator(odlcJson["Alphanumeric_Color"])  #interop_api_pb2.Odlc.WHITE
    #print(odlc.autonomous)
    odlc.autonomous = isAutonomous # Decide To keep or Not
    #print(odlc.shape)     
    if client_service:
        odlc = client.post_odlc(odlc)
    else:
        odlc = async_client.post_odlc(odlc).result()
    print(odlc.id)

    if odlcImageChunk == None:
        print("in If")
        with open(odlcImage, 'rb') as f:
            image_data = f.read()
    else:
        print("in else")
        image_data = bytes(odlcImageChunk, 'utf-8')

    if client_service:
        client.put_odlc_image(odlc.id, image_data)
    else:
        async_client.put_odlc_image(odlc.id, image_data).result()
    return odlc.id

@sio.event
def dbUpdated(updatedJson):
    try:
        json = updatedJson['xodlc']
        update_odlc(odlc_id = json['Odlcid'], odlcJson = json, isAutonomous = False)
    except Exception as err:
        print("Error (dbUpdated): ", err)
        pass

def update_odlc(odlc_id = None, odlcJson = None, odlcImage = None, isAutonomous = True):
    odlc = interop_api_pb2.Odlc()
    odlc.mission = globalMissionId
    odlc.type = enumerator(odlcJson["Type"])                                          #interop_api_pb2.Odlc.STANDARD
    if odlcJson["Type"] == "EMERGENT":
        odlc.description = odlcJson["Description"]
    else:
        odlc.latitude = float(odlcJson["Latitude"])                                  #38
        odlc.longitude = float(odlcJson["Longitude"])                                #-76
        odlc.orientation = enumerator(odlcJson["Orientation"])                #interop_api_pb2.Odlc.N
        odlc.shape = enumerator(odlcJson["Shape"])                            #interop_api_pb2.Odlc.STAR
        odlc.shape_color = enumerator(odlcJson["Shape_Color"])                #interop_api_pb2.Odlc.RED
        odlc.alphanumeric = odlcJson["Alphanumeric"]                          #'A'
        odlc.alphanumeric_color = enumerator(odlcJson["Alphanumeric_Color"])  #interop_api_pb2.Odlc.WHITE
    odlc.autonomous = isAutonomous     # Decide To keep or Not
    if client_service:
        updateOdlc = client.put_odlc(odlc_id, odlc)
    else:
        updateOdlc = async_client.put_odlc(odlc_id, odlc).result()
    print(updateOdlc.id)

    if odlcImage != None:
        with open(odlcImage, 'rb') as f:
            image_data = f.read()
            if client_service:
                client.put_odlc_image(odlc_id, image_data)
            else:
                async_client.put_odlc_image(odlc_id, image_data).result()

def get_odlc(odlc_id = None):
    odlc_id = int(odlc_id)
    if client_service:
        odlc_json = client.get_odlc(odlc_id)
        odlc_image = client.get_odlc_image(odlc_id)
    else:
        odlc_json = async_client.get_odlc(odlc_id).result()
        odlc_image = async_client.get_odlc_image(odlc_id).result()

    # print(odlc_image, type(odlc_image))
    imgFolder = "/home/" + os.getlogin() + "/recvOdlcFromInterop/"
    if not os.path.exists(imgFolder):
        os.mkdir(imgFolder)
    img_path = imgFolder + str(odlc_id) + ".jpg" 
    with open(img_path ,"wb") as Imagefile:
            Imagefile.write(odlc_image)
    #print("Image Saved at ",img_path)
    return odlc_json, img_path

def delete_odlc(odlc_id = None, only_odlc_image = 0):  # 1: Deletes Image Only ,  0: Deletes Both Image and JSON
    odlc_id = int(odlc_id)
    if client_service:
        print("Not Async")
        if only_odlc_image:
            print("Image Deleted")
            client.delete_odlc_image(odlc_id)
        else:
            print("Image and JSON Deleted")
            client.delete_odlc(odlc_id)
    else:
        print("Async")
        if only_odlc_image:
            print("Image Deleted")
            async_client.delete_odlc_image(odlc_id).result()
        else:
            print("Image and JSON Deleted")
            async_client.delete_odlc(odlc_id).result()


@sio.event
def fetchMission(mission_id):
    global globalMissionId
    D = {}
    mission_id = int(mission_id)
    globalMissionId = int(mission_id)
    print("Fetching Mission ID: ", mission_id, "Global Mission ID: ", globalMissionId)
    if client_service:
        mission = client.get_mission(mission_id)
    else:
        mission = async_client.get_mission(mission_id).result()
    strMission = json_format.MessageToJson(mission)
    jsonMission = json.loads(strMission)
    missionFile = json.dumps(jsonMission, indent = 4).encode('utf-8')
    missionFolder = "/home/" + os.getlogin() + "/Interop_Mission/"
    if not os.path.exists(missionFolder):
        os.mkdir(missionFolder)
    missionPath = missionFolder + str(mission_id) + ".json" 
    with open(missionPath, 'wb') as missionJson:
        missionJson.write(missionFile)
    # print("Mission Saved at: ", missionPath)
    sio.emit('interopMission', jsonMission)
    # print(type(json.loads(strMission)))
    geofencePlotter(jsonMission)
    wpPlotter(jsonMission)
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
    D["obstacleFreePath"] = jsonMission["waypoints"]
    modifiedWaypointsDict = D
    # modifiedWaypointsList, modifiedWaypointsDict = plannedPath(jsonMission)
    # jetsonMission["WAYPOINT"] = modifiedWaypointsList
    jetsonMission["OFF_AXIS"] = [["Nearby Lat", "Nearby Lon", 25],[jsonMission["offAxisOdlcPos"]["latitude"], jsonMission["offAxisOdlcPos"]["longitude"]]]
    jetsonMission["EMERGENT"] = [jsonMission["emergentLastKnownPos"]["latitude"], jsonMission["emergentLastKnownPos"]["longitude"], 25]
    jetsonMission["DROP"] = [jsonMission["airDropPos"]["latitude"], jsonMission["airDropPos"]["longitude"], 25]
    missionJsonMaker(mission_id)
    # sio.emit('autoPath', modifiedWaypointsDict)
    # print(type(modifiedWaypointsDict))
    missionMakerThread = threading.Thread(target = missionMaker, args = (jsonMission, mission_id, modifiedWaypointsDict,))
    missionMakerThread.start()

def missionMaker(mission, mission_id, modifiedWaypointsDict):
    ###################################### ODLC #########################################################################
    searchWpList, searchWpDict = ODLC_grid.finalODLCWaypoints(mission["searchGridPoints"], 25)  ## Altitude in meters
    gridPlotter(mission, searchWpDict)
    print("ODLC Grid Coordinates Generated")
    print("Generating Obstacle free ODLC path....")
    # searchWpList, searchWpDict = aStar2(mission, searchWpList)   ##Obstacle free path for ODLC (comment if don't want to avoid obstacle in ODLC)
    jetsonMission["ODLC"] = searchWpList
    missionJsonMaker(mission_id)
    print("autoSearchWpList")
    # sio.emit("autoSearchWp", searchWpDict)
    ###################################### MAPPING #########################################################################
    mappingWpList, mappingWpDict = mapping_WP.finalMappingWaypoints(mission["mapHeight"], mission["mapCenterPos"]["latitude"], mission["mapCenterPos"]["longitude"], obstaclelist(mission), 100) ## Altitude in meters
    print("Mapping Grid Coordinates Generated")
    mapPlotter(mission, mappingWpDict)
    #print("Generating Obstacle free map path....")
    # mappingWpList, mappingWpDict, initialWp, finalWp = saruAvoidance(mappingWpList, mappingWpDict, mission)
    # print(initialWp)
    # print("$")
    # print(finalWp)
    # print("$")
    # print(geofenceList(mission))
    # print("$")
    # print(ODLC_grid.stayInPolygon(initialWp, finalWp, geofenceList(mission)))
    # print("#################################")
    # print(mappingWpDict)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # mappingWpList, mappingWpDict = plannedPath(mission, mappingWpList)  ##Obstacle free path for mapping ( comment if don't want to avoid obstacle in Mapping)
    jetsonMission["MAP"] = mappingWpList
    missionJsonMaker(mission_id)
    print("Boom done")
    sio.emit('autoPath', modifiedWaypointsDict)
    sio.emit("autoSearchWp", searchWpDict)
    sio.emit("mappingWp", mappingWpDict)
    # editedMission(mission_id)
    
def editedMission(mission_id):
    odlcDict, odlcList, wpDict, wpList, mapDict, mapList = readMission()
    sio.emit('autoPath', wpDict)
    time.sleep(2)
    sio.emit("autoSearchWp", odlcDict)
    time.sleep(2)
    sio.emit("mappingWp", mapDict)
    time.sleep(2)
    jetsonMission["WAYPOINT"] = wpList
    jetsonMission["ODLC"] = odlcList
    jetsonMission["MAP"] = mapList
    print(odlcList)
    print("@@")
    missionJsonMaker(mission_id)
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
def missionJsonMaker(mission_id):
    missionFolder = "/home/" + os.getlogin() + "/Interop_Mission/"
    missionPath = missionFolder + "jetsonMission_" + str(mission_id) + ".json" 
    with open(missionPath, 'wb') as missionJson:
        missionJson.write(json.dumps(jetsonMission, indent = 4).encode('utf-8'))

@sio.event
def sendTask(taskString, mission_id = globalMissionId):
    print(mission_id, globalMissionId)
    print("Executing: ", taskString)
    try:
        currentUavLocation = [globalVehicleJson["uavLat"], globalVehicleJson["uavLon"], globalVehicleJson["uavAlt"]]
        print(currentUavLocation)

        missionFolder = "/home/" + os.getlogin() + "/Interop_Mission/"
        missionPath = missionFolder + "jetsonMission_" + str(mission_id) + ".json"
        with open(missionPath, 'rb') as missionJson:
            missionMakerJson = json.load(missionJson)

        missionPath = missionFolder + str(mission_id) + ".json"
        with open(missionPath, 'rb') as missionJson:
            interopJson = json.load(missionJson)

        if taskString == "startWaypoints":
            taskType = "WAYPOINT"
        elif taskString == "startOdlc":
            taskType = "ODLC"
        elif taskString == "startMapping":
            taskType = "MAP"
        elif taskString == "startOffAxis":
            taskType = "OFF_AXIS"
        elif taskString == "startEmergent":
            taskType = "EMERGENT"
        elif taskString == "startGotoDrop":
            taskType = "DROP"

        if taskType == "DROP" or taskType == "EMERGENT":
            taskWp = [currentUavLocation, [missionMakerJson[taskType][0], missionMakerJson[taskType][1], missionMakerJson[taskType][2]]]
        else:
            taskWp = [currentUavLocation, [missionMakerJson[taskType][0][0], missionMakerJson[taskType][0][1], missionMakerJson[taskType][0][2]]]
        print("generating Path to task", taskWp)
        #pathToTaskList, pathToTaskDict = plannedPath(interopJson, taskWp)
        pathToTaskList = taskWp
        for i, val in enumerate(pathToTaskList):
            pathToTaskList[i] = [val[0], val[1], val[2], {"MAP": False, "ODLC": False}]
        task.append([taskType, pathToTaskList, (len(task) + 1)])

        missionPath = missionFolder + "jetsonTask_" + str(mission_id) + " " + creation + ".json"
        with open(missionPath, 'wb') as taskFile:
            taskFile.write(json.dumps(task, indent = 4).encode('utf-8'))

        sendTaskToJetson(task[-1])
    except Exception as err:
        print("Error (sendTask): ", err)
        pass

@sio.event
def sendCmd(command):
    if command == 'startUnlatchRover':
        print("Unlatching")
    elif command == 'startEngageBrake':
        print("Engaging Brake")
    elif command == 'startDropSequence':
        print("Starting Drop")
    elif command == 'incAlt':
        print("Increasing Altitude")
    elif command == 'Pause':
        print("Pausing")
        sendTaskToJetson("pause")
    elif command == 'Stop':
        print("Stop")
        sendTaskToJetson("stop")
        sendTaskToJetson("play")


def sendTaskToJetson(taskTosend):
    while True:
        send_to_swarmcontroller(swarm_send_sock, taskTosend)
        print("Sent", taskTosend)
        break
    print("Boom")
    #sio.emit("taskConfirmation", "Recieved")

def send_to_swarmcontroller(sock, dt):
    try:
        if dt == "pause" or dt == "stop":
            port = swarm_pause_port
            if dt == "stop":
                dt = "STOP"
            else:
                dt = True
        elif dt== "play":
            port = swarm_pause_port
            dt = False
        else:
            port = swarm_send_port

        app_json = json.dumps(dt, sort_keys=True).encode(
            "UTF-8"
        )  ###save data in json file in transformed format of base 8 - octal data
        sock.sendto(
            app_json, (swarm_send_ip, port)
        )  ###send data in UDP format to the given format
        # print("Data sent to swarm_code:-", swarm_send_port)
    except Exception as err:
        sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  ###ye bhi pata kar hi lo 1 baar
        print("Error in send to swarmcontroller", err)


def my_background_task():
    run_once = 0 
    mission = client.get_mission(1)
    missio = json_format.MessageToJson(mission)
    print(missio)
    print(type(missio))
    if run_once == 0:
        run_once = 1
    sio.emit('messagetoreact',json.loads(missio))

    
sio.connect('http://localhost:5000/')
print("Emmiting Data")
sio.emit('join_room', "Python's Room")
#######################################################
# my_background_task()
# f = open()
#uploadMap(1, '/home/uas-dtu/53.jpg')
#downloadMap(1)
#upload_odlc(json.load(open("/home/uas-dtu/Downloads/88.json")))
# delete_odlc(34, 0)  # 1: Deletes Image Only ,  0: Deletes Both Image and JSON
#get_odlc(25)
#update_odlc(25)
#telemToReact('127.0.0.1:14550')
#telemToInterop('127.0.0.1:14550')
# telem_to_interop = threading.Thread(target = telemToInterop, args=('127.0.0.1:14550',))
# telem_to_interop.start()
# fetchMission(1)
# telem_upd()
# msg = threading.Thread(target = my_background_task)
# msg = threading.Thread(target = getDataFromGcsClient)localhost
# sendTaskToJetson("pause")
# time.sleep(5)
# sendTaskToJetson("play")
# response = {}
# response['field'] = "628a11b9a925f705e9c9df82"
# addToDb(response)
# get_odlc(476)