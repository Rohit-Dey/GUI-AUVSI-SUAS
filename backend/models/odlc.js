const mongoose=require('mongoose');
const storage=require('../middleware/upload');

const odlc=new mongoose.Schema({
    Shape:{
        type: String,
    },
    Shape_Color:{
        type:String,
    },
    Alphanumeric:{
        type:String
    },
    Alphanumeric_Color:{
        type:String,
    },
    Orientation:{
        type:String,
    },
    Latitude:{
        type:String,
    },
    Longitude:{
        type:String,
    },
    Type:{
        type:String,
        require:true
    },
    Description:{
        type:String,
    },
    Odlcid:{
        type:Number,
        require: true,
    },
    fileid:{
        type:mongoose.Schema.Types.ObjectId,
        ref:'photos.files'
    }
})
const suas_model=new mongoose.model('characteristics',odlc);
module.exports=suas_model;