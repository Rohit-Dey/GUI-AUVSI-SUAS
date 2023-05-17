import React, { useContext } from "react";
import { Typography } from "@mui/material";
import "../Css/PlaneInfo.css"
import { SocketContext } from "../context/SocketContext";

function UgvInfo(props) {
    const context = useContext(SocketContext);
    const { ugvTelem } = context;

    return (
        <>
            {ugvTelem &&
                <>
                    <div className="planedata">
                        <Typography variant="subtitle1" gutterBottom component="div">
                            Latitude:
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom component="div">
                            {ugvTelem.ugvLat}
                        </Typography>
                    </div>
                    <div className="planedata">
                        <Typography variant="subtitle1" gutterBottom component="div">
                            Longitude:
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom component="div">
                            {ugvTelem.ugvLon}
                        </Typography>
                    </div>
                    <div className="planedata">
                        <Typography variant="subtitle1" gutterBottom component="div">
                            Yaw:
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom component="div">
                            {ugvTelem.ugvYaw}
                        </Typography>
                    </div>
                    <div className="planedata">
                        <Typography variant="subtitle1" gutterBottom component="div">
                            Ground Speed {props.checked ? "(m/s)" : "(knots)"}:
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom component="div">
                            {props.checked ? ugvTelem.ugvSpeed.toFixed(3) : (ugvTelem.ugvSpeed * 1.94384).toFixed(3)}
                        </Typography>
                    </div>
                </>
            }
        </>
    );
}

export default UgvInfo;