import React, { createContext, useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const SocketContext = createContext();

const socket = io(process.env.REACT_APP_BACKEND_CONN + '/wtp');
socket.emit("join_room", "React's Room")

const ContextProvider = ({ children }) => {
    const [mission, setMission] = useState("No mission");
    const [aStarPath, setAStarPath] = useState();
    const [odlcPath, setOdlcPath] = useState();
    const [mapPath, setMapPath] = useState();
    const [mapStatus, setMapStatus] = useState();
    const [taskStatus, setTaskStatus] = useState();
    const [uavTelem, setUavTelem] = useState();
    const [ugvTelem, setRoverTelem] = useState();

    useEffect(() => {
        msgforreact()
        if (localStorage.getItem("mission") !== null) {
            setMission(JSON.parse(window.localStorage.getItem("mission")));
            setOdlcPath(JSON.parse(window.localStorage.getItem("odlcPath")));
            setMapPath(JSON.parse(window.localStorage.getItem("mapPath")));
            setAStarPath(JSON.parse(window.localStorage.getItem("aStarPath")));
        }
    }, []);

    useEffect(() => {
        if (mission !== "No mission") {
            window.localStorage.setItem("mission", JSON.stringify(mission));
            window.localStorage.setItem("aStarPath", JSON.stringify(aStarPath));
            window.localStorage.setItem("odlcPath", JSON.stringify(odlcPath));
            window.localStorage.setItem("mapPath", JSON.stringify(mapPath));
        }
    }, [mission, aStarPath, odlcPath, mapPath])

    useEffect(() => {
        const uavdatalistener = uavTelemetry();
        return () => { uavdatalistener() };
    }, []);

    useEffect(() => {
        const roverdatalistener = roverTelemetry();
        return () => { roverdatalistener() };
    }, [])

    const msgforreact = () => {
        socket.on("sendtoreact", (data) => {
        });
    }
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    socket.on("missionFromInterop", (data) => {
        setMission({ ...data });
    });

    socket.on("aStarPath", (data) => {
        setAStarPath({ ...data });
    });

    socket.on("aStarOdlcPath", (data) => {
        setOdlcPath({ ...data });
    });

    socket.on("aStarMapPath", (data) => {
        setMapPath({ ...data });
    });

    socket.on("mapUploadStatus", (data) => {
        setMapStatus({ ...data });
    });

    socket.on("taskConfirmation", (data) => {
        setTaskStatus({ ...data });
    });

    const uavTelemetry = () => {
        socket.on("uavTelem", (data) => {
            if (data === "Paused") {
                setUavTelem(null)
            }
            else {
                setUavTelem({ ...data });
            }
        });
    }

    const roverTelemetry = () => {
        socket.on("roverTelem", (data) => {
            if (data === "Paused") {
                setRoverTelem(null)
            }
            else {
                setRoverTelem({ ...data });
            }
        });
    }

    //// ROVER DROP ////////

    // const RoverDrop = () => {
    //     const mission_id = 1;
    //     socket.emit("RoverDropToPython", mission_id);
    // }

    // const RoverDropToReact = () => {
    //     socket.on("RoverDropToReact", (data) => {
    //         console.log("insocketcontext RoverDrop")
    //         console.log(data)
    //         setRoverdata({ ...data });
    //     });
    // }


    return (
        <div>
            <SocketContext.Provider value={{ socket, mission, aStarPath, mapStatus, uavTelem, ugvTelem, odlcPath, mapPath, taskStatus }}>
                {children}
            </SocketContext.Provider>
        </div>

    )
}

export { ContextProvider, SocketContext }