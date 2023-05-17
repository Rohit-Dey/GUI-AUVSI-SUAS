import React, { useEffect, useState, useContext } from 'react'
import PropTypes from 'prop-types';
import { styled } from '@mui/material/styles';
import { Drawer, Tab, Tabs, Box, Divider, Typography, IconButton, Toolbar, Container } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Form from "./Form";
import Sidebar from "./Sidebar";
import Mapping from "./Map";
import homeContext from "../context/home/homeContext";
import "../Css/Home.css"
import ImgCarousel from "./ImgCarousel";
import MultiNavbar from "./Navbar"

const drawerWidth = "25vw";
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
      {value === index && (
        <Box sx={{ p: 1}}>
          {children}
        </Box>
      )}
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

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

function Home() {
  const context = useContext(homeContext);
  
  const { open,setopen, opencarousel, setopencarousel,setodlcformdata,setemergentdata, fetchimg,update,setupdate} = context;

  const [value, setValue] = useState(0);
  const [standardCharacteristics, setStandardCharacteristics] = useState([]);
  const [standardImageJson, setStandardImageJson] = useState([]);
  const [emergentCharacteristics, setEmergentCharacteristics] = useState([]);
  const [emergentImageJson, setEmergentImageJson] = useState([]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
    // setIsHovered(-1);
  };

  const closedrawer = () => {
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
    setemergentdata({
      fileid: "",
      Description: "",
    });
    setopen(false);
  };
  

  useEffect(()=>{
    fetchimg().then((imgdata)=>{
        if((standardCharacteristics.length === 0 && emergentCharacteristics.length === 0) || (imgdata.length !== (standardCharacteristics.length + emergentCharacteristics.length))) 
        {
           setupdate(true)
        }
    })
  })


  useEffect(() => {
    fetchimg().then((imgdata) => {
      if (update) {
        const copyimgdata = JSON.parse(JSON.stringify(imgdata));
        let sc = [],ec = [],si = [],ei = [];
        copyimgdata.map((value, index) => {
          if (value.odlc.Type === 'STANDARD') {
            sc.push(value.odlc)
            si.push(value.file.data);
          }
          else {
            ec.push(value.odlc);
            ei.push(value.file.data);
          }
          return ec, sc, si, ei;
        })
        setStandardCharacteristics(sc);
        setEmergentCharacteristics(ec)
        setStandardImageJson(si);
        setEmergentImageJson(ei);
        setupdate(false)
      }
    });

  }, [update])

  return (
    <>
      <MultiNavbar />
      <Mapping />

      <Sidebar />
      <Drawer
        anchor="right"
        open={open}
        onClose={closedrawer}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar style={{height:"12vh"}}/>
        <Container sx={{ width: "25vw", mt: "6%", textAlign: "center" }}>
          <Form />
        </Container>
      </Drawer >

      <Drawer
        anchor="bottom"
        open={opencarousel}
        variant="persistent"
        className="imagedrawer"
      >
        <DrawerHeader sx={{ pl: "20vw", display: "flex", border: 0, minHeight: "3vh", maxHeight: "3vh" }}>
          <Tabs
            value={value}
            onChange={handleChange}
            sx={{ mx: "auto", minHeight: "5vh", maxHeight: "5vh" }}
            className="odlctype"
          >
            <Tab className='standardtab' label="Standard" sx={{ pt: "0%", pb: "1%", fontSize: 13, maxHeight: "3vh" }} {...a11yProps(0)} />
            <Tab label="Emergent" sx={{ pt: "0%", pb: "1%", fontSize: 13, maxHeight: "3vh" }} {...a11yProps(1)} />
          </Tabs>

          <IconButton onClick={closedrawer} sx={{ pt: 0 }}>
            <ExpandMoreIcon />
          </IconButton>
        </DrawerHeader>

        <Divider />
        <TabPanel value={value} index={0}>
          {standardImageJson.length !== 0 ?
            <ImgCarousel images={standardImageJson} odlc={standardCharacteristics} slidesperview={4} type={"standard"} swiperStyle='swiperslide' mySwiper='mySwiper'></ImgCarousel>
            :
            <Box sx={{ height: "30vh", ml: "15vw" }}>
              <Typography variant="h5" align='center' sx={{ py: "3.5%" }} gutterBottom component="div">
                No Images Found
              </Typography>
            </Box>
          }
        </TabPanel>
        <TabPanel value={value} index={1}>
          {emergentImageJson.length !== 0 ?
            <ImgCarousel images={emergentImageJson} odlc={emergentCharacteristics} slidesperview={4} type={"emergent"} swiperStyle='swiperslide' mySwiper='mySwiper'></ImgCarousel>
            :
            <Box sx={{ height: "30vh", ml: "15vw" }}>
              <Typography variant="h5" align='center' sx={{ py: "3.5%" }} gutterBottom component="div">
                No Images Found
              </Typography>
            </Box>
          }
        </TabPanel>
      </Drawer>
    </>
  );
}

export default Home;
