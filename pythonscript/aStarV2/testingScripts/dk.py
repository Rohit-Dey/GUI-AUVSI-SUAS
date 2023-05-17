from dronekit import connect, VehicleMode, LocationGlobalRelative
import time, math
import makePath

# vehicle = connect('/dev/ttyTHS1', wait_ready=True, baud=57600)
vehicle = connect('127.0.0.1:14550', wait_ready=True, baud=57600)

def arm_and_takeoff(aTargetAltitude):

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)

  print("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    print(" Altitude: ", vehicle.location.global_relative_frame.alt) 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print("Reached target altitude")
      break
    time.sleep(1)
    
# Initialize the takeoff sequence to 15m
arm_and_takeoff(10)

print("Take off complete")


def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def go_to_waypoint(L):

  for i in range(len(L)):
    #lat1 = vehicle.location.global_relative_frame.lat
    #lon1 = vehicle.location.global_relative_frame.lon
    #lat2 = i[0]
    #lon2 = i[1]
    
    print("reaching waypoint number",i+1," : ",L[i])
    a_location = LocationGlobalRelative(L[i][0],L[i][1],L[i][2])
    vehicle.simple_goto(a_location)
    # print(L.index(i))
    while True: 
      dist = haversine(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, L[i][0], L[i][1])
      if dist > 0.001:
        vehicle.simple_goto(a_location)
        time.sleep(2)
        continue
      else:
        break  
go_to_waypoint(makePath.Waypoints)

# waypoint = [(28.75322182793156, 77.1156781757395, 20), (28.753492508309858, 77.11578056301704, 15), (28.753618826557993, 77.11549388117818, 15), (28.753835370594373, 77.1157396097149, 25), (28.754069960694537, 77.11565770098774, 25), (28.753817323984745, 77.11604676989643, 25), (28.75410604776035, 77.11639488771739, 25), (28.753654911425105, 77.116620133729, 30), (28.753636870110757, 77.11606724601413, 20), (28.753492505567362, 77.11631297246669, 15), (28.75327596103604, 77.11631297048116, 15)]
# go_to_waypoint(waypoint)



# Hover for 10 seconds

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()