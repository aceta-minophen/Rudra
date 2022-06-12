/*Importing the packages we need*/
const express = require('express');
const path = require('path');

let initial_path = path.join(__dirname, "public"); //Store the public folder path inside a variable

const app = express(); //creating express.js server
app.use(express.static(initial_path)); //set public folder path to static path

app.get('/', (req, res) => {
    res.sendFile(path.join(initial_path, "light_switch.html"));
});

var admin = require("firebase-admin");

var serviceAccount = require("./rudra-x-firebase-adminsdk-e2s77-9f4eb01499.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://rudra-x-default-rtdb.firebaseio.com"
});

/*Running the server on port 8080*/
app.listen("8080", () => {
    console.log('listening.....');
})