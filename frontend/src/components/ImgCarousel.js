import React, { useState, useContext, useEffect } from 'react'
import {
    CardContent, Card, Typography, CardMedia, Stack, IconButton, DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Button,
    Dialog
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import "swiper/css/pagination";
import "swiper/css/navigation";
import { Pagination, Navigation } from "swiper";
import homeContext from "../context/home/homeContext";
import '../Css/ImgCarousel.css'


export default function ImgCarousel(props) {
    const context = useContext(homeContext);
    const { fillform, setfillform, setopen, setodlcformdata, setimgdata, setodlctype, setemergentdata, setformtype, DeleteObject } = context;
    const { images, odlc, type, swiperStyle, mySwiper, slidesperview } = props

    const [isHovered, setIsHovered] = useState(-1);
    const [opendelmodal, setOpendelmodal] = useState(false);
    const [delind, setdelind] = useState(-1);

    function handleClick(index) {
        setIsHovered(index);
    }

    function handleLeave() {
        setIsHovered(-1);
    }

    const opendrawer = (value, index, type) => {
        setimgdata(value);
        setodlctype(type)
        setformtype("edit")
        if (type === "standard") {
            const copyodlc = JSON.parse(JSON.stringify(odlc[index]));
            setodlcformdata({
                fileid: copyodlc.fileid,
                Shape: copyodlc.Shape,
                Shape_Color: copyodlc.Shape_Color,
                Alphanumeric: copyodlc.Alphanumeric,
                Alphanumeric_Color: copyodlc.Alphanumeric_Color,
                Orientation: copyodlc.Orientation,
            });
        }
        else {
            const copyodlc = JSON.parse(JSON.stringify(odlc[index]));
            setemergentdata({
                fileid: copyodlc.fileid,
                Description: copyodlc.Description
            })
        }
        setfillform(true);
        setopen(true);

    };

    const handleDelete = (index) => {
        setdelind(index)
        setOpendelmodal(true);
    }

    const delfinish = () => {
        DeleteObject(odlc[delind].fileid);
        setdelind(-1);
        setOpendelmodal(false);
    }

    return (
        <>
            <Swiper
                slidesPerView={slidesperview}
                spaceBetween={10}
                pagination={{
                    clickable: true,
                }}
                navigation={true}
                modules={[Pagination, Navigation]}
                className={mySwiper}
            >
                {odlc && images.map((value, index) => {
                    return (
                        <>
                            <SwiperSlide key={index} className={swiperStyle}>
                                <Card className="card" sx={{ height: "35vh" }}
                                    onMouseEnter={() => handleClick(index)}
                                    onMouseLeave={() => handleLeave()}
                                >
                                    <Stack direction="row" spacing={0} sx={{ position: "absolute", right: "0" }}>
                                        <IconButton size="small" onClick={() => opendrawer(value, index, type)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton size="small" onClick={() => handleDelete(index)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </Stack>

                                    {isHovered === index ?
                                        (odlc[index] &&
                                            <CardContent className="card-content" sx={{ pt: "15%" }}>
                                                {type === "emergent" &&
                                                    <>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                OdlcId:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Odlcid}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Description:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Description}
                                                            </Typography>
                                                        </div>
                                                    </>
                                                }
                                                {type === "standard" &&
                                                    <>
                                                    <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                OdlcId:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Odlcid}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Shape:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Shape}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Shape Color:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Shape_Color}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Alphanumeric:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Alphanumeric}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Alphanumeric Color:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Alphanumeric_Color}
                                                            </Typography>
                                                        </div>
                                                        <div className="planedata">
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                Orientation:
                                                            </Typography>
                                                            <Typography variant="subtitle2" gutterBottom component="div">
                                                                {odlc[index].Orientation}
                                                            </Typography>
                                                        </div>
                                                    </>
                                                }
                                            </CardContent>
                                        ) :
                                        (
                                            <>
                                                <CardMedia
                                                    className="image"
                                                    component="img"
                                                    sx={{ height: "35vh" }}
                                                    image={`data:image/jpg;base64,${value.toString()}`}
                                                />
                                            </>
                                        )}
                                </Card>
                            </SwiperSlide>
                        </>
                    );
                })}
            </Swiper>

            <Dialog
                open={opendelmodal}
                // onClose={handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"Do you want to continue?"}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        {"This action will stop the process."}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpendelmodal(false)}>No</Button>
                    <Button onClick={() => { delfinish() }}>Yes</Button>
                </DialogActions>
            </Dialog>
        </>
    )
}
