import React, { useState, useContext, useEffect } from "react";
import {
    Typography,
    Box,
    IconButton,
    MenuItem,
    Menu,
    AppBar,
    Toolbar,
    Button,
} from "@mui/material";
import Battery3BarIcon from "@mui/icons-material/Battery3Bar";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import MoreIcon from "@mui/icons-material/MoreVert";
import "../Css/Navbar.css";
import homeContext from "../context/home/homeContext";
import OpenInBrowserIcon from "@mui/icons-material/OpenInBrowser";
import BrowserUpdatedIcon from "@mui/icons-material/BrowserUpdated";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import OfflineBoltOutlinedIcon from '@mui/icons-material/OfflineBoltOutlined';
import { useLocation,Link } from 'react-router-dom';
import { SocketContext } from "../context/SocketContext";
import Timer from "./Timer";
import AddPhotoAlternateIcon from '@mui/icons-material/AddPhotoAlternate';


function MultiNavbar() {
    const context1 = useContext(SocketContext);
    const { socket, uavTelem } = context1;
    let location = useLocation();
    const { pathname } = location;

    const context = useContext(homeContext);
    const {
        opencarousel,
        setopencarousel,
        setopen,
        setformtype,
        setodlctype,
        setemergentdata,
        setodlcformdata,
        setimgdata,
        setfillform
    } = context;

    const [anchorEl, setAnchorEl] = React.useState(null);
    const opennewobj = Boolean(anchorEl);
    const [mobileMoreAnchorEl, setMobileMoreAnchorEl] = useState(null);

    const isMobileMenuOpen = Boolean(mobileMoreAnchorEl);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleMobileMenuClose = () => {
        setMobileMoreAnchorEl(null);
    };

    const handleMobileMenuOpen = (event) => {
        setMobileMoreAnchorEl(event.currentTarget);
    };

    const newobj = (type) => {
        setAnchorEl(null);
        setimgdata(null);
        setodlctype(type);
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
        setformtype("new")
        setfillform(true);
        setopen(true);
    };

    const mobileMenuId = "primary-search-account-menu-mobile";
    const renderMobileMenu = (
        <Menu
            anchorEl={mobileMoreAnchorEl}
            anchorOrigin={{
                vertical: "top",
                horizontal: "right",
            }}
            id={mobileMenuId}
            keepMounted
            transformOrigin={{
                vertical: "top",
                horizontal: "right",
            }}
            open={isMobileMenuOpen}
            onClose={handleMobileMenuClose}
        >
            <MenuItem>
                <IconButton size="large" aria-label="show 4 new mails" color="inherit">
                    Menu
                </IconButton>
                <p>Messages</p>
            </MenuItem>
        </Menu>
    );

    return (
        <>
            <AppBar position="relative" sx={{ zIndex: 1202 }}>
                <Toolbar>
                    <img src="./images/uasdtulogo.png" alt="" style={{height:"8vh",margin:"1vh 0"}}/>
                    <Box sx={{ flexGrow: 1 }} />
                    <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
                    {uavTelem &&
                        <div className="arm" style={{alignItems:"center",marginRight:"3%"}}>{uavTelem.uavArmed ? "ARMED" : "DISARM"}</div>
                    }
                        <div className='time'>
                            <AccessTimeIcon />
                            <div className="timer"><Timer /></div>
                        </div>
                        {uavTelem &&
                            <>
                                <div className='battery'>
                                    <OfflineBoltOutlinedIcon />
                                    <div className="batterypercent">{uavTelem.uavBattery.current}A</div>
                                </div>
                                <div className="Voltage">
                                    <Battery3BarIcon />
                                    <div className="voltagevalue">{uavTelem.uavBattery.voltage}V</div>
                                </div>
                                <div className="mode">{uavTelem.uavMode}</div>
                            </>
                        }
                    </Box>

                    <Box sx={{ flexGrow: 1 }} />
                    <Box sx={{ display: { xs: "none", md: "flex" } }}>
                        <IconButton
                            id="basic-button"
                            aria-controls={opennewobj ? 'basic-menu' : undefined}
                            aria-haspopup="true"
                            aria-expanded={opennewobj ? 'true' : undefined}
                            onClick={handleClick}
                            sx={{ color: 'white' }}
                        >
                            <AddPhotoAlternateIcon/>
                        </IconButton>
                        <Menu
                            id="basic-menu"
                            anchorEl={anchorEl}
                            open={opennewobj}
                            onClose={handleClose}
                            MenuListProps={{
                                'aria-labelledby': 'basic-button',
                            }}
                        >
                            <MenuItem onClick={() => {
                                newobj("standard");
                            }}>
                                Standard Object
                            </MenuItem>
                            <MenuItem onClick={() => {
                                newobj("emergent");
                            }}>
                                Emergent Object
                            </MenuItem>
                        </Menu>
                        {pathname !== "/odlc" && 
                        (
                        <>
                        <IconButton
                            size="large"
                            aria-label="open image slide"
                            color="inherit"
                            onClick={() => {
                                setopencarousel(!opencarousel);
                            }}
                        >
                            {!opencarousel ? <OpenInBrowserIcon /> : <BrowserUpdatedIcon />}
                        </IconButton>
                        <IconButton
                            size="large"
                            edge="end"
                            aria-label="open in new tab"
                            color="inherit"
                            sx={{ m: "auto" }}
                            component={Link}
                            to='/odlc' 
                            target="_blank"                         
                        >
                            <OpenInNewIcon />
                        </IconButton>
                        </>)
                        }
                    </Box>

                    <Box sx={{ display: { xs: "flex", md: "none" } }}>
                        <IconButton
                            size="large"
                            aria-label="show more"
                            aria-controls={mobileMenuId}
                            aria-haspopup="true"
                            onClick={handleMobileMenuOpen}
                            color="inherit"
                        >
                            <MoreIcon />
                        </IconButton>
                    </Box>
                </Toolbar>
            </AppBar>
            {renderMobileMenu}
        </>
    );
}

export default MultiNavbar;
