import React, { useContext } from "react";
import { Typography } from "@mui/material";
import "../Css/PlaneInfo.css"
import { SocketContext } from "../context/SocketContext";

function PlaneInfo(props) {
    const context = useContext(SocketContext);
    const {uavTelem } = context;

    return (
        <>
            {uavTelem && 
            <>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="span">
                    Latitude:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="span">
                    {uavTelem.uavLat}
                </Typography>
            </div>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="div">
                    Longitude:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="div">
                    {uavTelem.uavLon}
                </Typography>
            </div>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="div">
                    Altitude - AGL {props.checked ? "(m)" : "(feet)"}:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="div">
                {props.checked ? uavTelem.uavAlt.toFixed(4) : (uavTelem.uavAlt * 3.28084).toFixed(4)}
                </Typography>
            </div>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="div">
                    Altitude - MSL {props.checked ? "(m)" : "(feet)"}:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="div">
                {props.checked ? uavTelem.uavMslAlt.toFixed(4) : (uavTelem.uavMslAlt * 3.28084).toFixed(4)}
                </Typography>
            </div>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="div">
                    Air Speed {props.checked ? "(m/s)" : "(knots)"}:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="div">
                {props.checked ? uavTelem.uavSpeed.toFixed(3) : (uavTelem.uavSpeed * 1.94384).toFixed(3)}
                </Typography>
            </div>
            <div className="planedata">
                <Typography variant="subtitle1" gutterBottom component="div">
                    Ground Speed {props.checked ? "(m/s)" : "(knots)"}:
                </Typography>
                <Typography variant="subtitle1" gutterBottom component="div">
                {props.checked ? uavTelem.uavSpeed.toFixed(3) : (uavTelem.uavSpeed * 1.94384).toFixed(3)}
                </Typography>
            </div>
            </>
            }
        </>
    );
}

export default PlaneInfo;