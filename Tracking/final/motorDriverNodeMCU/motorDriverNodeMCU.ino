/*
   e-Gizmo QMC5883L GY-271 Compass

   Sample sketch for the GY-271 QMC5883L
   for getting the raw data of x, y, z and
   Radius in degrees.

   Codes by e-Gizmo Mechatronix Central
   http://www.e-gizmo.com
   July 10,2017

*/

#include <WiFiClient.h>
#include <Wire.h>
#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>
#include <Wire.h>
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"


// Insert Firebase project API Key
#define API_KEY "AIzaSyA3sxz8LTLgtvdkvBAaLvZO7gBLqzuLM_A"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://rudra-x-default-rtdb.firebaseio.com/" 
WiFiServer server(80);
//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
float x, y;
bool signupOK = false;



/*// Insert your network credentials
#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"*/




int turnLeft;
int turnRight;
int stop1, start1;


void setup(){
  Serial.begin(115200);
  //pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  //pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  Wire.begin(D1,D2);


   server.begin(); 
  Serial.println("Server started");
}


void loop() {
  /*if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 5 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    if (Firebase.RTDB.getInt(&fbdo, "/following/turnLeft")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        turnLeft = fbdo.intData();
        //Serial.println(turnLeft);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    
    if (Firebase.RTDB.getFloat(&fbdo, "/following/turnRight")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        turnRight = fbdo.intData();
        //Serial.println(turnRight);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    if (Firebase.RTDB.getFloat(&fbdo, "/following/start1")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        start1 = fbdo.intData();
        //Serial.println(start1);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    if (Firebase.RTDB.getFloat(&fbdo, "/following/stop1")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        stop1 = fbdo.intData();

        //Serial.println(stop1);

        Serial.println(stop1);

      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }*/

//
//    if (Firebase.RTDB.getFloat(&fbdo, "/joystick/x")) {
//      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
//        x = fbdo.floatData();
//        Serial.print("x: ");
//        Serial.println(x);
//      }
//    }
//    else {
//      Serial.println(fbdo.errorReason());
//    }

//    if (Firebase.RTDB.getFloat(&fbdo, "/joystick/y")) {
//      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
//        y = fbdo.floatData();
//        Serial.print("y: ");
//        Serial.println(y);
//      }
//    }
//    else {
//      Serial.println(fbdo.errorReason());
//    }

    
  }

  
  int val;
 
  WiFiClient client = server.available();
  if(!client){
    return;
  }

  Serial.println("New Client");
  while(!client.available()){
    delay(1);
  }

  String req = client.readStringUntil('\r');
  req.replace("+", " ");          // Spaces without +
  req.replace(" HTTP/1.1", "");   // this delete HTTP/1.1
  req.replace("GET /", "");   
  val = req.toInt();
 /*if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 100 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    if (Firebase.RTDB.setInt(&fbdo, "magnet/dir", headingDegrees)){
      Serial.println("PASSED");
      //Serial.println("PATH: " + fbdo.dataPath());
      //Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  }*/
  //delay(100);
  
  


    if(turnLeft==0 && turnRight ==0){
      val = 1000;
  }
    if(turnLeft==1 && turnRight == 0){
      val = 1001;
  }
    if(turnLeft==0 && turnRight == 1){
      val = 1002;
  }
    if(stop1 == 0 && start1 == 1){
      val = 3000;
  }
    if(stop1 == 1 && start1 == 0){
      val = 3001;
  }
  
  

  byte buffer[10];
  buffer[0] = lowByte(val);
  buffer[1] = highByte(val);


  //Serial.println(val);
  Serial.println(val);
  Serial.println(start1);
  Wire.beginTransmission(8);
  Wire.write(buffer, 2);
  Wire.endTransmission();

  
}
