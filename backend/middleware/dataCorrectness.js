

const checkJson = (req,res) => {
    let obj = JSON.parse(req.body.json);

    if (req.params.Type === "STANDARD") {

        if(obj.Alphanumeric) {
            // upload.single("file");
        } else {
            console.log("Can't save your details. Please try again!")
            return res.status(400).send("Can't save your details. Please try again!");
        }
  
      }
      else if (req.params.Type === "EMERGENT") {

        if(obj.Description) {
            // upload.single("file");
        } else {
            console.log("Can't save your details. Please try again!")
            return res.status(400).send("Can't save your details. Please try again!");
        }
      }

    next();
}

module.exports = checkJson;