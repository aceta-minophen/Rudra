/*
   e-Gizmo QMC5883L GY-271 Compass

   Sample sketch for the GY-271 QMC5883L
   for getting the raw data of x, y, z and
   Radius in degrees.

   Codes by e-Gizmo Mechatronix Central
   http://www.e-gizmo.com
   July 10,2017

*/



#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
/*#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"*/


#define WIFI_SSID "Suk"
#define WIFI_PASSWORD "suk@study789"

// Insert Firebase project API Key
#define API_KEY "AIzaSyA3sxz8LTLgtvdkvBAaLvZO7gBLqzuLM_A"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "https://rudra-x-default-rtdb.firebaseio.com/" 

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
float x, y;
bool signupOK = false;



#include <Wire.h>
#include <QMC5883L.h>

QMC5883L compass;

// Insert your network credentials
#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"




const int trigPin1 = 15;
const int echoPin1 = 2;


//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration1;
float distanceCm1;
float distanceInch;

String recog;


int X_save = 100000;
int Y_save = 100000;

int turnLeft = 0;
int turnRight = 0;


void setup(){
  Serial.begin(115200);
  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
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

  Wire.begin();
  compass.init();
}


void loop() {
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 5 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    if (Firebase.RTDB.getInt(&fbdo, "/Computer Vision/Face Recognition/User/Recognized")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        recog = fbdo.boolData();
        Serial.println(recog);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    
    /*if (Firebase.RTDB.getFloat(&fbdo, "/joystick/y")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int") {
        Y = fbdo.floatData();
        //Serial.println(y);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }*/
  }
  int x,y,z;
  compass.read(&x,&y,&z);

 // Calculate heading when the magnetometer is level, then correct for signs of axis.
  // Atan2() automatically check the correct formula taking care of the quadrant you are in
  float heading = atan2(y, x);

  float declinationAngle = 0.0404;
  heading += declinationAngle;
  // Find yours here: http://www.magnetic-declination.com/

   // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;

  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;

  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 


  Serial.print("x: ");
  Serial.print(x);
  Serial.print("    y: ");
  Serial.print(y);
  Serial.print("    z: ");
  Serial.print(z);
  Serial.print("    heading: ");
  Serial.print(heading);
  Serial.print("    Radius: ");
  Serial.print(headingDegrees);
  Serial.println();
  Serial.print("Fec rec: ");
  Serial.println(recog);

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

  if(recog=="true"){
    X_save = x;
    Y_save = y;
  }

  Serial.println(X_save);
  Serial.println(Y_save);

  if(y>=60000){
    if(x>X_save+20){
      turnLeft = 1;
      turnRight = 0;
    }
    else if (x<X_save-20){
      turnLeft = 0;
      turnRight = 1;
    }
    else{
      turnLeft = 0;
      turnRight = 0;
    }
  }
  else if(y<60000){
    if(x>X_save+20){
      turnLeft = 0;
      turnRight = 1;
    }
    else if (x<X_save-20){
      turnLeft = 1;
      turnRight = 0;
    }
    else{
      turnLeft = 0;
      turnRight = 0;
    }
  }

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 10 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    if (Firebase.RTDB.setInt(&fbdo, "following/turnLeft", turnLeft)){
      Serial.println("PASSED");
      //Serial.println("PATH: " + fbdo.dataPath());
      //Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  }

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 10 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // Write an Int number on the database path test/int
    if (Firebase.RTDB.setInt(&fbdo, "following/turnRight", turnRight)){
      Serial.println("PASSED");
      //Serial.println("PATH: " + fbdo.dataPath());
      //Serial.println("TYPE: " + fbdo.dataType());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  }
}
