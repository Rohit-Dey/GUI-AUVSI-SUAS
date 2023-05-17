import dronekit
from pymavlink import mavutil
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import numpy as np
from math import *
import threading
from math import radians, cos, sin, asin, sqrt,atan2
import random
import requests
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString

class swarmbot:
    def __init__(self,s):
        self.velocity=[0,0]
        self.vehicle = dronekit.connect(s, wait_ready=True)
        self.id=int(self.vehicle.parameters['SYSID_THISMAV'])
        print("Connected to vehicle id : " + str(self.id))
        self.wplist=[]
    
    def get_pos(self):
        self.pos= [self.vehicle.location.global_frame.lat,self.vehicle.location.global_frame.lon]
        return self.pos
    
    def get_vel(self):
        return self.vehicle.velocity

    def update_pos(self,pos,v):
        self.position=pos
        pos_x = pos[0]
        pos_y = pos[1]
        pos_z = pos[2]
        a_location = LocationGlobalRelative(pos_x, pos_y, pos_z)
        self.vehicle.simple_goto(a_location,v,v)

    def update_vel(self,v):
        self.velocity=v       
        velocity_x=v[0]
        velocity_y=v[1]
        velocity_z=v[2]
        msg = self.vehicle.message_factory.set_position_target_global_int_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
            0b0000111111000111, # type_mask (only speeds enabled)
            0, # lat_int - X Position in WGS84 frame in 1e7 * meters
            0, # lon_int - Y Position in WGS84 frame in 1e7 * meters
            0, # alt - Altitude in meters in AMSL altitude(not WGS84 if absolute or relative)
            # altitude above terrain if GLOBAL_TERRAIN_ALT_INT
            velocity_x, # X velocity in NED frame in m/s
            velocity_y, # Y velocity in NED frame in m/s
            velocity_z, # Z velocity in NED frame in m/s
            0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        self.vehicle.send_mavlink(msg)
    def send_attitude_target(self,roll_angle = 0.0, pitch_angle = 0.0,
                         yaw_angle = None, yaw_rate = 0.0, use_yaw_rate = False,
                         thrust = 0.5):
        """
        use_yaw_rate: the yaw can be controlled using yaw_angle OR yaw_rate.
                      When one is used, the other is ignored by Ardupilot.
        thrust: 0 <= thrust <= 1, as a fraction of maximum vertical thrust.
                Note that as of Copter 3.5, thrust = 0.5 triggers a special case in
                the code for maintaining current altitude.
        """
        if yaw_angle is None:
            # this value may be unused by the vehicle, depending on use_yaw_rate
            yaw_angle = self.vehicle.attitude.yaw
        # Thrust >  0.5: Ascend
        # Thrust == 0.5: Hold the altitude
        # Thrust <  0.5: Descend
        msg = self.vehicle.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            1, # Target system
            1, # Target component
            0b00000000 if use_yaw_rate else 0b00000100,
            self.to_quaternion(roll_angle, pitch_angle, yaw_angle), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            radians(yaw_rate), # Body yaw rate in radian/second
            thrust  # Thrust
        )
        self.vehicle.send_mavlink(msg)
    def to_quaternion(self,roll = 0.0, pitch = 0.0, yaw = 0.0):
        """
        Convert degrees to quaternions
        """
        t0 = cos(radians(yaw * 0.5))
        t1 = sin(radians(yaw * 0.5))
        t2 = cos(radians(roll * 0.5))
        t3 = sin(radians(roll * 0.5))
        t4 = cos(radians(pitch * 0.5))
        t5 = sin(radians(pitch * 0.5))

        w = t0 * t2 * t4 + t1 * t3 * t5
        x = t0 * t3 * t4 - t1 * t2 * t5
        y = t0 * t2 * t5 + t1 * t3 * t4
        z = t1 * t2 * t4 - t0 * t3 
        return [w, x, y, z]

    def heading(self):
        self.head=self.vehicle.heading
        return self.head
        

    def altitude(self):
        return self.vehicle.location.global_relative_frame.alt


    def arm_and_takeoff(self, aTargetAltitude):
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...",self.id)
            time.sleep(1)

            
        print ("Arming motors",self.id)
        
        # Copter should arm in GUIDED mode
        self.vehicle.mode = dronekit.VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:      
            print (" Waiting for arming...",self.id)
            time.sleep(1)

        print ("Taking off!",self.id)
        self.vehicle.simple_takeoff(aTargetAltitude)

        while True:
            print (" Altitude: ", self.vehicle.location.global_relative_frame.alt)      
            if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.90: 
                print ("Reached target altitude",self.id)
                break
            time.sleep(1)

    def land(self):
        self.vehicle.mode = dronekit.VehicleMode("LAND")

    def wpoints(self,p):
        self.wplist=[]
        for i in range(len(p)):
           self.wplist.append(p[i])
        return self.wplist

    def waypoints(self):
        return self.wplist
    
    def Battery(self):
        return self.vehicle.battery

n=1
vehicle = []
approached_points = []
li = []
for i in range (n):
    vehicle.append(swarmbot("127.0.0.1:" + str(14552+(i*10))))
t=[]
for i in range(n):
    t1=t.append(threading.Thread(target=vehicle[i].arm_and_takeoff,args=(20,)))
for i in t:
    i.start()
for i in t:
    i.join()
while True:
            vehicle[0].update_vel([10,10,0])
            x = vehicle[0].Battery()
            l = vehicle[0].get_pos()
            print(l)
            print(x)
            time.sleep(1)
            print("done")
