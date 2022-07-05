// Motor A -- RIGHT
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 14;

int x, y;

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

#include <WiFi.h>
const char *ssid = "paya1";
const char *password = "naina123";

WiFiServer server(80); // Port 80

#define LED2 2 // LED2 is a Built-in LED.
String estado = "";
int wait30 = 30000; // time to reconnect when connection is lost.

void setup()
{
  Serial.begin(115200);
  pinMode(LED2, OUTPUT);

  // Connect WiFi net.
  Serial.println();
  Serial.print("Connecting with ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected with WiFi.");

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

void loop()
{
  // If disconnected, try to reconnect every 30 seconds.
  if ((WiFi.status() != WL_CONNECTED) && (millis() > wait30))
  {
    Serial.println("Trying to reconnect WiFi...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    wait30 = millis() + 30000;
  }
  // Check if a client has connected..
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }

  /* Serial.print("New client: ");
  Serial.println(client.remoteIP()); */

  // Espera hasta que el cliente envíe datos.
  // while(!client.available()){ delay(1); }

  /////////////////////////////////////////////////////
  // Read the information sent by the client.
  String req = client.readStringUntil('\r');
  /* Serial.println(req); */

  /* // Make the client's request.
       if (req.indexOf("gpio/1") != -1) {digitalWrite(LED2, HIGH); estado = "ON";}
       if (req.indexOf("gpio/0") != -1){digitalWrite(LED2, LOW); estado = "OFF";}
     if (req.indexOf("consulta") != -1){
         if (digitalRead(LED2)){estado = "LED2 now is ON";}
         else {estado = "LED2 now is OFF";}
          }

  //////////////////////////////////////////////
  //  WEB PAGE. ////////////////////////////
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  Important.
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<head><meta charset=utf-8></head>");
  client.println("<body><center><font face='Arial'>");
  client.println("<h1>Servidor web con ESP32.</h1>");
  client.println("<h2><font color='#009900'>KIO4.COM - Juan A. Villalpando</font></h2>");
  client.println("<h3>Página web.</h3>");
  client.println("<br><br>");
  client.println("<a href='gpio/0'><button>Click to ON LED2</button></a>");
  client.println("<a href='gpio/1'><button>Click to OFF LED2</button></a>");
  client.println("<a href='consulta'><button>Consult status LED2</button></a>");
  client.println("<br><br>");
  client.println(estado);
  client.println("</font></center></body></html>");

  Serial.print("Client disconnected: ");
  Serial.println(client.remoteIP());
  client.flush();
  client.stop(); */

  req.replace("+", " ");        // Spaces without +
  req.replace(" HTTP/1.1", ""); // this delete HTTP/1.1
  req.replace("GET /", "");
  int val = req.toInt();

  byte buffer[10];
  buffer[0] = lowByte(val);
  buffer[1] = highByte(val);

  //Serial.println(val);

  

  if (val <= 200)
  {
    x = 100 - val;
  }

  if (val > 200 && val <= 400)
  {
    y = val - 300;
  }

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

  client.flush();
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
