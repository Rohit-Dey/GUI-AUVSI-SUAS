import React, { useRef, useEffect, useState, useContext } from "react";
import "mapbox-gl-style-switcher/styles.css";
import homeContext from "../context/home/homeContext";
import mapboxgl from "mapbox-gl"; // eslint-disable-next-line
import MapboxDraw from "@mapbox/mapbox-gl-draw"; // eslint-disable-next-line
import { SocketContext } from "../context/SocketContext";
import context from "../context/home/HomeState";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import "../Css/Map.css";
mapboxgl.accessToken =
  "pk.eyJ1Ijoic3VqYWwwODEwIiwiYSI6ImNsMmc1eHhlMDAwY2Uzb213dXBvdm9rdXcifQ.iIliIqDLgXPJGarndfo10w";

function Map(props) {
  const { mission,aStarPath,odlcPath,mapPath } = props;
  const Data = mission;
  const mapContainer = useRef(null);
  const map = useRef(null);

  const [exportdata, setexportdata] = useState(null);
  let {obstacleFreePath} = aStarPath
  const modifiedWaypoints = obstacleFreePath
  // console.log(obstacleFreePath)
  // const {modifiedWaypoints}=aStarPath
  // const { modifiedWaypoints } = sujalKaOutput;
  let {
    lostCommsPos,
    flyZones,
    waypoints,
    searchGridPoints,
    offAxisOdlcPos,
    emergentLastKnownPos,
    airDropBoundaryPoints,
    airDropPos,
    ugvDrivePos,
    stationaryObstacles,
    mapCenterPos,
  } = Data;

  var markers_dict = [];
  var points_dict = [];

  //single latlng objects
  for (let feature in Data) {
    if (!Array.isArray(Data[feature])) {
      markers_dict.push({
        key: feature,
        value: Data[feature],
      });
    } else {
      points_dict.push({
        key: feature,
        value: Data[feature],
      });
    }
  }

  // **********************************POINT GEOJSON********************************************
  let point_geojson = {
    type: "FeatureCollection",
    features: [],
  };
  const dict = [
    ["LostCommPosition", [lostCommsPos.longitude, lostCommsPos.latitude]],
    ["offAxisOdlcPos", [offAxisOdlcPos.longitude, offAxisOdlcPos.latitude]],
    [
      "emergentLastKnownPos",
      [emergentLastKnownPos.longitude, emergentLastKnownPos.latitude],
    ],
    ["airDropPos", [airDropPos.longitude, airDropPos.latitude]],
    ["ugvDrivePos", [ugvDrivePos.longitude, ugvDrivePos.latitude]],
  ];

  for (let i = 0; i < dict.length; i++) {
    var feat = {
      type: "Feature",
      id: dict[i][0],
      geometry: {
        type: "Point",
        coordinates: dict[i][1],
      },
      properties: {
        type: dict[i][0],
      },
    };
    point_geojson.features.push(feat);
  }
  
  // **********************************POINT GEOJSON********************************************
  let i;
  let list1 = [];
  for (i of flyZones[0].boundaryPoints) {
    list1.push([i.longitude, i.latitude]);
  }

  let list3 = [];
  for (i of searchGridPoints) {
    list3.push([i.longitude, i.latitude]);
  }
  let list4 = [];
  for (i of airDropBoundaryPoints) {
    list4.push([i.longitude, i.latitude]);
  }
  list4.push([
    airDropBoundaryPoints[0].longitude,
    airDropBoundaryPoints[0].latitude,
  ]);

  let map_geojson = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [list1],
        },
        properties: {
          type: "flyzones",
        },
      },
    ],
  };

  // let n = 0;
  // for (let i of markers_dict) {
  //   if (i.value.latitude === undefined) {
  //   } else {
  //     n++;
  //     let feat = {
  //       type: "Feature",
  //       id: i.key,
  //       geometry: {
  //         type: "Point",
  //         coordinates: [i.value.longitude, i.value.latitude],
  //       },
  //       properties: {
  //         type: i.key,
  //       },
  //     };
  //     map_geojson.features.push(feat);
  //   }
  // }

  let searchpt_geojson = {
    type: "FeatureCollection",
    features: [],
  };
  let num = 0;
  for (let i of stationaryObstacles) {
    num++;
    let feature = {
      id: "Obstacle-" + num,
      type: "Feature",
      properties: {
        radius: i.radius,
        height: i.height,
        type: "stationaryObstacles",
      },
      geometry: {
        type: "Point",
        coordinates: [i.longitude, i.latitude],
      },
    };
    searchpt_geojson.features.push(feature);
  }
  // console.log(searchpt_geojson);
  // circle-radius": ['match',['get','radius'],]
  let list2 = [];
  for (i of waypoints) {
    list2.push([i.longitude, i.latitude]);
  }
  let waypoints_geojson = {
    type: "FeatureCollection",
    features: [],
  };
  num = 0;
  for (let i of waypoints) {
    num++;
    let feature = {
      type: "Feature",
      id: "Waypoint-" + num,
      geometry: {
        type: "Point",
        coordinates: [i.longitude, i.latitude],
      },
      properties: {
        height: i.altitude,
        base_height: 0,
        color: "blue",
        type: "waypoints",
      },
    };
    waypoints_geojson.features.push(feature);
  }
  let waypt_geojson = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [list2],
        },
        properties: {
          type: "waypoints",
        },
      },
    ],
  };
  
  let searchgrid_geojson = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [list3],
        },
        properties: {
          type: "Search_grid",
        },
      },
    ],
  };
  let ugvgridjson = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [list4],
        },
        properties: {
          type: "UGV_grid",
        },
      },
    ],
  };

  const [lng, setLng] = useState(mapCenterPos.longitude);
  const [lat, setLat] = useState(mapCenterPos.latitude);
  const [zoom, setZoom] = useState(15);
  const [pos, setpos] = useState(null);
  // AMERICA RATIOS
  let ratio = [
    196717.31, 98358.65, 49179.33, 24589.66, 12294.83, 6147.42, 3073.71,
    1536.85, 768.43, 384.21, 192.11, 96.05, 48.03, 24.01, 12.01, 6.0, 3.0, 1.5,
    0.7508333, 0.375, 0.1875, 0.09416667, 0.04666667,
  ];
  // INDIA RATIOS
  // let ratio = [241309.50, 120654.75, 60327.38, 30163.69, 15081.84, 7540.92, 3770.46, 1885.23, 942.62, 471.31, 235.65, 117.83, 58.91, 29.46, 14.73, 7.36, 3.68, 1.84, 0.92083333, 0.46, 0.23, 0.115, 0.0575]

  let rad_arr = ["match", ["get", "radius"]];
  useEffect(() => {
    let arr = [];
    for (let i of stationaryObstacles) {
      if (arr.includes(i.radius)) {
      } else {
        rad_arr.push(i.radius);
        rad_arr.push(i.radius / ratio[Math.round(zoom)]);
      }
      arr.push(i.radius);
    }
    rad_arr.push(50);
    // console.log(rad_arr);

    // console.log('hello world')
  });
  //********************************************************** */
  useEffect(() => {
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-v9",
      center: [lng, lat],
      zoom: zoom,
    });
  });
  

  function HoverFunc(layer_id, source_id, geojson_id, current_map) {
    let hover_id = null;
    current_map.on("mousemove", layer_id, (e) => {
      current_map.getCanvas().style.cursor = "pointer";
      if (e.features.length > 0) {
        setpos(geojson_id.features[e.features[0].id].id);
        if (hover_id !== null) {
          current_map.setFeatureState(
            { source: source_id, id: hover_id },
            { hover: true }
          );
        }
        hover_id = e.features[0].id;
        current_map.setFeatureState(
          { source: source_id, id: hover_id },
          { hover: false }
        );
      }
    });
    current_map.on("mouseleave", layer_id, () => {
      if (hover_id !== null) {
        setpos(null);
        current_map.setFeatureState(
          { source: source_id, id: hover_id },
          { hover: false }
        );
      }
      hover_id = null;
      current_map.getCanvas().style.cursor = "";
    });
  }

  //*********************************************************/
  useEffect(() => {
    if (!map.current) return; // wait for map to initialize
    //Stores value of zoom while moving the map and display it
    map.current.on("move", () => {
      setZoom(map.current.getZoom().toFixed(2));
    });
    // console.log(zoom);
  });

  useEffect(() => {
    if (!map.current) return;
    map.current.on("load", async () => {
      function create_marker(x, y, title) {
        const marker = new mapboxgl.Marker()
          .setLngLat([x, y])
          .addTo(map.current);
        let markerElement = marker.getElement();
        const popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false,
          closeOnMove: true,
        }).setHTML(`${title}<br><b>Location:</b>(${x},${y})`);
        marker.setPopup(popup);
        markerElement.addEventListener("mouseenter", () => {
          markerElement.style.cursor = "pointer";
          marker.togglePopup();
        });
        markerElement.addEventListener("mouseleave", () => {
          markerElement.style.cursor = "";
          marker.togglePopup();
        });
      }
      const marker_list = await getMarkers();
      const updateSource = setInterval(async () => {
        const marker_list = await getMarkers(updateSource);
        for (let i of marker_list) {
          const { Shape, Latitude, Longitude } = i;
          create_marker(Longitude, Latitude, Shape);
        }
      }, 2000);
      async function getMarkers(updateSource) {
        // Make a GET request to the API and return the location of the ISS.
        try {
          const odlc_response = await fetch(
            process.env.REACT_APP_BACKEND_CONN + "/api/file/odlc_latlon",
            { method: "GET" }
          );
          const { xodlc } = await odlc_response.json();
          for (let i of xodlc) {
            const { Shape, Latitude, Longitude } = i;
            create_marker(Longitude, Latitude, Shape);
          }
          return xodlc;
          // Fly the map to the location.
          // Return the location of the ISS as GeoJSON.
          // return {
          //   type: "FeatureCollection",
          //   features: [
          //     {
          //       type: "Feature",
          //       geometry: {
          //         type: "Point",
          //         coordinates: [longitude, latitude],
          //       },
          //     },
          //   ],
          // };
        } catch (err) {
          // If the updateSource interval is defined, clear the interval to stop updating the source.
          if (updateSource) clearInterval(updateSource);
          throw new Error(err);
        }
      }

      // create_marker(-76.4296,38.1465,'Point')
      // console.log("marker_list", marker_list);
      // console.log('marker_list1',i)
      // console.log('marker_list_if',marker_list)
      // for (let q = 0; q < marker_list.length; q++) {
      //   console.log('marker_list.length',marker_list[q])
      //   create_marker(marker_list[q])
      // }

      // for (let i = 0; i < marker_list.length; i++) {
      //   create_marker(
      //     marker_list[i][i].Longitude,
      //     marker_list[i][i].Latitude,
      //     marker_list[i][i].Shape
      //   );
      // }
    });
  });
  //*********************************************************/
  //*********************************************************/
  function HoverFunc(layer_id, source_id, geojson_id, current_map) {
    let hover_id = null;
    current_map.on("mousemove", layer_id, (e) => {
      current_map.getCanvas().style.cursor = "pointer";
      if (e.features.length > 0) {
        setpos(geojson_id.features[e.features[0].id].id);
        if (hover_id !== null) {
          current_map.setFeatureState(
            { source: source_id, id: hover_id },
            { hover: true }
          );
        }
        hover_id = e.features[0].id;
        current_map.setFeatureState(
          { source: source_id, id: hover_id },
          { hover: false }
        );
      }
    });
    current_map.on("mouseleave", layer_id, () => {
      if (hover_id !== null) {
        setpos(null);
        current_map.setFeatureState(
          { source: source_id, id: hover_id },
          { hover: false }
        );
      }
      hover_id = null;
      current_map.getCanvas().style.cursor = "";
    });
  }

  //*********************************************************/
  /*********************************************************/

  useEffect(()=>{
    map.current.on('load', () => {
      map.current.addSource("gridpts", {
        type: "geojson",
        data: searchpt_geojson,
        generateId: true,
      });
      // console.log('hello')
      map.current.addLayer({
        id: "searchpts",
        type: "circle",
        source: "gridpts",
        layout: {},
        paint: {
          "circle-radius": rad_arr,
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#000000",
            "#FFFF00",
          ],
          "circle-stroke-width": 1.5,
          "circle-stroke-color": "#FFFF00",
          "circle-opacity": 0.2,
          "circle-translate": [-12, 6],
        },
        filter: ["==", "$type", "Point"],
      });
      HoverFunc("searchpts", "gridpts", searchpt_geojson, map.current);
    })  
    // console.log('Hello World')
  },[zoom])
  useEffect(() => {
    if (!map.current) return;
    map.current.on("load", () => {
      // stores value of lat and long of mouse pointer
      map.current.on("mousemove", (f) => {
        setLat(f.lngLat.lat.toFixed(4));
        setLng(f.lngLat.lng.toFixed(4));
      });

      // ****************LIVE LOCATION*************************************

      // Add a data source containing one point feature.

      // *****************************************************
      // adding sources....

      map.current.addSource("points_Source", {
        type: "geojson",
        data: point_geojson,
        generateId: true,
      });
      map.current.addSource("flyzones", {
        type: "geojson",
        data: map_geojson,
        generateId: true,
      });


      map.current.addSource("Search_grid", {
        type: "geojson",
        data: searchgrid_geojson,
        generateId: true,
      });

      /******************************************************************* */
    

      /******************************************************************* */

      // ******************************************************************

      /******************************************************************* */
      map.current.addSource("waypoints", {
        type: "geojson",
        data: waypoints_geojson,
        generateId: true,
      });
      map.current.addSource("waypoints-line", {
        type: "geojson",
        data: waypt_geojson,
        generateId: true,
      });

      map.current.addLayer({
        id: "waypts",
        type: "circle",
        source: "waypoints",
        layout: {},
        paint: {
          "circle-radius": 3,
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#000000",
            "#0000FF",
          ],
          "circle-stroke-width": 1.5,
          "circle-stroke-color": "white",
        },
      });

      map.current.addLayer({
        id: "waypts-outline",
        type: "line",
        source: "waypoints-line",
        layout: {},
        paint: {
          "line-color": "#4169E1",
          "line-width": 3,
          "line-opacity": 0.6,
          "line-dasharray": [2, 1],
        },
        // filter: ["==", "$type", "Point"],
      });

      HoverFunc("waypts", "waypoints", waypoints_geojson, map.current);

      /******************************************************************* */
      map.current.addSource("ugvSource", {
        type: "geojson",
        data: ugvgridjson,
        generateId: true,
      });
      map.current.addLayer({
        id: "uggrid",
        type: "line",
        source: "ugvSource",
        layout: {},
        paint: {
          "line-color": "#0000FF",
          "line-width": 3,
          "line-opacity": 1,
        },
        // filter: ["==", "$type", "Point"],
      });
      map.current.addLayer({
        id: "uggrid-fill",
        type: "fill",
        source: "ugvSource",
        layout: {},
        paint: {
          "fill-color": "#0000FF",
          "fill-opacity": 0.2,
        },
        // filter: ["==", "$type", "Point"],
      });
      // Add a new layer to visualize the polygon.
      map.current.addLayer({
        id: "Serach",
        type: "fill",
        source: "Search_grid",
        layout: {},
        paint: {
          "fill-color": "#00008B", // blue color fill
          "fill-opacity": 0.2,
        },
      });
      // Add a black outline around the polygon.
      map.current.addLayer({
        id: "Search-outline",
        type: "line",
        source: "Search_grid",
        layout: {},
        paint: {
          "line-color": "#00008B",
          "line-width": 3,
        },
      });

      map.current.addLayer({
        id: "points-viz",
        type: "circle",
        source: "points_Source",
        paint: {
          "circle-radius": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            10,
            5,
          ],
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#EE4B2B",
            "#000000",
          ],
          "circle-stroke-width": 1.5,
          "circle-stroke-color": "white",
        },
        filter: ["==", "$type", "Point"],
      });
      HoverFunc("points-viz", "points_Source", point_geojson, map.current);

      map.current.addLayer({
        id: "Flyzone",
        type: "fill",
        source: "flyzones",
        layout: {},
        paint: {
          "fill-color": "#0080ff", // blue color fill
          "fill-opacity": 0,
        },
        filter: ["==", "$type", "Polygon"],
      });
      // Add a black outline around the polygon.
      map.current.addLayer({
        id: "flyzones-outline",
        type: "line",
        source: "flyzones",
        layout: {},
        paint: {
          "line-color": "#FF0000",
          "line-width": 3,
        },
        filter: ["==", "$type", "Polygon"],
      });
      /******************************************************************* */
      // map.current.addLayer();
    });

    map.current.on("load", async () => {
      const draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true,
        },
        defaultMode: "simple_select",
      });
      map.current.addControl(new mapboxgl.NavigationControl(), "top-right");
      map.current.addControl(new mapboxgl.FullscreenControl());
      // map.current.addControl(new mapboxgl.)
      map.current.addControl(draw);
      map.current.on("draw.create", updateArea);
      map.current.on("draw.delete", updateArea);
      map.current.on("draw.update", updateArea);
      // map.current.on("draw.export", export_btn);

      function updateArea(e) {
        const data = draw.getAll();
        setexportdata(data);
      }
    });

    map.current.on("load", async () => {
      if (!map.current && modifiedWaypoints==undefined) return;
      let mod_waypoints_geojson = {
        type: "FeatureCollection",
        features: [],
      };
      num = 0;
      for (let i of modifiedWaypoints) {
        num++;
        let feature = {
          type: "Feature",
          id: "Modified Waypoint-" + num,
          geometry: {
            type: "Point",
            coordinates: [i.longitude, i.latitude],
          },
          properties: {
            height: i.altitude,
            base_height: 0,
            color: "blue",
            type: "modified waypoints",
          },
        };
        mod_waypoints_geojson.features.push(feature);
      }
      let modlist = [];
      for (i of modifiedWaypoints) {
        modlist.push([i.longitude, i.latitude]);
      }
      let mod_waypt_geojson = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: {
              type: "Polygon",
              coordinates: [modlist],
            },
            properties: {
              type: "mod_waypoints",
            },
          },
        ],
      };
      map.current.addSource("mod_waypoints_line", {
        type: "geojson",
        data: mod_waypt_geojson,
        generateId: true,
      });
      map.current.addSource("mod_waypoints", {
        type: "geojson",
        data: mod_waypoints_geojson,
        generateId: true,
      });
      map.current.addLayer({
        id: "mod_waypts",
        type: "circle",
        source: "mod_waypoints",
        layout: {},
        paint: {
          "circle-radius": 4,
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#0000FF",
            "#32CD32",
          ],
          "circle-stroke-width": 1.0,
          "circle-stroke-color": "white",
        },
      });

      map.current.addLayer({
        id: "mod-waypts-outline",
        type: "line",
        source: "mod_waypoints_line",
        layout: {},
        paint: {
          "line-color": "#32CD32",
          "line-width": 3,
          "line-opacity": 0.6,
          "line-dasharray": [5, 5],
        },
      });

      

      HoverFunc(
        "mod_waypts",
        "mod_waypoints",
        mod_waypoints_geojson,
        map.current
      );
    });
    map.current.on("load", async () => {
      map.current.loadImage(
        "https://cdn-icons-png.flaticon.com/512/1812/1812583.png",
        (error, photo) => {
          if (error) throw error;

          // Add the image to the map style.
          map.current.addImage("chutiya", photo);
        }
      );
      const geojson = await getLocation();
      // Add the ISS location as a source.
      map.current.addSource("drone_Source", {
        type: "geojson",
        data: geojson,
      });
      // Add the rocket symbol layer to the map.
      map.current.addLayer({
        id: "drone",
        type: "symbol",
        source: "drone_Source",
        layout: {
          "icon-image": "chutiya",
          "icon-size": ["interpolate", ["linear"], ["zoom"], 5, 0.4, 20, 0.05],
        },
      });

      // Update the source from the API every 2 seconds.
      const updateSource = setInterval(async () => {
        const geojson = await getLocation(updateSource);
        map.current.getSource("drone_Source").setData(geojson);
      }, 10);

      async function getLocation(updateSource) {
        // Make a GET request to the API and return the location of the ISS.
        try {
          const response = await fetch("http://localhost:5000/geojson", {
            method: "GET",
          });
          const { data } = await response.json();
          const { uavLat, uavLon } = data;
          // Fly the map to the location.
          // map.current.flyTo({
          //   center: [uavLon, uavLat],
          //   speed: 0.5,
          // });
          return {
            type: "FeatureCollection",
            features: [
              {
                type: "Feature",
                geometry: {
                  type: "Point",
                  coordinates: [uavLon, uavLat],
                },
              },
            ],
          };
        } catch (err) {
          if (updateSource) clearInterval(updateSource);
          throw new Error(err);
        }
      }
    });
  });
  useEffect(()=>{
    map.current.on("load", async () => {
      if (!map.current && odlcPath==undefined) return;
      let {obstacleFreePath}=odlcPath
      const modifiedODLC=obstacleFreePath  
      let mod_ODLC_geojson = {
        type: "FeatureCollection",
        features: [],
      };
      num = 0;
      for (let i of modifiedODLC) {
        num++;
        let feature = {
          type: "Feature",
          id: "Modified ODLC-" + num,
          geometry: {
            type: "Point",
            coordinates: [i.longitude, i.latitude],
          },
          properties: {
            base_height: 0,
            color: "blue",
            type: "modified ODLC",
          },
        };
        mod_ODLC_geojson.features.push(feature);
      }
      let modlist = [];
      for (i of modifiedODLC) {
        modlist.push([i.longitude, i.latitude]);
      }
      let mod_ODLC_LINE_geojson = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: {
              type: "Polygon",
              coordinates: [modlist],
            },
            properties: {
              type: "mod_ODLC",
            },
          },
        ],
      };
      map.current.addSource("mod_ODLC_line", {
        type: "geojson",
        data: mod_ODLC_LINE_geojson,
        generateId: true,
      });
      map.current.addSource("mod_ODLC", {
        type: "geojson",
        data: mod_ODLC_geojson,
        generateId: true,
      });
      map.current.addLayer({
        id: "mod_ODLC_LINE",
        type: "circle",
        source: "mod_ODLC",
        layout: {},
        paint: {
          "circle-radius": 4,
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#0000FF",
            "#FFA500",
          ],
          "circle-stroke-width": 1.0,
          "circle-stroke-color": "white",
        },
      });

      map.current.addLayer({
        id: "mod-ODLC_LINE-outline",
        type: "line",
        source: "mod_ODLC_line",
        layout: {},
        paint: {
          "line-color": "#FFA500",
          "line-width": 3,
          "line-opacity": 0.6,
          "line-dasharray": [5, 5],
        },
      });

      

      HoverFunc(
        "mod_ODLC_LINE",
        "mod_ODLC",
        mod_ODLC_geojson,
        map.current
      );
    });
    map.current.on("load", async () => {
      if (!map.current && mapPath==undefined) return;
      let {obstacleFreePath}=mapPath
      const modifiedMAP=obstacleFreePath  
      let mod_MAP_geojson = {
        type: "FeatureCollection",
        features: [],
      };
      num = 0;
      for (let i of modifiedMAP) {
        num++;
        let feature = {
          type: "Feature",
          id: "Modified MAP-" + num,
          geometry: {
            type: "Point",
            coordinates: [i.longitude, i.latitude],
          },
          properties: {
            base_height: 0,
            color: "blue",
            type: "modified MAP",
          },
        };
        mod_MAP_geojson.features.push(feature);
      }
      let modlist = [];
      for (i of modifiedMAP) {
        modlist.push([i.longitude, i.latitude]);
      }
      let mod_MAP_LINE_geojson = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: {
              type: "Polygon",
              coordinates: [modlist],
            },
            properties: {
              type: "mod_MAP",
            },
          },
        ],
      };
      map.current.addSource("mod_MAP_line", {
        type: "geojson",
        data: mod_MAP_LINE_geojson,
        generateId: true,
      });
      map.current.addSource("mod_MAP", {
        type: "geojson",
        data: mod_MAP_geojson,
        generateId: true,
      });
      map.current.addLayer({
        id: "mod_MAP_LINE",
        type: "circle",
        source: "mod_MAP",
        layout: {},
        paint: {
          "circle-radius": 4,
          "circle-color": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            "#0000FF",
            "#c1afc4",
          ],
          "circle-stroke-width": 1.0,
          "circle-stroke-color": "white",
        },
      });

      map.current.addLayer({
        id: "mod-MAP_LINE-outline",
        type: "line",
        source: "mod_MAP_line",
        layout: {},
        paint: {
          "line-color": "#c1afc4",
          "line-width": 2,
          "line-opacity": 0.6,
          "line-dasharray": [5,18],
        },
      });

      

      HoverFunc(
        "mod_MAP_LINE",
        "mod_MAP",
        mod_MAP_geojson,
        map.current
      );
    });
  })
  function export_btn() {
    console.log(exportdata);
  }

  return (
    // <div className="expcontainer">
    <div className="map">
      <div className="sidebar_Map">
        Lat:{lat} | Lng:{lng} | zoom:{zoom}
        <br />
        ID:<strong>{pos}</strong>
        <br />
        <button className="Export_btn" onClick={export_btn}>
          Export Coordinates
        </button>
      </div>
      <div ref={mapContainer} className="map_Container"></div>
    </div>
    // </div>
  );
}

function NoMap() {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [lng, setLng] = useState(77.1161173);
  const [lat, setLat] = useState(28.7535955);
  const [zoom, setZoom] = useState(17);
  const [pos, setpos] = useState(null);
  useEffect(() => {
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-v9",
      center: [lng, lat],
      zoom: zoom,
    });
  });
  return (
    // <div className="expcontainer">
    <div className="map">
      <div className="sidebar_Map">
        NO MISSION AVAILABLE
        <br />
      </div>
      <div ref={mapContainer} className="map_Container"></div>
    </div>
    // </div>
  );
}
const Mapping = () => {
  const context1 = useContext(SocketContext);
  let { mission,aStarPath,mapPath,odlcPath } = context1;
  // const context = useContext(homeContext);
  // console.log('misson', mission)
  // const { mission_status, set_status } = context
  // console.log({mission_status})

  return (
    <div>
      {mission !== "No mission"&& mapPath !== undefined ? (
        mission && <Map mission={mission} aStarPath={aStarPath} odlcPath={odlcPath} mapPath={mapPath} />
      ) : (
        <NoMap />
      )}
    </div>
  );
};

export default Mapping;
