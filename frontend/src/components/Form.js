import React, { useState, useContext, useEffect } from 'react'
import homeContext from "../context/home/homeContext";
import { TextField, Typography } from "@mui/material"
import { Autocomplete } from "@mui/material";
import Button from '@mui/material/Button';
import { styled } from "@mui/material/styles";
import "../Css/Form.css"

const Colors = [
  { label: '' },
  { label: 'WHITE' },
  { label: 'BLACK' },
  { label: 'GRAY' },
  { label: 'RED' },
  { label: 'BLUE' },
  { label: "GREEN" },
  { label: 'YELLOW' },
  { label: 'PURPLE' },
  { label: 'ORANGE' },
  { label: 'BROWN' }
];
const Shapes = [
  { label: '' },
  { label: 'CIRCLE' },
  { label: 'CROSS' },
  { label: 'HEPTAGON' },
  { label: 'HEXAGON' },
  { label: 'OCTAGON' },
  { label: "PENTAGON" },
  { label: 'QUARTER_CIRCLE' },
  { label: 'RECTANGLE' },
  { label: 'SEMICIRCLE' },
  { label: 'SQUARE' },
  { label: 'STAR' },
  { label: 'TRAPEZOID' },
  { label: 'TRIANGLE' }
];

const Input = styled("input")({
  display: "none",
});

function Form() {
  const context = useContext(homeContext);
  const { fillform, setfillform, open, setopen, odlcformdata, setodlcformdata, emergentdata, setemergentdata, Updateodlc, Createobject, imgdata, setimgdata, formtype, setformtype, odlctype, setodlctype } = context;

  const [shape, setshape] = useState({ label: '' });
  const [shapeColor, setshapeColor] = useState({ label: '' });
  const [alphanumericColor, setalphanumericColor] = useState({ label: '' });

  const [uploadedFileName, setUploadedFileName] = useState("");
  const [fileData, setFileData] = useState("");
  const [uploadedFile, setUploadedFile] = useState();


  const closedrawer = () => {
    setopen(false)
    setUploadedFileName("")
    setUploadedFile()
    setFileData("")
    setodlcformdata({
      fileid: "",
      Shape: "",
      Shape_Color: "",
      Alphanumeric: "",
      Alphanumeric_Color: "",
      Orientation: "",
      Latitude:"",
      Longitude:""
    });
    setalphanumericColor({ label: '' });
    setshapeColor({ label: '' });
    setshape({ label: '' });
    setemergentdata({
      fileid: "",
      Description: "",
    });
  }

  const handlefile = (e) => {
    setUploadedFile(e.target.files[0])
    setUploadedFileName(e.target.files[0].name);
    let reader = new FileReader();

    reader.onloadend = () => {
      setFileData(reader.result);
    };

    reader.readAsDataURL(e.target.files[0]);
  }

  useEffect(() => {
    if (fillform && open && odlctype === "standard") {
      setshape({ label: odlcformdata.Shape })
      setshapeColor({ label: odlcformdata.Shape_Color })
      setalphanumericColor({ label: odlcformdata.Alphanumeric_Color })
      setfillform(false)
    }
  }, [fillform, odlcformdata])


  const handleshapeChange = (e, value) => {
    if (value)
      setshape({ label: value.label });
  };

  const handleshapeColorChange = (e, value) => {
    if (value)
      setshapeColor({ label: value.label });
  };

  const handlealphanumericColorChange = (e, value) => {
    if (value)
      setalphanumericColor({ label: value.label });
  };

  const onChange = (e) => {
    if (odlctype === "standard") {
      setodlcformdata({ ...odlcformdata, [e.target.name]: e.target.value });
    }
    else {
      setemergentdata({ ...emergentdata, [e.target.name]: e.target.value });
    }
  };

  const handleUpdate = async (id, type) => {
    let jsonData
    if (type === "standard") {
      if(formtype === "edit")
      {
        jsonData = {
          Shape: shape.label,
          Shape_Color: shapeColor.label,
          Alphanumeric: odlcformdata.Alphanumeric,
          Alphanumeric_Color: alphanumericColor.label,
          Orientation: odlcformdata.Orientation
        };
      }
      else
      { 
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
    }
    else {
      jsonData = {
        Description: emergentdata.Description
      }
    }

    if (formtype === "edit") {
      Updateodlc(jsonData, id);
      closedrawer()
    } else {
      Createobject(jsonData, type.toUpperCase(), uploadedFile);
      closedrawer()
    }
  }

  return (
    <>
      {(formtype === "edit") ? <><img
        src={`data:image/jpg;base64,${imgdata}`}
        alt=""
        style={{ width: "90%", height: "35vh" }}
      /></> :
        <div className="sidebarbtn inputfields">
          <label htmlFor="drawer-upload-file">
            <Input
              accept="image/*"
              id="drawer-upload-file"
              multiple
              type="file"
              size="small"
              onChange={handlefile}
            />
            <Button
              variant="contained"
              component="span"
              className="btn-form"
              size="small"
            >
              Upload
            </Button>
            {(uploadedFileName !== "") ? <Typography sx={{ my: '2', mx: 'auto' }}>
              {uploadedFileName}
            </Typography> : null}
          </label>
        </div>
      }
      {odlctype === "emergent" ? (
        <>
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
        </>
      ) : (
        <>

          <div className="inputfile">
            <Autocomplete
              id="combo-box-demo"
              options={Shapes}
              onChange={(e, value) => { handleshapeChange(e, value) }}
              value={shape}
              size="small"
              sx={{ width: '100%', mt: "7%" }}
              renderInput={(params) => <TextField {...params} label="Shape" />}
            />
          </div>
          <div className="inputfields">
            <Autocomplete
              id="combo-box-demo"
              options={Colors}
              onChange={(e, value) => { handleshapeColorChange(e, value) }}
              value={shapeColor}
              size="small"
              sx={{ width: "100%", mt: "3%" }}
              renderInput={(params) => <TextField {...params} label="Shape Colour" />}
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
            onChange={(e, value) => { handlealphanumericColorChange(e, value) }}
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
      )
      }
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: "3%" }}>
        <Button
          className="cancelbtn"
          onClick={() => closedrawer()}
          size="small"
        >
          Cancel
        </Button>
        <Button
          className="submitbtn"
          onClick={() => {
            odlctype === "emergent" ? 
            handleUpdate(emergentdata.fileid, odlctype):
            handleUpdate(odlcformdata.fileid, odlctype) 
          }}
          size="small"
        >
          Submit
        </Button>
      </div>
    </>
  )
}

export default Form