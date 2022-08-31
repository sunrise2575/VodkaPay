const express = require("express");
const path = require("path");
const app = express();
var port = 8002;
app.use("/", express.static(path.join(__dirname, "../frontend/build/")));
app.listen(port, () => console.log(`listen ${port}`));
