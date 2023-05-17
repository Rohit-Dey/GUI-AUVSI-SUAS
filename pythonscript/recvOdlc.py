from http import client
from logging.config import listen
import socket			
import os
import threading
from api import upload_odlc, get_odlc
import json
import time
import requests
from gcsApi import uploadToLocalDbStandard
from google.protobuf import json_format

filesUploaded = []
uploadDbThread = []
incoming_data = []
fetchData = []
sendData = []

jetsonUsername = 'uas-dtu'
jetsonIp = '192.168.0.103'
jetsonOdlcFolderPath = '~/Desktop/VISION/ODLC/'
gcsOdlcFolder = '/home/' + os.getlogin() + '/interop_odlc/'
localDbUrl = "http://localhost:5000/api/file/upload"

if not os.path.exists(gcsOdlcFolder):
    os.mkdir(gcsOdlcFolder)
    print("Created Directory")

def sendDataToInterop(extractedFilename):
    filePath = gcsOdlcFolder
    while True:
        try:
            #print("Trying for ", extractedFilename)
            jsonData = filePath + extractedFilename + '.json'
            imgData = filePath + extractedFilename + '.jpg'
            if os.path.exists(jsonData) and os.path.exists(imgData):
                #if extractedFilename not in filesUploaded:
                odlcId = upload_odlc(json.load(open(jsonData)), imgData)
                print("Successful for ", extractedFilename, "with ID: ", odlcId)
                while True:
                    if odlcId:
                        dBThread = threading.Thread(target= sendToLocalDb, args=(odlcId,))
                        uploadDbThread.append(dBThread)
                        uploadDbThread[-1].start()
                        break
                    else:
                        continue
                #filesUploaded.append(extractedFilename)
                break
            else:
                remoteUsername = jetsonUsername
                remoteIp = jetsonIp
                if not os.path.exists(jsonData):
                    remotePath = jetsonOdlcFolderPath + extractedFilename + '.json'
                elif not os.path.exists(imgData):
                    remotePath = jetsonOdlcFolderPath + extractedFilename + '.jpg'
                destination = gcsOdlcFolder
                os.system('sshpass -p Aether scp "%s@%s:%s" "%s"' % (remoteUsername, remoteIp, remotePath, destination))
                print("Retrying for ", extractedFilename)
                continue
        except Exception as err:
            print("Error (interop): ", err)
            #exit(0)

def recvData(filename):
    try:
        remoteUsername = jetsonUsername
        remoteIp = jetsonIp
        remotePath = jetsonOdlcFolderPath + filename
        destination = gcsOdlcFolder
        os.system('sshpass -p Aether scp "%s@%s:%s" "%s"' % (remoteUsername, remoteIp, remotePath, destination))
        time.sleep(0.5)
        extractedName = filename.split('.')
        #print("Bitch: ", extractedName)
        # if extractedName not in filesUploaded:
        #     filesUploaded.append(extractedName)
        apiRequest = threading.Thread(target= sendDataToInterop, args=(extractedName[0],))
        sendData.append(apiRequest)
        sendData[-1].start()
            #time.sleep(1)
    except Exception as err:
        pass
        #print("Error (scp): ", err)

def sendToLocalDb(Odlcid):
    try:
        while True:
            jsonFromInterop, imgPathFromInterop = get_odlc(Odlcid)
            jsonFromInterop = json.loads(json_format.MessageToJson(jsonFromInterop))
            if jsonFromInterop and imgPathFromInterop:
                print(jsonFromInterop)
                print(imgPathFromInterop)
                imgName = str(Odlcid) + '.jpg'
                status = uploadToLocalDbStandard(jsonFromInterop, imgPathFromInterop, imgName)
                print(status)
                break
            else:
                print("Could Not Get Data from Interop")
                continue
    except Exception as err:
        print("Error (sendToLocalDB): ", err)
        pass


##################################################Main############################################################################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
while True:
    try:
        print("Trying to Connect")
        sock.connect((jetsonIp, 6969))
        print("Connected")
        while True:
            data = sock.recv(1024).decode()
            if data:
                data = data.split('n')
                if len(data) > 1:
                    data.pop()
                for i in data:
                    new_data = i.split('g')
                    new_data = new_data[0]
                    if new_data[-1] == 'o':
                        new_data = new_data + 'n'
                        #print(new_data)
                        incoming_data.append(new_data)
                        extractedName = new_data.split('.')
                        #print(extractedName[0])
                        if extractedName[0] not in filesUploaded:
                            filesUploaded.append(extractedName[0])
                            #print(filesUploaded)
                            scpFile = threading.Thread(target= recvData, args=(new_data,))
                            fetchData.append(scpFile)
                            fetchData[-1].start()
                    elif new_data[-1] == 'p':
                        new_data = new_data + 'g'
                        #print(new_data)
                        incoming_data.append(new_data)
                        extractedName = new_data.split('.')
                        #print(extractedName[0])
                        if extractedName[0] not in filesUploaded:
                            filesUploaded.append(extractedName[0])
                            #print(filesUploaded)
                            scpFile = threading.Thread(target= recvData, args=(new_data,))
                            fetchData.append(scpFile)
                            fetchData[-1].start()
                #print(incoming_data)
                #incoming_data.append(data)
                print(filesUploaded)
                # scpFile = threading.Thread(target= recvData, args=(data,))
                # fetchData.append(scpFile)
                # fetchData[-1].start()
                #os.system('sshpass -p Aether scp "%s@%s:%s" "%s"' % (remoteUsername, remoteIp, remotePath, destination) )
    except Exception as err:
        print("Error: (Sockets)", err)
        continue

