const multer = require("multer");
const path = require("path");
const {GridFsStorage} = require('multer-gridfs-storage');

const storage = new GridFsStorage({
    url: process.env.DB_URL,
    options: { useNewUrlParser: true, useUnifiedTopology: true },
    file: (req, file) => {
        const match = ["image/png", "image/jpeg"];

        if (match.indexOf(file.mimetype) === -1) {
            const filename = `${Date.now()}${file.originalname}`;
            return filename;
        }

        return {
            bucketName: "photos",
            filename: `${Date.now()}${file.originalname}`,
        };
    }

});

module.exports = multer({storage});