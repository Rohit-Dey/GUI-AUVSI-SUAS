import React, { useContext, useState } from 'react'
import homeContext from "./homeContext"
import { SocketContext } from '../SocketContext';

function HomeState(props) {
  const host = process.env.REACT_APP_BACKEND_CONN;

  const context = useContext(SocketContext);
  const { socket } = context;

  const [open, setopen] = useState(false);
  const [odlctype, setodlctype] = useState(null)
  const [opencarousel, setopencarousel] = useState(false)
  const [formtype, setformtype] = useState("new")
  const [markerchange, setmarkerchange] = useState(0)
  const [update,setupdate] = useState(true)
  const [mission_status,set_status]=useState(0)
  const [fillform,setfillform] = useState(false);
  

  const [odlcformdata, setodlcformdata] = useState({
    fileid: "",
    Shape: "",
    Shape_Color: "",
    Alphanumeric: "",
    Alphanumeric_Color: "",
    Orientation: "",
    Latitude:"",
    Longitude:""
  });
  const [emergentdata, setemergentdata] = useState({
    fileid: "",
    Description: ""
  })

  const [imgdata, setimgdata] = useState(null);

  const fetchimg = async () => {
    const url = `${host}/api/file/allimages`;
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const imgdata = await response.json();
    return imgdata;
  };

  const Updateodlc = async (jsonData, fileid) => {
    const url = `${host}/api/file/updateimage/${fileid}`;
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });
    const odlcdata = await response.json();
    socket.emit('dbUpdated', odlcdata)
    setopen(false);
    setupdate(true)
  }

  const Createobject = async (jsonData, objecttype, fileData) => {
    let formdata = new FormData();
    formdata.append("file", fileData);
    formdata.append("json", JSON.stringify(jsonData));

    const url = `${host}/api/file/upload/${objecttype}`;
    const response = await fetch(url, {
      method: "POST",
      headers: {},
      body: formdata,
    });
    const newobjdata = await response.json();
    socket.emit('addToDb', newobjdata)
    setodlcformdata({
      Shape: "",
      Shape_Color: "",
      Alphanumeric: "",
      Alphanumeric_Color: "",
      Orientation: ""
    })
    setopen(false);
    setupdate(true)
  }

  const DeleteObject = async (fileid) => {
    const url = `${host}/api/file/deleteimage/${fileid}`;
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const answer = await response.json();
    socket.emit('deleteFromDb', answer)
    console.log(answer)
    setupdate(true)
  }

  return (
    <homeContext.Provider value={{open, setopen,fillform,setfillform,update,mission_status,set_status,setupdate, emergentdata, setemergentdata, odlcformdata, setodlcformdata, fetchimg, Updateodlc, Createobject, DeleteObject, imgdata, setimgdata, odlctype, setodlctype, formtype, setformtype, opencarousel, setopencarousel,markerchange,setmarkerchange}}>
      {props.children}
    </homeContext.Provider>
  )
}

export default HomeState;