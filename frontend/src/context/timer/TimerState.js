import React, { useState } from 'react'
import timerContext from "./timerContext"

function TimerState(props){
  const[isActive, setIsActive] = useState(false);
  const [min, setMin] = useState(0);
  const [sec, setSec] = useState(0);

  const handleStart = () =>{
    setIsActive(true);
  }

  const handleReset = () => {
    setSec(0);
    setMin(0);
    setIsActive(false);
  }

  return (
    <timerContext.Provider value={{isActive,setIsActive,sec,setSec,min,setMin, handleReset,handleStart }}>
      {props.children}
    </timerContext.Provider>
  )
}

export default TimerState;