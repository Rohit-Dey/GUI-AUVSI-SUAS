import React, { useState, useContext, useEffect } from "react";
import { Typography, Stack } from "@mui/material";
import { TextField } from "@mui/material";
import { Autocomplete } from "@mui/material";
import Button from "@mui/material/Button";
import MultiNavbar from "./Navbar";
import ImgCarousel from "./ImgCarousel";
import { styled } from "@mui/material/styles";
import homeContext from "../context/home/homeContext";
import "../Css/ZenMode.css";
import { Tab, Tabs, Box, Divider } from '@mui/material';
import PropTypes from 'prop-types';

const Colors = [
  { label: "" },
  { label: "WHITE" },
  { label: "BLACK" },
  { label: "GRAY" },
  { label: "RED" },
  { label: "BLUE" },
  { label: "GREEN" },
  { label: "YELLOW" },
  { label: "PURPLE" },
  { label: "ORANGE" },
  { label: "BROWN" },
];
const Shapes = [
  { label: "" },
  { label: "CIRCLE" },
  { label: "CROSS" },
  { label: "HEPTAGON" },
  { label: "HEXAGON" },
  { label: "OCTAGON" },
  { label: "PENTAGON" },
  { label: "QUARTER_CIRCLE" },
  { label: "RECTANGLE" },
  { label: "SEMICIRCLE" },
  { label: "SQUARE" },
  { label: "STAR" },
  { label: "TRAPEZOID" },
  { label: "TRIANGLE" },
];

const Input = styled("input")({
  display: "none",
});

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
      {value === index && <Box sx={{ py: 1, height: "100%" }}>{children}</Box>}
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

function ZenMode() {
  const context = useContext(homeContext);
  const {
    open,
    odlcformdata,
    setodlcformdata,
    emergentdata,
    setemergentdata,
    Updateodlc,
    Createobject,
    fetchimg,
    imgdata,
    setimgdata,
    formtype,
    setformtype,
    odlctype,
    setodlctype,
    update,
    setupdate,
    fillform,
    setfillform,
  } = context;

  const [shape, setshape] = useState({ label: "" });
  const [shapeColor, setshapeColor] = useState({ label: "" });
  const [alphanumericColor, setalphanumericColor] = useState({ label: "" });

  const [uploadedFileName, setUploadedFileName] = useState("");
  const [fileData, setFileData] = useState("");
  const [uploadedFile, setUploadedFile] = useState();

  const [value, setValue] = useState(0);
  const [standardCharacteristics, setStandardCharacteristics] = useState([]);
  const [standardImageJson, setStandardImageJson] = useState([]);
  const [emergentCharacteristics, setEmergentCharacteristics] = useState([]);
  const [emergentImageJson, setEmergentImageJson] = useState([]);
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handlefile = (e) => {
    setUploadedFile(e.target.files[0]);
    setUploadedFileName(e.target.files[0].name);
    let reader = new FileReader();

    reader.onloadend = () => {
      setFileData(reader.result);
    };

    reader.readAsDataURL(e.target.files[0]);
  };

  useEffect(() => {
    if (fillform && open && odlctype === "standard") {
      setUploadedFileName("");
      setUploadedFile("");
      setFileData("");
      setimgdata("");
      setshape({ label: odlcformdata.Shape })
      setshapeColor({ label: odlcformdata.Shape_Color })
      setalphanumericColor({ label: odlcformdata.Alphanumeric_Color })
      setfillform(false)
    }
  }, [fillform, odlcformdata]);

  const CancelForm = () => {
    setUploadedFileName("");
    setUploadedFile("");
    setFileData("");
    setimgdata("");
    setodlcformdata({
      fileid: "",
      Shape: "",
      Shape_Color: "",
      Alphanumeric: "",
      Alphanumeric_Color: "",
      Orientation: "",
      Latitude: "",
      Longitude: ""
    });
    setemergentdata({
      fileid: "",
      Description: "",
    });
    setalphanumericColor({ label: "" });
    setshapeColor({ label: "" });
    setshape({ label: "" });
    setformtype("new");
  };

  const handleshapeChange = (e, value) => {
    if (value) setshape({ label: value.label });
  };

  const handleshapeColorChange = (e, value) => {
    if (value) setshapeColor({ label: value.label });
  };

  const handlealphanumericColorChange = (e, value) => {
    if (value) setalphanumericColor({ label: value.label });
  };

  const onChange = (e) => {
    if (odlctype === "standard") {
      setodlcformdata({ ...odlcformdata, [e.target.name]: e.target.value });
    } else {
      setemergentdata({ ...emergentdata, [e.target.name]: e.target.value });
    }
  };

  const handleUpdate = async (id, type) => {
    let jsonData;
    if (type === "standard") {
      if (formtype === "edit") {
        jsonData = {
          Shape: shape.label,
          Shape_Color: shapeColor.label,
          Alphanumeric: odlcformdata.Alphanumeric,
          Alphanumeric_Color: alphanumericColor.label,
          Orientation: odlcformdata.Orientation
        };
      }
      else {
        jsonData = {
          Shape: shape.label,
          Shape_Color: shapeColor.label,
          Alphanumeric: odlcformdata.Alphanumeric,
          Alphanumeric_Color: alphanumericColor.label,
          Orientation: odlcformdata.Orientation,
          Latitude: odlcformdata.Latitude,
          Longitude: odlcformdata.Longitude
        };
      }
    } else {
      jsonData = {
        Description: emergentdata.Description,
      };
    }

    if (formtype === "edit") {
      Updateodlc(jsonData, id);
      CancelForm();
    } else {
      Createobject(jsonData, type.toUpperCase(), uploadedFile);
      CancelForm();
    }
  };

  useEffect(() => {
    fetchimg().then((imgdata) => {
      if ((standardCharacteristics.length === 0 && emergentCharacteristics.length === 0) || (imgdata.length !== (standardCharacteristics.length + emergentCharacteristics.length))) {
        setupdate(true)
      }
    })
  })


  useEffect(() => {
    fetchimg().then((imgdata) => {
      if (update) {
        const copyimgdata = JSON.parse(JSON.stringify(imgdata));
        let sc = [], ec = [], si = [], ei = [];
        copyimgdata.map((value, index) => {
          if (value.odlc.Type === "STANDARD") {
            sc.push(value.odlc);
            si.push(value.file.data);
          } else {
            ec.push(value.odlc);
            ei.push(value.file.data);
          }
          return ec, sc, si, ei;
        });
        setStandardCharacteristics(sc);
        setEmergentCharacteristics(ec);
        setStandardImageJson(si);
        setEmergentImageJson(ei);
        setupdate(false);
      }
    });
  }, [update]);

  return (
    <>
      <div className="zenContainer">
        <MultiNavbar />

        <Stack
          direction="row"
          sx={{
            alignItems: "center",
            mx: "auto",
          }}
          spacing={1}
        >
          <>
            <div className="formstandard">
              {odlctype === "emergent" ? (
                <>
                  <div className="inputfields">
                    <TextField
                      id="outlined-basic"
                      label="Description"
                      name="Description"
                      onChange={onChange}
                      multiline
                      value={emergentdata.Description}
                      sx={{ width: "100%" }}
                      margin="dense"
                      variant="outlined"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div className="inputfields">
                    <Autocomplete
                      id="combo-box-demo"
                      options={Shapes}
                      onChange={handleshapeChange}
                      value={shape}
                      size="small"
                      sx={{ width: "100%", mt: "7%" }}
                      renderInput={(params) => (
                        <TextField {...params} label="Shape" />
                      )}
                    />
                  </div>
                  <div className="inputfields">
                    <Autocomplete
                      id="combo-box-demo"
                      options={Colors}
                      onChange={handleshapeColorChange}
                      value={shapeColor}
                      size="small"
                      sx={{ width: "100%", mt: "3%" }}
                      renderInput={(params) => (
                        <TextField {...params} label="Shape Colour" />
                      )}
                    />
                  </div>
                  <div className="alphanumerictext inputfields">
                    <TextField
                      id="outlined-basic"
                      sx={{ width: "48%" }}
                      name="Alphanumeric"
                      onChange={onChange}
                      size="small"
                      value={odlcformdata.Alphanumeric}
                      label="AlphaNumeric"
                      margin="dense"
                      variant="outlined"
                    />
                    <TextField
                      id="outlined-basic"
                      label="Orientation"
                      name="Orientation"
                      onChange={onChange}
                      size="small"
                      value={odlcformdata.Orientation}
                      sx={{ width: "48%" }}
                      margin="dense"
                      variant="outlined"
                    />
                  </div>
                  <Autocomplete
                    id="combo-box-demo"
                    options={Colors}
                    onChange={handlealphanumericColorChange}
                    value={alphanumericColor}
                    sx={{ width: "100%", mt: "3%" }}
                    size="small"
                    renderInput={(params) => (
                      <TextField {...params} label="AlphaNumeric Colours" />
                    )}
                  />
                  {formtype === "new" &&
                    <div className="alphanumerictext inputfields">
                      <TextField
                        id="outlined-basic"
                        sx={{ width: "48%" }}
                        name="Latitude"
                        onChange={onChange}
                        size="small"
                        value={odlcformdata.Latitude}
                        label="Latitude"
                        margin="dense"
                        variant="outlined"
                      />
                      <TextField
                        id="outlined-basic"
                        label="Longitude"
                        name="Longitude"
                        onChange={onChange}
                        size="small"
                        value={odlcformdata.Longitude}
                        sx={{ width: "48%" }}
                        margin="dense"
                        variant="outlined"
                      />
                    </div>
                  }
                </>
              )}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "3%",
                }}
              >
                <Button
                  className="cancelbtn"
                  onClick={() => CancelForm()}
                  size="small"
                >
                  Cancel
                </Button>
                <Button
                  className="submitbtn"
                  onClick={() => {
                    odlctype === "emergent"
                      ? handleUpdate(emergentdata.fileid, odlctype)
                      : handleUpdate(odlcformdata.fileid, odlctype);
                  }}
                  size="small"
                >
                  Submit
                </Button>
              </div>
            </div>
            {formtype === "edit" ? (
              <>
                <img
                  src={`data:image/jpg;base64,${imgdata}`}
                  alt=""
                  style={{ width: "30vw", height: "40vh", margin: "0 10vw" }}
                />
              </>
            ) : (
              <>
                <div className="sidebarbtn">
                  <label htmlFor="drawer-upload-button">
                    <Input
                      accept="image/*"
                      id="drawer-upload-button"
                      multiple
                      type="file"
                      size="small"
                      onChange={handlefile}
                    />

                    <Button
                      variant="contained"
                      component="span"
                      className="btn"
                      size="small"
                      sx={{ ml: 0 }}
                    >
                      Upload
                    </Button>
                  </label>
                </div>

                <Typography
                  variant="p"
                  style={{ whiteSpace: "pre-line", color: "white" }}
                >
                  {uploadedFileName}
                </Typography>
              </>
            )}
          </>
        </Stack>

        <div>
          <Tabs
            value={value}
            onChange={handleChange}
            sx={{ mx: "auto", minHeight: "5vh", maxHeight: "5vh" }}
            // style={{margin: 'auto'}}
            centered
            className="odlctype"
          >
            <Tab
              label="Standard"
              sx={{ pt: "0%", pb: "1%", fontSize: 13, maxHeight: "3vh" }}
              {...a11yProps(0)}
            />
            <Tab
              label="Emergent"
              sx={{ pt: "0%", pb: "1%", fontSize: 13, maxHeight: "3vh" }}
              {...a11yProps(1)}
            />
          </Tabs>
          <Divider />
          <TabPanel value={value} index={0}>
            {standardImageJson.length !== 0 ? (
              <ImgCarousel
                images={standardImageJson}
                odlc={standardCharacteristics}
                slidesperview={5}
                type={"standard"}
              ></ImgCarousel>
            ) : (
              <Typography
                variant="h5"
                align="center"
                sx={{ py: "3.5%", color: "white" }}
                gutterBottom
                component="div"
              >
                No Images Found
              </Typography>
            )}
          </TabPanel>
          <TabPanel value={value} index={1}>
            {emergentImageJson.length !== 0 ? (
              <ImgCarousel
                images={emergentImageJson}
                odlc={emergentCharacteristics}
                slidesperview={5}
                type={"emergent"}
              ></ImgCarousel>
            ) : (
              <Typography
                variant="h5"
                align="center"
                sx={{ py: "3.5%" }}
                gutterBottom
                component="div"
              >
                No Images Found
              </Typography>
            )}
          </TabPanel>
        </div>
      </div>
    </>
  );
}

export default ZenMode;
