const upload = require("../middleware/upload");
const express = require("express");
const router = express.Router();
const Grid = require("gridfs-stream");
const mongoose = require("mongoose");
const conn = mongoose.connection;
const suas_model = require('../models/odlc')
const checkJson = require('../middleware/dataCorrectness');
let gfs;

conn.once("open", function () {
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection("photos");
});

router.get("/findduplicate", async (req, res) => {
  // const obj = JSON.parse(req.body)
  const { Shape, Shape_color, Alphanumeric, Alphanumeric_Color, Orientation, Latitude, Longitude, Type } = req.body;

  const odlc = await suas_model.find({
    Shape: Shape,
    Shape_Color: Shape_color,
    Alphanumeric: Alphanumeric,
    Alphanumeric_Color: Alphanumeric_Color,
    Orientation: Orientation,
    Latitude: Latitude,
    Longitude: Longitude,
    Type: Type
  });

  res.status(200).json({ odlc })
})

router.get("/allimages", async (req, res) => {
  let files = await gfs.db.collection("photos.chunks").find({}).toArray();
  
  const promises = files.map(async (file) => {
    let odlc = await suas_model.findOne({ fileid: file.files_id });
    return {odlc,file};
  });

  const data_json = await Promise.all(promises)

   
  res.status(200).json(data_json)
 
})

router.put("/updateimage/:fileid", async (req, res) => {
  const { Shape, Shape_Color, Alphanumeric, Alphanumeric_Color, Orientation, Latitude, Longitude, Type, Description, Odlcid } = req.body;
  const new_odlc = {};

  if (Shape) {
    new_odlc.Shape = Shape;
  }

  if (Shape_Color) {
    new_odlc.Shape_Color = Shape_Color;
  }

  if (Alphanumeric_Color) {
    new_odlc.Alphanumeric_Color = Alphanumeric_Color;
  }

  if (Alphanumeric) {
    new_odlc.Alphanumeric = Alphanumeric;
  }

  if (Orientation) {
    new_odlc.Orientation = Orientation;
  }

  if (Latitude) {
    new_odlc.Latitude = Latitude;
  }

  if (Longitude) {
    new_odlc.Longitude = Longitude;
  }

  if (Type) {
    new_odlc.Type = Type;
  }

  if(Description)
  { 
    new_odlc.Description = Description;
  }

  if(Odlcid)
  {
    new_odlc.Odlcid = Odlcid;
  }

  console.log(new_odlc);

  let odlc = await suas_model.findOne({ fileid: req.params.fileid });
  if (!odlc) {
    return res.status(404).send("Not Found");
  }

  odlc = await suas_model.findOneAndUpdate({ fileid: req.params.fileid }, { $set: new_odlc })
  let xodlc = await suas_model.findOne({ fileid: req.params.fileid });

  res.status(200).json({ xodlc });
})

router.get("/singleimage/:fileid", async (req, res) => {
  let chunk = await gfs.db.collection("photos.chunks").find({files_id: mongoose.Types.ObjectId(req.params.fileid)}).toArray()
  // let chunk = await gfs.db.collection("photos.chunks").find({ files_id: mongoose.Types.ObjectId(req.params.fileid) }.toArray();
  let odlc = await suas_model.findOne({ fileid: req.params.fileid});
  res.json({ chunk,odlc })

});

router.delete("/deleteimage/:fileid", async (req, res) => {
  let success = false;
  try {
    const delodlc = await suas_model.findOne({fileid:req.params.fileid})
    await suas_model.deleteOne({fileid:req.params.fileid})

    await gfs.db.collection("photos.chunks").remove({ files_id: mongoose.Types.ObjectId(req.params.fileid) }).catch(err => {
      return res.status(404).send('file not found')
    });

    await gfs.db.collection("photos.files").remove({_id : mongoose.Types.ObjectId(req.params.fileid)}).catch(err => {
      return res.status(404).send('file not found')
    });
    success = true;
    
    res.status(200).json({success,odlcid: delodlc.Odlcid});
  } catch (error) {
    console.log(error);
    res.send("An error occured.");
  }
});

router.get('/odlc_latlon',async(req, res)=>{
  const xodlc=await suas_model.find({},{Latitude:1,Longitude:1,Shape:1})
  res.status(200).json({xodlc})
})
// checkJson
router.post("/upload/:Type", upload.single("file"), async (req, res) => {
  let success = false;
  try {
    if (req.file === undefined) return res.send("you must select a file.");
    const obj = JSON.parse(req.body.json)
    console.log(obj);
    let odlc
    if (req.params.Type === "STANDARD") {
      const { Shape, Shape_Color, Alphanumeric, Alphanumeric_Color, Orientation, Latitude, Longitude, Odlcid} = obj;
      odlc = new suas_model({
        fileid: req.file.id,
        Shape,
        Shape_Color,
        Alphanumeric,
        Alphanumeric_Color,
        Orientation,
        Latitude,
        Longitude,
        Type: req.params.Type,
        Odlcid
      });

    }
    else if (req.params.Type === "EMERGENT") {
      const { Description,Odlcid } = obj;
      odlc = new suas_model({
        fileid: req.file.id,
        Description,
        Type: req.params.Type,
        Odlcid
      })
    }
    await odlc.save();
    success = true;
    res.status(200).json({ success,fileid:req.file.id });
  }
  catch {
    res.status(404).json({ success }); 
  }
});

module.exports = router;