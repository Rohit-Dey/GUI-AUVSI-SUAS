import React, { useState, useContext, useEffect } from 'react'
import sideBarContext from "./sideBarContext"
import { SocketContext } from "../SocketContext";
import timerContext from '../timer/timerContext';

function SideBarState(props) {
  const context = useContext(SocketContext);
  const { socket } = context;

  const context1 = useContext(timerContext);
  const { handleStart } = context1;

  const [openclmodal, setOpenclmodal] = useState(false);
  const [openInput, setOpenInput] = useState(false);
  const [isTeleOn, setIsTeleOn] = useState(false);
  const [isOdlcOn, setIsOdlcOn] = useState(false);
  const [isOffAxisOn, setIsOffAxisOn] = useState(false);
  const [isMapOn, setIsMapOn] = useState(false);
  const [isWayPoints, setIsWayPoints] = useState(false);
  const [currButton, setcurrButton] = useState(null);
  const [showRoverDrop, setShowRoverDrop] = useState(false);
  const [GotoEmergent, setGotoEmergent] = useState(false);
  const [Latch, setLatch] = useState(false);
  const [Brake, setBrake] = useState(false);

  useEffect(() => {
    setIsTeleOn('true' === window.localStorage.getItem('Telem'));
    setIsOdlcOn('true' === window.localStorage.getItem('Odlc'));
    setIsOffAxisOn('true' === window.localStorage.getItem('OffAxis'));
    setIsMapOn('true' === window.localStorage.getItem("Map"));
    setIsWayPoints('true' === window.localStorage.getItem('Waypoints'));
    setShowRoverDrop('true' === window.localStorage.getItem('RoverDrop'));
    setGotoEmergent('true' === window.localStorage.getItem('Emergent'))
    setLatch('true' === window.localStorage.getItem('Latch'))
    setBrake('true' === window.localStorage.getItem('Brake'))
  }, [])

  const handleCloseInput = (ipaddress) => {
    window.localStorage.setItem("Telem", true);
    setOpenInput(false);
    setIsTeleOn(true);
    socket.emit('telemPipeline', ipaddress.textmask)
  };

  const check = () => {
    if (GotoEmergent === false && isOdlcOn === false && isOffAxisOn === false && isWayPoints === false && isMapOn === false && showRoverDrop === false) {
      return true;
    }
    return false;
  }

  const handleTelem = () => {
    if (isTeleOn === true) {
      setcurrButton("Telem")
      setOpenclmodal(true);
    }
    else {
      setOpenInput(true);
    }
  };

  const handleOdlc = () => {
    if (isOdlcOn === true) {
      setcurrButton("Odlc")
      setOpenclmodal(true);

    }
    else {
      if (check()) {
        setIsOdlcOn(true);
        window.localStorage.setItem("Odlc", true);
        sendOdlcTask()
        handleStart()
      }
    }
  }

  const handleOffAxis = () => {
    if (isOffAxisOn === true) {
      setcurrButton("OffAxis")
      setOpenclmodal(true);

    }
    else {
      if (check() === true) {
        setIsOffAxisOn(true);
        window.localStorage.setItem("OffAxis", true);
        sendOffAxisTask();
        handleStart()
      }
    }
  }

  const handleMap = () => {
    if (isMapOn === true) {
      setcurrButton("Map")
      setOpenclmodal(true);

    }
    else {
      if (check() === true) {
        setIsMapOn(true);
        window.localStorage.setItem("Map", true);
        sendMappingTask()
        handleStart()
      }
    }
  }

  const handleWaypoints = () => {
    if (isWayPoints === true) {
      setcurrButton("Waypoints")
      setOpenclmodal(true);
    }
    else {
      if (check() === true) {
        setIsWayPoints(true);
        window.localStorage.setItem("Waypoints", true);
        sendWaypointsTask()
        handleStart()
      }
    }
  }

  const handleRoverdrop = () => {
    if (showRoverDrop === true) {
      setcurrButton("RoverDrop")
      setOpenclmodal(true);

    }
    else {
      if (check() === true) {
        setShowRoverDrop(true)
        window.localStorage.setItem("RoverDrop", true);
        sendRoverDropGotoTask()
        handleStart()
      }
    }
  }

  const handleGotoEmergent = () => {
    if (GotoEmergent === true) {
      setcurrButton("Emergent")
      setOpenclmodal(true);

    }
    else {
      if (check() === true) {
        setGotoEmergent(true)
        window.localStorage.setItem("Emergent", true);
        sendEmergentTask()
        handleStart()
      }
    }
  }

  const sendWaypointsTask = () => {
    console.log("Waypoints sent")
    socket.emit('sendTask', "startWaypoints")
  }

  const sendEmergentTask = () => {
    console.log("Emergent Sent")
    socket.emit('sendTask', "startEmergent")
  }

  const sendOdlcTask = () => {
    console.log("Odlc sent")
    socket.emit('sendTask', "startOdlc")
  }

  const sendOffAxisTask = () => {
    console.log("Off-Axis sent")
    socket.emit('sendTask', "startOffAxis")
  }

  const sendMappingTask = () => {
    console.log("Mapping sent")
    socket.emit('sendTask', "startMapping")
  }

  const sendRoverDropGotoTask = () => {
    console.log("Rover Goto sent")
    socket.emit('sendTask', "startGotoDrop")
  }

  const PauseTask = () => {
    console.log("Pause")
    socket.emit('sendCmd', "Pause")
  }

  const StopTask = () => {
    console.log("Stop")
    socket.emit('sendCmd', "Stop")
  }

  return (
    <sideBarContext.Provider value={{ openclmodal, setOpenclmodal, currButton, setcurrButton, openInput, setOpenInput, isTeleOn, setIsTeleOn, isOdlcOn, setIsOdlcOn, isOffAxisOn, setIsOffAxisOn, isMapOn, setIsMapOn, isWayPoints, setIsWayPoints, showRoverDrop, setShowRoverDrop, GotoEmergent, setGotoEmergent, handleTelem, handleCloseInput, handleOdlc, handleOffAxis, handleMap, handleWaypoints, handleRoverdrop, handleGotoEmergent, PauseTask,Latch,setLatch,Brake,setBrake }}>
      {props.children}
    </sideBarContext.Provider>
  )
}

export default SideBarState;
