
import React, { useEffect,useContext } from "react";
import timerContext from '../context/timer/timerContext';

function Timer() {
  const context = useContext(timerContext);
  const {isActive,setIsActive,sec,setSec,min,setMin} = context;

  useEffect(() => {
    const data = window.localStorage.getItem('sec')
    if(data!= null && JSON.parse(data) !== 0){
      setIsActive(true)
      setSec(JSON.parse(data));
    }
  }, [])

  useEffect(() => {
    const dataMin = window.localStorage.getItem('min')
    if(dataMin !==null && JSON.parse(dataMin) !== 0){
      setIsActive(true)
      setMin(JSON.parse(dataMin));
    }
  }, [])

  useEffect(() => {
    window.localStorage.setItem('sec', JSON.stringify(sec))
  }, [sec])

  useEffect(() => {
    window.localStorage.setItem('min', JSON.stringify(min))
  }, [min])

  useEffect(() =>{
    if(isActive){
      if(sec === 60){
        setMin(min+1);
        setSec(0)
      }
      const secId = setInterval(() => setSec((sec) => (sec+1)), 1000);
        
      return() => {
        clearInterval(secId);
      }
    }
  }, [isActive, sec, min])
  

  return (
    <>
     <div style={{whiteSpace:"nowrap"}}>{min <= 9 ? "0" + min: min } : {sec <= 9 ? "0" + sec: sec}</div>
    </>
  );
}

export default Timer;
