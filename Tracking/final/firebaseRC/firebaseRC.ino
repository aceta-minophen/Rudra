
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
#define WIFI_SSID "Galaxy M219B55"
#define WIFI_PASSWORD "ussr1512"

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

// Motor A -- RIGHT
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 14;

float X, Y;

// Motor B -- LEFT
int motor2Pin1 = 25;
int motor2Pin2 = 33;
int enable2Pin = 32;

// Setting PWM properties
const int freq = 30000;
const int pwmChannelL = 0;
const int pwmChannelR = 0;
const int resolution = 8;
int dutyCycle = 230;

WiFiServer server(80); // Port 80

#define LED2 2 // LED2 is a Built-in LED.
String estado = "";
int wait30 = 30000; // time to reconnect when connection is lost.

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
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
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("ok");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  

  // Start Web Server.
  server.begin();
  Serial.println("Web Server started.");

  // Esta es la IP
  Serial.print("This is IP to connect to the WebServer: ");
  Serial.print("http://");
  Serial.println(WiFi.localIP());

  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

  // configure LED PWM functionalitites
  ledcSetup(pwmChannelL, freq, resolution);
  ledcSetup(pwmChannelR, freq, resolution);

  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannelR);
  ledcAttachPin(enable2Pin, pwmChannelL);
  
}

void loop() {
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 10 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();
    if (Firebase.RTDB.getInt(&fbdo, "/joystick/x")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int") {
        X = fbdo.floatData();
        //Serial.println(x);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }
    
    if (Firebase.RTDB.getFloat(&fbdo, "/joystick/y")) {
      if (fbdo.dataType() == "float" || fbdo.dataType() == "int") {
        Y = fbdo.floatData();
        //Serial.println(y);
      }
    }
    else {
      Serial.println(fbdo.errorReason());
    }
  }

  x=X*100;
  y=Y*100;

  Serial.print("x: ");
  Serial.print(x);
  Serial.print(",y: ");
  Serial.println(y); 

  if(y>=-10 && y<=10){
    stopMoving();
  }

  if(y>10 && x<-30){
    antiClockwiseFor();
  }

  if(y>10 && x>30){
    clockwiseFor();
  }

  if(y>10 && x>=-30 && x<=30){
    goForward(y);
  }


  if(y<-10 && x<-30){
    clockwiseBack();
  }

  if(y<-10 && x>30){
    antiClockwiseBack();
  }

  if(y<-10 && x>=-30 && x<=30){
    goBack(y);
  }

  /* Wire.beginTransmission(8);
  Wire.write(buffer, 2);
  Wire.endTransmission(); */

  //client.flush();
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
