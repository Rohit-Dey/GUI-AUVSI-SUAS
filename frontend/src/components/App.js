import React,{useEffect} from "react";
import Home from "./Home";
import ZenMode from "./ZenMode";
import { ContextProvider } from '../context/SocketContext';
import HomeState from "../context//home/HomeState";
import TimerState from "../context/timer/TimerState";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SideBarState from "../context/sidebar/SideBarState";
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  useEffect(()=>{
    console.log(process.env)
  })

  return (
    <>
      <ThemeProvider theme={darkTheme}>
        <ContextProvider>
          <HomeState>
          <TimerState>
            <SideBarState>
                <BrowserRouter>
                  <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/odlc" element={<ZenMode />} />
                  </Routes>
                </BrowserRouter>
            </SideBarState>
            </TimerState>
          </HomeState>
        </ContextProvider>
      </ThemeProvider>
    </>
  );
}

export default App