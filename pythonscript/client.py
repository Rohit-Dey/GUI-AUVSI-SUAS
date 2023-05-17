import gc
import socketio
import threading
import time
import socket
import json
from auvsi_suas.client import client                #   SUAS_DATA CALL FILES
from auvsi_suas.proto import interop_api_pb2        #

client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

sio = socketio.Client()


@sio.event
def team_data(): 
    teams = client.get_teams()
    print(teams)

@sio.event
def missn_dt():
    mission = client.get_mission(1)
    print(mission)

@sio.event
def pst_telem():    
    telemetry= interop_api_pb2.Telemetry()
    telemetry.latitude = 79
    telemetry.longitude = -76
    telemetry.altitude = 100
    telemetry.heading = 90
    client.post_telemetry(telemetry)

@sio.event
def pst_odlc():
    odlc = interop_api_pb2.Odlc()
    odlc.type = interop_api_pb2.Odlc.STANDARD
    odlc.latitude = 38
    odlc.longitude = -76
    odlc.orientation = interop_api_pb2.Odlc.N
    odlc.shape = interop_api_pb2.Odlc.SQUARE
    odlc.shape_color = interop_api_pb2.Odlc.GREEN
    odlc.alphanumeric = 'A'
    odlc.alphanumeric_color = interop_api_pb2.Odlc.WHITE

    odlc = client.post_odlc(odlc)

    with open('/home/kunal/Desktop/ashu/D/3044', 'rb') as f:
        image_data = f.read()
        client.put_odlc_image(odlc.id, image_data)
        
@sio.event
def pst_map_img():
    mission_id = 1

    with open('/home/kunal/Desktop/ashu/D/3044.jpg', 'rb') as f:
        image_data = f.read()
        client.put_map_image(mission_id, image_data)

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

def my_background_task():
    while(1):
        sio.emit('messagetoreact',"Hi bro I am python client")
        time.sleep(0.05)



sio.connect('http://localhost:5000')
print("Emmiting Data")
sio.emit('join_room', "Python's Room")

my_background_task()

#msg = threading.Thread(target = my_background_task)
# msg = threading.Thread(target = getDataFromGcsClient)
# msg.start()
#sio.wait()