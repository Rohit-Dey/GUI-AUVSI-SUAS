require("dotenv").config({path: "../frontend/.env" });
const express = require("express");
const http = require("http")
const connection=require('./db')
const upload=require('./routes/upload')
const app = express()
const cors = require("cors");
const port = process.env.BACKEND_PORT;
connection();

const server = http.createServer(app);
const io = require("socket.io")(server,{
    cors:{
        origin:"*",
        method:["GET","POST"]
    }
});

app.use(cors());
app.use(express.json())

app.use('/api/file',upload)

app.get("/",(req,res)=>{
    res.send("Server running");
})

let telem_json = {};
app.get("/geojson",(req,res)=>{
    res.send(telem_json)
})

const pythToWeb = io.of("/");
const webToPyth = io.of("/wtp");

pythToWeb.use((socket, next) => {
    next();
})

webToPyth.use((socket, next) => {
    next();
})

pythToWeb.on('connection',(socket)=>{
    console.log("Python Connected")
    socket.on("join_room",(room) => {
        console.log(room," joined ptw")
        socket.join(room)

        //pythToWeb.to(room).emit('joined',"user joined");
    });    

    socket.on("messagetoreact",(data)=>{
        console.log("msg to react: here", data)//["1"]['MODE'])
        webToPyth.emit("sendtoreact",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    socket.on("interopMission",(data)=>{
        console.log("Mission Recieved from interop", data)//["1"]['MODE'])
        webToPyth.emit("missionFromInterop",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("autoPath",(data)=>{
        console.log("Automatic Path: ", data)//["1"]['MODE'])
        webToPyth.emit("aStarPath",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("autoSearchWp",(data)=>{
        console.log("Automatic Search Path: ", data)//["1"]['MODE'])
        webToPyth.emit("aStarOdlcPath",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("mappingWp",(data)=>{
        console.log("Automatic Map Path: ", data)//["1"]['MODE'])
        webToPyth.emit("aStarMapPath",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("mapUploadStatus",(data)=>{
        console.log("mapUploadStatus", data)//["1"]['MODE'])
        webToPyth.emit("mapUploadStatus",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("uavTelem",(data)=>{
        telem_json = {data}
        console.log("uavTelem: ", data)//["1"]['MODE'])
        webToPyth.emit("uavTelem",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("roverTelem",(data)=>{
        telem_json = {data}
        console.log("roverTelem: ", data)//["1"]['MODE'])
        webToPyth.emit("roverTelem",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("ugvTelem",(data)=>{
        telem_json = {data}
        console.log("ugvTelem: ", data)//["1"]['MODE'])
        webToPyth.emit("ugvTelem",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("taskConfirmation",(data)=>{
        console.log("taskConfirmation: ", data)//["1"]['MODE'])
        webToPyth.emit("taskConfirmation",data)
        //webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("msgtopython",(data)=>{ 
        console.log("")
        pythToWeb.to("Room1").emit('sendtopython',data)
    });

    socket.on('disconnect',()=>{
        pythToWeb.to("Room1").emit("disconnected");
    });
});

webToPyth.on('connection',(socket)=>{
    console.log("2 Con")
    socket.on("join_room",(room) => {
        console.log(room," joined wtp")
        socket.join(room)
    });   
    
    socket.on("messagetoreact",(data)=>{
        console.log("inwtp")
        webToPyth.to("Room1").emit("sendtoreact",data)
    });

    socket.on("msgtopython",(data)=>{ 
        console.log("To Python: ", data)
        pythToWeb.emit('sendtopython',data)
        //pythToWeb.to("Room1").emit('sendtopython',data)
    });
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    socket.on("fetchMission", (data) => { 
        console.log("Fetching Mission_ID: ", data)
        pythToWeb.emit('fetchMission', data) 
    });

    socket.on("uploadMap", (data) => { 
        console.log("Uploading Map ", data)
        pythToWeb.emit('uploadMap',data)
        //pythToWeb.to("Room1").emit('sendtopython',data)
    });

    socket.on("telemPipeline",(data)=>{ 
        console.log("Telem: ", data)
        pythToWeb.emit('controlUavTelem',data)
        // pythToWeb.emit('telemToReact',data)
        //pythToWeb.to("Room1").emit('sendtopython',data)
    });

    socket.on("sendTask",(data)=>{ 
        console.log("Task: ", data)
        pythToWeb.emit('sendTask', data)
        // pythToWeb.emit('telemToReact',data)
        //pythToWeb.to("Room1").emit('sendtopython',data)
    });

    socket.on("sendCmd",(data)=>{ 
        console.log("Command: ", data)
        pythToWeb.emit('sendCmd', data)
    });

    socket.on("dbUpdated", (data) =>{
        console.log("Db Updated: ", data)
        pythToWeb.emit('dbUpdated', data)
    })

    socket.on("addToDb", (data) =>{
        console.log("Added to DB: ", data)
        pythToWeb.emit('addToDb', data)
    })

    socket.on("deleteFromDb", (data) =>{
        console.log("Delete from DB: ", data)
        pythToWeb.emit('deleteFromDb', data)
    })


    // socket.on("RoverDropToPython",(data)=>{ 
    //     console.log("RoverDrop: in app.js ", data)
    //     pythToWeb.emit('RoverDrop',data)
    //     //pythToWeb.to("Room1").emit('sendtopython',data)
    // });

    socket.on('disconnect',()=>{
        webToPyth.to("Room1").emit("disconnected");
    });
});

server.listen(port,() => {
console.log(`App listening at http://localhost:${port}`)
});
