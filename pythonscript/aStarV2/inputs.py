from aStarV2 import grid, imprtntpts,makePath


# DTU Sample Mission
# jsonData = {
#   "id": 1,
#   "lostCommsPos": {
#     "latitude": 28.75367425,
#     "longitude": 77.11576816
#   },
#   "flyZones": [
#     {
#       "altitudeMin": 65.0,
#       "altitudeMax": 180.0,
#       "boundaryPoints": [
#         {
#           "latitude": 28.75280299,
#           "longitude": 77.11616480
#         },
#         {
#           "latitude": 28.75287834,
#           "longitude": 77.11577951
#         },
#         {
#           "latitude": 28.75304204,
#           "longitude": 77.11556315
#         },
#         {
#           "latitude": 28.75337204,
#           "longitude": 77.11537050
#         },
#         {
#           "latitude": 28.75381636,
#           "longitude": 77.11534975
#         },
#         {
#           "latitude": 28.75420092,
#           "longitude": 77.11552165
#         },
#         {
#           "latitude": 28.75435682,
#           "longitude": 77.11570245
#         },
#         {
#           "latitude": 28.75446595,
#           "longitude": 77.11603736
#         },
#         {
#           "latitude": 28.75435942,
#           "longitude": 77.11644340
#         },
#         {
#           "latitude": 28.75421911,
#           "longitude": 77.11662123
#         },
#         {
#           "latitude": 28.75385534,
#           "longitude": 77.11681388
#         },
#         {
#           "latitude": 28.75343440,
#           "longitude": 77.11682870
#         },
#         {
#           "latitude": 28.75306543,
#           "longitude": 77.11665680
#         },
#         {
#           "latitude": 28.75289133,
#           "longitude": 77.11644637
#         }
#       ]
#     }
#   ],
#   "waypoints": [
#     {
#       "latitude": 28.75391566,
#       "longitude": 77.11568030,
#       "altitude": 792.0
#     },
#     {
#       "latitude": 28.75431948,
#       "longitude": 77.11598208,
#       "altitude": 808.0
#     },
#     {
#       "latitude": 28.75403263,
#       "longitude": 77.11660152,
#       "altitude": 799.0
#     },
#     {
#       "latitude": 28.75380148,
#       "longitude": 77.11633151,
#       "altitude": 818.0
#     },
#     {
#       "latitude": 28.75351185,
#       "longitude": 77.11647445,
#       "altitude": 841.0
#     },
#     {
#       "latitude": 28.75312196,
#       "longitude": 77.11571206,
#       "altitude": 828.0
#     },
#     {
#       "latitude": 28.75371236,
#       "longitude": 77.11544840,
#       "altitude": 818.0
#     }
#   ],
#   "searchGridPoints": [
#     {
#       "latitude": 28.75327732,
#       "longitude": 77.11602988
#     },
#     {
#       "latitude": 28.75333142,
#       "longitude": 77.11620814
#     },
#     {
#       "latitude": 28.75348742,
#       "longitude": 77.11657785
#     },
#     {
#       "latitude": 28.75333125,
#       "longitude": 77.11657785
#     },
#     {
#       "latitude": 28.75304037,
#       "longitude": 77.11639303
#     },
#     {
#       "latitude": 28.75301108,
#       "longitude": 77.11609242
#     },
#     {
#       "latitude": 28.75316336,
#       "longitude": 77.11593432
#     }
#   ],
#   "offAxisOdlcPos": {
#     "latitude": 28.75352534,
#     "longitude": 77.11607885
#   },
#   "emergentLastKnownPos": {
#     "latitude": 28.75335643,
#     "longitude": 77.11638478
#   },
#   "airDropBoundaryPoints": [
#     {
#       "latitude": 28.75338619,
#       "longitude": 77.11573711
#     },
#     {
#       "latitude": 28.75329406,
#       "longitude": 77.11571017
#     },
#     {
#       "latitude": 28.75332477,
#       "longitude": 77.11560778
#     },
#     {
#       "latitude": 28.75340508,
#       "longitude": 77.11562394
#     }
#   ],
#   "airDropPos": {
#     "latitude": 28.75333356,
#     "longitude": 77.11567220
#   },
#   "ugvDrivePos": {
#     "latitude": 28.75355501,
#     "longitude": 77.11562965
#   },
#   "stationaryObstacles": [
#     {
#       "latitude": 28.75413596,
#       "longitude": 77.11584471,
#       "radius": 39.0,
#       "height": 180.0
#     },
#     {
#       "latitude": 28.75403722,
#       "longitude": 77.11615591,
#       "radius": 23.0,
#       "height": 135.0
#     },
#     {
#       "latitude": 28.75415935,
#       "longitude": 77.11644637,
#       "radius": 50.0,
#       "height": 180.0
#     },
#     {
#       "latitude": 28.75320834,
#       "longitude": 77.11626854,
#       "radius": 33.0,
#       "height": 75.0
#     }
#   ],
#   "mapCenterPos": {
#     "latitude": 28.75364835,
#     "longitude": 77.11609492
#   },
#   "mapHeight": 165.0
# }

# Sample SUAS input file
jsonData = {
  "id": 1,
  "lostCommsPos": {
    "latitude": 38.144778,
    "longitude": -76.429417
  },
  "flyZones": [
    {
      "altitudeMin": 100.0,
      "altitudeMax": 750.0,
      "boundaryPoints": [
        {
          "latitude": 38.1462694444444,
          "longitude": -76.4281638888889
        },
        {
          "latitude": 38.151625,
          "longitude": -76.4286833333333
        },
        {
          "latitude": 38.1518888888889,
          "longitude": -76.4314666666667
        },
        {
          "latitude": 38.1505944444444,
          "longitude": -76.4353611111111
        },
        {
          "latitude": 38.1475666666667,
          "longitude": -76.4323416666667
        },
        {
          "latitude": 38.1446666666667,
          "longitude": -76.4329472222222
        },
        {
          "latitude": 38.1432555555556,
          "longitude": -76.4347666666667
        },
        {
          "latitude": 38.1404638888889,
          "longitude": -76.4326361111111
        },
        {
          "latitude": 38.1407194444444,
          "longitude": -76.4260138888889
        },
        {
          "latitude": 38.1437611111111,
          "longitude": -76.4212055555556
        },
        {
          "latitude": 38.1473472222222,
          "longitude": -76.4232111111111
        },
        {
          "latitude": 38.1461305555556,
          "longitude": -76.4266527777778
        }
      ]
    }
  ],
  "waypoints": [
    {
      "latitude": 38.1446916666667,
      "longitude": -76.4279944444445,
      "altitude": 200.0
    },
    {
      "latitude": 38.1461944444444,
      "longitude": -76.4237138888889,
      "altitude": 300.0
    },
    {
      "latitude": 38.1438972222222,
      "longitude": -76.42255,
      "altitude": 400.0
    },
    {
      "latitude": 38.1417722222222,
      "longitude": -76.4251083333333,
      "altitude": 400.0
    },
    {
      "latitude": 38.14535,
      "longitude": -76.428675,
      "altitude": 300.0
    },
    {
      "latitude": 38.1508972222222,
      "longitude": -76.4292972222222,
      "altitude": 300.0
    },
    {
      "latitude": 38.1514944444444,
      "longitude": -76.4313833333333,
      "altitude": 300.0
    },
    {
      "latitude": 38.1505333333333,
      "longitude": -76.434175,
      "altitude": 300.0
    },
    {
      "latitude": 38.1479472222222,
      "longitude": -76.4316055555556,
      "altitude": 200.0
    },
    {
      "latitude": 38.1443333333333,
      "longitude": -76.4322888888889,
      "altitude": 200.0
    },
    {
      "latitude": 38.1433166666667,
      "longitude": -76.4337111111111,
      "altitude": 300.0
    },
    {
      "latitude": 38.1410944444444,
      "longitude": -76.4321555555556,
      "altitude": 400.0
    },
    {
      "latitude": 38.1415777777778,
      "longitude": -76.4252472222222,
      "altitude": 400.0
    },
    {
      "latitude": 38.1446083333333,
      "longitude": -76.4282527777778,
      "altitude": 200.0
    }
  ],
  "searchGridPoints": [
    {
      "latitude": 38.1444444444444,
      "longitude": -76.4280916666667
    },
    {
      "latitude": 38.1459444444444,
      "longitude": -76.4237944444445
    },
    {
      "latitude": 38.1439305555556,
      "longitude": -76.4227444444444
    },
    {
      "latitude": 38.1417138888889,
      "longitude": -76.4253805555556
    },
    {
      "latitude": 38.1412111111111,
      "longitude": -76.4322361111111
    },
    {
      "latitude": 38.1431055555556,
      "longitude": -76.4335972222222
    },
    {
      "latitude": 38.1441805555556,
      "longitude": -76.4320111111111
    },
    {
      "latitude": 38.1452611111111,
      "longitude": -76.4289194444444
    },
    {
      "latitude": 38.1444444444444,
      "longitude": -76.4280916666667
    }
  ],
  "offAxisOdlcPos": {
    "latitude": 38.145111,
    "longitude": -76.427861
  },
  "emergentLastKnownPos": {
    "latitude": 38.145111,
    "longitude": -76.427861
  },
  "airDropBoundaryPoints": [
    {
      "latitude": 38.14616666666666,
      "longitude": -76.42666666666668
    },
    {
      "latitude": 38.14636111111111,
      "longitude": -76.42616666666667
    },
    {
      "latitude": 38.14558333333334,
      "longitude": -76.42608333333334
    },
    {
      "latitude": 38.14541666666667,
      "longitude": -76.42661111111111
    }
  ],
  "airDropPos": {
    "latitude": 38.145848,
    "longitude": -76.426374
  },
  "ugvDrivePos": {
    "latitude": 38.146152,
    "longitude": -76.426396
  },
  "stationaryObstacles": [
    {
      "latitude": 38.146689,
      "longitude": -76.426475,
      "radius": 150.0,
      "height": 750.0
    },
    {
      "latitude": 38.142914,
      "longitude": -76.430297,
      "radius": 300.0,
      "height": 300.0
    },
    {
      "latitude": 38.149504,
      "longitude": -76.43311,
      "radius": 100.0,
      "height": 750.0
    },
    {
      "latitude": 38.148711,
      "longitude": -76.429061,
      "radius": 300.0,
      "height": 750.0
    },
    {
      "latitude": 38.144203,
      "longitude": -76.426155,
      "radius": 50.0,
      "height": 400.0
    },
    {
      "latitude": 38.146003,
      "longitude": -76.430733,
      "radius": 225.0,
      "height": 500.0
    }
  ],
  "mapCenterPos": {
    "latitude": 38.145103,
    "longitude": -76.427856
  },
  "mapHeight": 1200.0
}
# ####################################################################################################
# ####################################################################################################
# ####################################################################################################
def feetToMeter(a):
  b = a*0.3048
  return b

def obstaclelist(a):
    obs = []
    for i in a["stationaryObstacles"]:
      x = feetToMeter(i["radius"])
      o = (i["latitude"],i["longitude"],x)
      obs.append(o)

    return obs

def waypointlist(a):
    wps = []
    for i in a["waypoints"]:
        y = i["altitude"] - 40
        x = feetToMeter(y)
        w = (i["latitude"],i["longitude"],x)
        wps.append(w)

    return(wps)

def geofenceList(a):
    gfs = []
    b = a["flyZones"][0]
    for i in b["boundaryPoints"]:
        g = (i["latitude"],i["longitude"])
        gfs.append(g)

    return gfs

# inclusionGeofence = geofenceList(jsonData)
# Waypoints = waypointlist(jsonData)
# Obstacles = obstaclelist(jsonData)

# inclusionGeofence = [(28.75282483, 77.11612238),( 28.75310103, 77.11551856),( 28.75361659, 77.11535054),( 28.75419660, 77.11550806),(28.75446819, 77.11606463),(28.75424723, 77.11658444),(28.75369485, 77.11682072),(28.75310103, 77.11665795)]
# Waypoints = [(28.75323452, 77.11570758, 20),(28.75363961, 77.11551856, 15),(28.75409072, 77.11568133, 25),(28.75412295, 77.11642167, 25),( 28.75366262, 77.11663695, 30),(28.75365342, 77.11609613, 20),(28.75329437, 77.11634291, 15)]
# Obstacles = [(28.75345548, 77.11560257,10),(28.75392961, 77.11551856, 13),( 28.75411374, 77.11605413,20),(28.75342326, 77.11619589,5)]

# inclusionGeofence = [(28.75339705, 77.11586844),(28.75339882, 77.11668222),(28.75402530, 77.11669032),(28.75402530, 77.11587047),(28.75384960, 77.11586844),(28.75384783, 77.11643728),(28.75357807, 77.11643728),(28.75357630, 77.11586844)]
# Waypoints = [(28.75348756, 77.11596966,10),(28.75393656, 77.11597168,10)]
# Obstacles = [(28.75371117, 77.11664174, 3)]


def plannedPath(mission, wayPointList = None):
  ################################################################

  #waypointList = [(lat1,lon1,alt1_in_meters),(lat2,lon2,alt2_in_meters)]
  inclusionGeofence = geofenceList(mission)
  if wayPointList == None:
    Waypoints = waypointlist(mission)
  else:
    Waypoints = wayPointList
  Obstacles = obstaclelist(mission)
  ################################################################
  cellDimension = 10
  minCorner, maxCorner = grid.cornerCoordinates(inclusionGeofence)
  length, width = grid.makeBoundary(minCorner,maxCorner)
  Rows, Columns = grid.getDimensions(cellDimension,length,width)
  ################################################################
  waypointCartesian = imprtntpts.wayptCart(Waypoints,minCorner)
  obstacleCartesian, obstacleRadius = imprtntpts.obsCart(Obstacles,cellDimension,minCorner)
  geofenceCartesian = imprtntpts.geoCart(inclusionGeofence,minCorner)
  ################################################################
  ob = makePath.obstacleMergeList(obstacleCartesian,obstacleRadius)
  waypointList = makePath.findPath(waypointCartesian,ob,geofenceCartesian,Waypoints,cellDimension,minCorner,maxCorner)
  waypointDictionary = makePath.jSonOutput(waypointList) 

  return waypointList, waypointDictionary

# def twoPointPlannedPath(mission,waypointList):
#   inclusionGeofence = geofenceList(mission)
#   Obstacles = obstaclelist(mission)
#   Waypoints = waypointList



# if __name__ == "__main__":
#   waypointList,waypointDictionary = plannedPath(jsonData)

#   print(waypointList)
#   ################################################################
#   ################################################################
#   ################################################################
#   print(waypointDictionary)





# if __name__ == "__main__":
#   print(inclusionGeofence)
#   print("#########################################################")
#   print(Waypoints)
#   print("#########################################################")
#   print(Obstacles)
#   print(len(Obstacles))

  # waypointList, waypointDictionary = pathPlanning(jsonData)
  # print(waypointList)
  # print("#########################################################")
  # print("#########################################################")
  # print("#########################################################")
  # print(waypointDictionary)
  
