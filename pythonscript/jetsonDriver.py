from ast import arg
import dronekit as dk
import os
import socket
import time
import threading
import subprocess as sp

vehicle = dk.connect('127.0.0.1:14585')
print("Connected")
cancelTermination = False
global status
status = 0
def flightTermination(value): # value = 1 to terminate
        value = int(value)
        msg = vehicle.message_factory.command_long_encode(
            0, 0,
            dk.mavutil.mavlink.MAV_CMD_DO_FLIGHTTERMINATION,
            0,
            value,
            0,
            0, 0, 0, 0, 0
        )
        for i in range(3):
            vehicle.send_mavlink(msg)

def comm():
    global cancelTermination
    while True:
        status = sp.call(["ping", "192.168.0.201", "-c1", "-w2", "-q"]) 
        print (status)
        if status == 0:
            print("comm is there")
            cancelTermination = True
        else:
            print("comm lost")
            cancelTermination = False

        # return status

def suas_failsafes():
    global cancelTermination
    startTime = time.time()
    while True:
        currentTime = time.time()
        print(currentTime - startTime, " seconds to terminate...")
        if cancelTermination:
            startTime = time.time()
        elif currentTime - startTime > 30 and currentTime - startTime < 180:
            vehicle.mode = 'RTL'
            print("Switching to RTL")
        elif (currentTime - startTime > 180) and (vehicle.mode != 'RTL' or vehicle.mode != 'LAND'):
            print("Terminating Flight......")
            flightTermination(1)
    print("Comm Re-established")
            #flightTermination(1)

def roverDrop():
    print("Starting Drop")

def Odlc():
    print("Starting ODLC")

def wpFollowing():
    print("Starting WP Following")

boom = threading.Thread(target = comm)
boom1 = threading.Thread(target = suas_failsafes)
# suas_failsafes(True)
# suas_failsafes(False)
boom.start()
boom1.start()
# s = time.time()
# while True:
#     c = time.time()
#     if c-s > 10:
#         print("lol: ", c-s)
#         cancelTermination = True
#         boom.join()

