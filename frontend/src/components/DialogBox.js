import React, { useContext, useEffect} from 'react'
import {
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Button
} from "@mui/material";
import sideBarContext from "../context/sidebar/sideBarContext";
import {SocketContext} from "../context/SocketContext"
import timerContext from '../context/timer/timerContext';

export default function DialogBox() {
    const context = useContext(sideBarContext);
    const {setOpenclmodal,currButton,setCurrButton,setIsTeleOn,isTeleOn,setIsOdlcOn,setIsOffAxisOn,setIsMapOn,setIsWayPoints,setShowRoverDrop,setGotoEmergent,PauseTask } = context;

    const context1 = useContext(SocketContext);
    const { socket } = context1;

    const context2 = useContext(timerContext)
    const {handleReset} = context2;
    
    const handleClosingTask = () =>{
        if(currButton === "Telem")
        { 
            setIsTeleOn(false);
            window.localStorage.setItem("Telem", false);
            socket.emit('telemPipeline', 'STOP')
        }
        else if(currButton === "Odlc")
        { 
            setIsOdlcOn(false);
            window.localStorage.setItem("Odlc", false);
            PauseTask()
        }
        else if(currButton === "OffAxis")
        { 
            setIsOffAxisOn(false);
            window.localStorage.setItem("OffAxis", false);
            PauseTask()
        }
        else if(currButton === "Map")
        { 
            setIsMapOn(false);
            window.localStorage.setItem("Map", false);
            PauseTask()
        }

        else if(currButton === "Waypoints")
        { 
            setIsWayPoints(false);
            window.localStorage.setItem("Waypoints", false);
            PauseTask()
        }
        else if(currButton === "RoverDrop")
        { 
            setShowRoverDrop(false);
            window.localStorage.setItem("RoverDrop", false);
            PauseTask()
        }
        else if(currButton === "Emergent")
        { 
            setGotoEmergent(false);
            window.localStorage.setItem("Emergent",false);
            PauseTask()
        }

        if(currButton !== "Telem")
        { 
            handleReset()
        }
        setOpenclmodal(false)
    }
    
    return (
        <>
            <DialogTitle id="alert-dialog-title">
                {"Do you want to continue?"}
            </DialogTitle>
            <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    {"This action will stop the process."}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={() => setOpenclmodal(false)}>No</Button>
                <Button onClick={() => {handleClosingTask()}}>Yes</Button>
            </DialogActions>
        </>
    )
}

