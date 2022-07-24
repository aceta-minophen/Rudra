/**
 * Websocket server app
 *
 * Will use base64 return to the websocket clients and
 * in memory capturing without saving
 *
 */
//"use strict";

/* var port = 9090;

var HTTP = require("http");

var FS = require("fs");

var HTML_CONTENT = FS.readFileSync(__dirname + "/www/index2.html");

var WS = require("ws");

var WSS = new WS.Server({ port: 9091 }); */

/*Importing the packages we need*/
const express = require('express');
const path = require('path');

let initial_path = path.join(__dirname, "www"); //Store the public folder path inside a variable

const app = express(); //creating express.js server
app.use(express.static(initial_path)); //set public folder path to static path

app.get('/', (req, res) => {
    res.sendFile(path.join(initial_path, "index.html"));
})

/*Running the server on port 8080*/
/* app.listen("8080", () => {
    console.log('listening.....');
}) */

app.listen(3000, '192.168.29.45' || 'localhost', function () {
    console.log('Application worker ' + process.pid + ' started...');
}
);

// Broadcast to all.

/* WSS.broadcast = function broadcast(data) {

    WSS.clients.forEach(function each(client) {

        client.send(data);

    });

};

var NodeWebcam = require("node-webcam");

var Webcam = NodeWebcam.create({
    callbackReturn: "base64",
    saveShots: false
});


// Main

init();

function init() {

    setupHTTP();

    setupWebcam();

    console.log("Visit localhost:9090");

}

function setupHTTP() {

    var server = HTTP.createServer();

    server.on("request", function (request, response) {

        response.write(HTML_CONTENT);

        response.end();

    });

    server.listen(port);

}

function setupWebcam() {

    function capture() {

        Webcam.capture("picture", function (err, data) {

            if (err) {

                throw err;

            }

            WSS.broadcast(data);

            setTimeout(capture, 100);

        });

    }

    capture();

} */