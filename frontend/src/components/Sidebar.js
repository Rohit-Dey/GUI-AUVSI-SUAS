import React, { useContext, useState } from "react";
import {
  Tabs,
  Box,
  Tab,
  Divider,
  Button,
  Typography,
  Drawer,
  Toolbar,
  Switch,
  Stack,
  FormControlLabel,
  Dialog,
  DialogActions,
  DialogTitle,
  TextField,
  FormControl,
  Input,
  InputLabel,
} from "@mui/material";
import PropTypes from "prop-types";
import { ElectricCar } from "@mui/icons-material";
import PlaneInfo from "./PlaneInfo";
import UgvInfo from "./UgvInfo";
import { SocketContext } from "../context/SocketContext";
import "../Css/Sidebar.css";
import DownloadIcon from "@mui/icons-material/Download";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import { styled } from "@mui/material/styles";
import SendIcon from "@mui/icons-material/Send";
import "../Css/Sidebar.css";
import homeContext from "../context/home/homeContext";
import { IMaskInput } from "react-imask";
import sideBarContext from "../context/sidebar/sideBarContext";
import DialogBox from "./DialogBox";
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ top: 0, height: "30vh" }}>{children}</Box>}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `vertical-tab-${index}`,
    "aria-controls": `vertical-tabpanel-${index}`,
  };
}

const Inputfile = styled("input")({
  display: "none",
});

const TextMaskCustom = React.forwardRef(function TextMaskCustom(props, ref) {
  const { onChange, ...other } = props;
  return (
    <IMaskInput
      {...other}
      mask="000.0.0.0:00000"
      definitions={{
        "#": /[1-9]/,
      }}
      inputRef={ref}
      onAccept={(value) => onChange({ target: { name: props.name, value } })}
      overwrite
    />
  );
});

TextMaskCustom.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default function SideBar(props) {
  const drawerWidth = "20vw";
  const context = useContext(SocketContext);
  const { socket } = context;
  const sidebarcontext = useContext(sideBarContext);
  const {
    openclmodal,
    setOpenclmodal,
    openInput,
    setOpenInput,
    isTeleOn,
    isOdlcOn,
    isOffAxisOn,
    isMapOn,
    isWayPoints,
    showRoverDrop,
    GotoEmergent,
    Latch, setLatch,Brake, setBrake,
    handleCloseInput,
    handleTelem,
    handleOdlc,
    handleOffAxis,
    handleMap,
    handleWaypoints,
    handleRoverdrop,
    handleGotoEmergent
  } = sidebarcontext;

  const context1 = useContext(homeContext);
  const { set_status } = context1;
  const [value, setValue] = useState(0);

  const [uploadedFileName, setUploadedFileName] = useState("");
  const [fileData, setFileData] = useState("");
  const [uploadedFile, setUploadedFile] = useState(); // send on backend as it is, inside req.body
  const [dataToSend, setDataToSend] = useState();
  const [checked, setChecked] = useState(true);
  const [getmissionid, setmissionid] = useState(false);
  const [missionIdValue, setMissionIdValue] = useState({ "missionid": "" });

  const [values, setValues] = useState({
    // textmask: "000.000.000.000",
    textmask: ""
  });

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleChangeMissionID = (e) => {
    setMissionIdValue({
      ...missionIdValue,
      [e.target.name]: e.target.value,
    });
  }

  const handleChangetext = (e) => {
    setValues({
      ...values,
      [e.target.name]: e.target.value,
    });
  };

  function kiasToMs() {
    let kias, ms;
    ms = 0.514444 * kias;
  }

  function msToKias() {
    let kias, ms;
    kias = ms / 0.514444;
  }

  const modalclose = () => {
    setOpenclmodal(false);
    setOpenInput(false);
    setmissionid(false);
  };

  const sendData = () => {
    let mission_id = "1:";
    setDataToSend(uploadedFile);
    // socket.emit("uploadMap", mission_id.concat(uploadedFileName));
    socket.emit("uploadMap", fileData)
  };

  const handleFile = (e) => {
    setUploadedFileName(e.target.files[0].name);
    setUploadedFile(e.target.files[0]);

    let reader = new FileReader();

    reader.onloadend = () => {
      setFileData(reader.result);
    };

    reader.readAsDataURL(e.target.files[0]);
  };

  const fetchMission = () => {
    set_status(1);
    socket.emit("fetchMission", missionIdValue.missionid);
    setmissionid(false);
  };

  const latching = () =>{
    setLatch(false);
    window.localStorage.setItem("Latch", false);
  }

  const disengageBrake = () => {
    setBrake(false);
    window.localStorage.setItem("Brake", false);
  }

  const unlatchRover = () => {
    setLatch(true)
    window.localStorage.setItem("Latch", true);
    socket.emit('sendCmd', "startUnlatchRover")
  }

  const engageBrake = () => {
    setBrake(true)
    window.localStorage.setItem("Brake", true);
    socket.emit('sendCmd', "startEngageBrake")
  }

  const dropRover = () => {
    socket.emit('sendCmd', "startDropSequence")
  }

  const incAltitude = () => {
    socket.emit('sendCmd', "incAlt")
  }

  return (
    <>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar style={{ height: "12vh" }} />
        <Box sx={{ backgroundColor: "transparent", height: "100%" }}>
          <Box sx={{ justifyContent: "center", display: "flex", border: 0 }}>
            <Tabs
              value={value}
              onChange={handleChange}
              sx={{ borderColor: "divider" }}
            >
              <Tab
                icon={
                  <img
                    style={{ minheight: "2.5vh", maxHeight: "3vh", height: "100%", paddingBottom: 4 }}
                    src="https://cdn-icons-png.flaticon.com/512/1812/1812583.png"
                    id="icondrone"
                    alt=""
                  />
                }
                label="Flight Info"
                {...a11yProps(0)}
              />
              <Tab
                icon={<ElectricCar sx={{ color: "white" }} />}
                label="UGV Info"
                {...a11yProps(1)}
              />
            </Tabs>
          </Box>
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            sx={{ display: "flex", mt: "3%", justifyContent: "center" }}
          >
            <Typography>kias</Typography>
            <FormControlLabel
              control={<Switch checked={checked} onChange={()=>{setChecked(!checked)}}/>}
            />
            <Typography>m/s</Typography>
          </Stack>
          <div className="sidebarbuttons">
            <TabPanel sx={{ height: "70vh" }} value={value} index={0}>
              <PlaneInfo checked={checked} />
            </TabPanel>
            <TabPanel value={value} index={1}>
              <UgvInfo checked={checked}/>
            </TabPanel>

            <Divider textAlign="left">Data</Divider>
            <div className="sidebarbtn1">
              <Button
                variant="contained"
                className="bts"
                endIcon={!isTeleOn ? <CheckIcon /> : <CloseIcon />}
                onClick={() => handleTelem()}
                sx={{ backgroundColor: isTeleOn ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                size="small"
              >
                Telem
              </Button>

              <Button
                variant="contained"
                endIcon={<DownloadIcon />}
                onClick={() => {
                  setmissionid(true);
                }}
                sx={{ color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                className="bts"
                size="small"
              >
                Mission
              </Button>
            </div>

            <Divider textAlign="left">Map</Divider>
            <Typography>{uploadedFileName}</Typography>

            <div className="sidebarbtn1">
              <label htmlFor="contained-button-file">
                <Inputfile
                  accept="image/*"
                  id="contained-button-file"
                  multiple
                  type="file"
                  size="small"
                  onChange={handleFile}
                />
                <Button
                  variant="contained"
                  component="span"
                  className="bts"
                  size="small"
                  sx={{ color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                >
                  Upload
                </Button>
              </label>
              <Button
                variant="contained"
                className="bts"
                size="small"
                endIcon={<SendIcon />}
                sx={{ color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                onClick={() => {
                  sendData()
                }}
              >
                Send
              </Button>
            </div>

            <Divider textAlign="left">Operations</Divider>
            <div className="sidebarbtn1">
              <Button
                variant="contained"
                className="bts"
                size="small"
                sx={{ backgroundColor: isOdlcOn ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                onClick={() => handleOdlc(isOdlcOn, "odlc")}
              >
                {isOdlcOn ? "Pause ODLC" : "ODLC"}
              </Button>
              <Button
                variant="contained"
                className="bts"
                size="small"
                color={isOffAxisOn ? "error" : "success"}
                sx={{ whiteSpace: "nowrap", backgroundColor: isOffAxisOn ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                onClick={() => handleOffAxis()}
              >
                {isOffAxisOn && "Pause"} {isOffAxisOn && <br />} OFF-AXIS
              </Button>
            </div>

            <div className="sidebarbtn1" style={{ marginBottom: '8% auto' }}>
              <Button
                variant="contained"
                className="bts"
                size="small"
                color={isMapOn ? "error" : "success"}
                sx={{ backgroundColor: isMapOn ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                onClick={() => handleMap()}
              >
                {isMapOn && "Pause"} {isMapOn && <br />}Map
              </Button>
              <Button
                variant="contained"
                className="bts"
                size="small"
                color={isWayPoints ? "error" : "success"}
                sx={{ whiteSpaces: "nowrap", backgroundColor: isWayPoints ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                onClick={() => handleWaypoints()}
              >
                {isWayPoints && "Pause"} {isWayPoints && <br />} Waypoints
              </Button>
            </div>

            <div className="sidebarbtn1" style={{ marginBottom: '4vh' }}>
              <Button
                variant="contained"
                className="bts"
                size="small"
                onClick={() => handleGotoEmergent()}
                sx={{ whiteSpace: "nowrap", backgroundColor: GotoEmergent ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550"}}
              >
                {GotoEmergent && "Pause"} {GotoEmergent && <br />} Emergent
              </Button>

              <Button
                variant="contained"
                className="bts"
                size="small"
                onClick={() => handleRoverdrop()}
                sx={{ whiteSpace: "nowrap", backgroundColor: showRoverDrop ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
              >
                {showRoverDrop && "Pause"} {showRoverDrop && <br />} Rover Drop
              </Button>
            </div>

            {showRoverDrop ? (
              <>
                <Divider textAlign="left">Rover Drop</Divider>
                <div className="sidebarbtn1" style={{ marginBottom: '8%' }}>
                  <Button variant="contained"
                    className="bts"
                    size="small"
                    sx={{ backgroundColor: Latch ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                    onClick={() => {Latch ? latching() : unlatchRover()}}>
                    Latch
                  </Button>

                  <Button variant="contained"
                    className="bts"
                    size="small"
                    sx={{ backgroundColor: Brake ? "#FF0266" : "#3BD16F", color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                    onClick={() => {Brake ? disengageBrake() : engageBrake() }}>
                    Brake
                  </Button>

                </div>

                <div className="sidebarbtn1" style={{ marginBottom: '25%' }}>

                  <Button variant="contained"
                    className="bts"
                    size="small"
                    endIcon={<ArrowUpwardIcon />}
                    sx={{ color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                    onClick={() => incAltitude()}
                  >
                    Alt
                  </Button>

                  <Button
                    variant="contained"
                    className="bts"
                    size="small"
                    sx={{ color: "white", fontSize: "0.9vw", fontWeight: "550" }}
                    onClick={() => dropRover()}
                  >
                    Start Sequence
                  </Button>
                </div>
              </>
            ) : null}
          </div>

          <Dialog
            open={openclmodal}
            // onClose={handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogBox />
          </Dialog>

          <Dialog
            open={openInput}
            onClose={modalclose}
            aria-labelledby="input-dialog-title"
            aria-describedby="input-dialog-description"
            maxWidth="xs"
            fullWidth
          >
            <DialogTitle id="input-dialog-title">{"IP Address"}</DialogTitle>
            <FormControl variant="standard" style={{ margin: "0.2rem 2rem 2rem 2rem" }}>
              <InputLabel htmlFor="formatted-text-mask-input">
                IP Address
              </InputLabel>
              <Input
                autoFocus
                value={values.textmask}
                onChange={handleChangetext}
                name="textmask"
                id="formatted-text-mask-input"
                inputComponent={TextMaskCustom}
              />
            </FormControl>

            <DialogActions>
              <Button onClick={() => setOpenInput(false)}>Cancel</Button>
              <Button onClick={() => handleCloseInput(values)} autoFocus>
                Submit
              </Button>
            </DialogActions>
          </Dialog>

          <Dialog
            open={getmissionid}
            onClose={modalclose}
            aria-labelledby="input-dialog-title"
            aria-describedby="input-dialog-description"
            maxWidth="xs"
            fullWidth
          >
            <DialogTitle id="input-dialog-title">{"Mission ID"}</DialogTitle>
            <TextField
              autoFocus
              value={missionIdValue.missionid}
              type="number"
              name="missionid"
              margin="dense"
              label="Mission ID"
              variant="standard"
              style={{ margin: "0.2rem 2rem 2rem 2rem" }}
              onChange={handleChangeMissionID}
            />
            <DialogActions>
              <Button onClick={() => setmissionid(false)}>Cancel</Button>
              <Button onClick={() => fetchMission()} autoFocus>
                Submit
              </Button>
            </DialogActions>
          </Dialog>
        </Box>
      </Drawer>
    </>
  );
}
