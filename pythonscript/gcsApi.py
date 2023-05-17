import requests
import json

def uploadToLocalDbStandard(payloadJson, imgPath, imgName):
    url = "http://localhost:5000/api/file/upload/STANDARD"
    payload={
        "Shape": payloadJson["shape"],
        "Shape_Color": payloadJson["shapeColor"],
        "Alphanumeric": payloadJson["alphanumeric"],
        "Alphanumeric_Color": payloadJson["alphanumericColor"],
        "Orientation": payloadJson["orientation"],
        "Latitude": payloadJson["latitude"],
        "Longitude": payloadJson["longitude"],
        "Odlcid":payloadJson['id']
    }
    files = {
            'json': (None, json.dumps(payload), 'application/json'),
            'file': (imgName, open(imgPath, 'rb'), 'image/png')
        }
    # files={
    #   'file',('49.jpg',open('/home/uas-dtu/interop_odlc/49.jpg','rb'),'image/png'),
    #   'json': (None, json.dumps(payload), 'application/json')
    # }
    headers = {}
    response = requests.request("POST", url, headers=headers, files=files)
    response = response.json()
    return response["success"]

def fetchFromLocalDb(fileId):
    url = "http://localhost:5000/api/file/singleimage/" + str(fileId)
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    # print(response["chunk"][0]['data'])
    # print(response["odlc"])
    return bytes(response["chunk"][0]['data'], 'utf-8'), response["odlc"]

def updateDb(json, fileId):
    url = "http://localhost:5000/api/file/updateimage/" + str(fileId)
    payload = converToDbSchema(json)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)
    
def updateEmergentDb(id, description, fileId):
    url = "http://localhost:5000/api/file/updateimage/" + str(fileId)
    payload = converToDbSchemaEmergent(id, description)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)

def converToDbSchemaEmergent(id, description):
    payload={
        "Description":description,
        "Odlcid":int(id)
    }
    return json.dumps(payload)


def converToDbSchema(payloadJson):
    payload={
        # "Shape": payloadJson.shape,
        # "Shape_Color": payloadJson.shape_color,
        # "Alphanumeric": payloadJson.alphanumeric,
        # "Alphanumeric_Color": payloadJson.alphanumeric_color,
        # "Orientation": payloadJson.orientation,
        # "Latitude": payloadJson.latitude,
        # "Longitude": payloadJson.longitude,
        "Odlcid":payloadJson.id
    }
    return json.dumps(payload)

# testJson = {
#     "shape": "SQUARE",
#     "shapeColor": "ORANGE",
#     "alphanumeric": "L",
#     "alphanumericColor": "GRAY",
#     "orientation": "SW",
#     "latitude": "-3.2610574022542423e-06",
#     "longitude": "-1.306449183535345e-06",
#     "id": 476
# }

# converToDbSchema(testJson)
# uploadToLocalDbStandard(testJson, '/home/uas-dtu/interop_odlc/195.jpg', '195.jpg')
# fetchFromLocalDb("62a985e332f6264321bbd3db")
# updateDb(testJson, "629d42f8f87a9007a4ecf7d0")