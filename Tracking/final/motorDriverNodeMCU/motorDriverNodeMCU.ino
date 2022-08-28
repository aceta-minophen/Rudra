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


/*// Insert your network credentials
#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"*/




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
    if (Firebase.RTDB.getInt(&fbdo, "/following/turnLeft")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        turnLeft = fbdo.intData();
        Serial.println(turnLeft);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }

    
    if (Firebase.RTDB.getFloat(&fbdo, "/following/turnRight")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int" || fbdo.dataType() == "bool" || fbdo.dataType() == "string") {
        turnRight = fbdo.intData();
        Serial.println(turnRight);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }
  }

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
    
  }

  
}

void stopMoving()
{
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);

  Serial.println("stop");
}

void goForward(int y)
{
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);

  float speedL = 0.85 * y + 145;
  float speedR = 0.80 * y + 140;

  ledcWrite(pwmChannelL, speedL);
  ledcWrite(pwmChannelR, speedR);

  Serial.println("Moving forward");
}

void goBack(int y)
{
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);

  float speedR = (-y) + 145;
  float speedL = 0.80 * (-y) + 140;

  ledcWrite(pwmChannelL, speedL);
  ledcWrite(pwmChannelR, speedR);

  Serial.println("Moving backward");
}

void clockwiseFor()
{
  // left motor on, right off

  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);

  ledcWrite(pwmChannelL, 200);
  ledcWrite(pwmChannelR, 200);

  Serial.println("Clockwise forward");
}

void antiClockwiseFor()
{
  // left off, right on

  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);

  ledcWrite(pwmChannelL, 200);
  ledcWrite(pwmChannelR, 200);

  Serial.println("Anti Clockwise forward");
}

void clockwiseBack()
{
  // left off, right on

  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);

  ledcWrite(pwmChannelL, 200);
  ledcWrite(pwmChannelR, 200);

  Serial.println("Clockwise backward");
}

void antiClockwiseBack()
{
  // left on, right off

  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);

  ledcWrite(pwmChannelL, 200);
  ledcWrite(pwmChannelR, 230);

  Serial.println("Anti Clockwise backward");
}
