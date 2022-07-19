// ---------------------------------------------------------------- //
// Arduino Ultrasoninc Sensor HC-SR04
// Re-writed by Arbi Abdul Jabbaar
// Using Arduino IDE 1.8.7
// Using HC-SR04 Module
// Tested on 17 September 2019
// ---------------------------------------------------------------- //

#define echoPin 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 9 //attach pin D3 Arduino to pin Trig of HC-SR04

// defines variables
long duration; // variable for the duration of sound wave travel
int distance1, distance2,distance3,i=0,totaldistance; // variable for the distance measurement

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");
}
void loop() {
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance1 = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

if (i==0)
{
  distance3 = distance1;
  i=1;
}
else if (i==1)
{
  distance2 = distance1;
  i=0;
}
  totaldistance= distance3- distance2;

  
  
  // Displays the distance on the Serial Monitor

 
  Serial.print("Distance1: ");
  Serial.print(distance1);
  Serial.println(" cm");

  Serial.print("Distance2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  Serial.print("Distance3: ");
  Serial.print(distance3);
  Serial.println(" cm");

  if (totaldistance>0)
  {
    Serial.print("Change Distance: ");
    Serial.print(totaldistance);
    Serial.println(" cm");
    Serial.println("coming near ");
  }
  
 else if (totaldistance<0)
  {
    Serial.print("Change Distance: ");
    Serial.print(totaldistance);
    Serial.println(" cm");
    Serial.println("going far ");
  }
  else 
  {
    Serial.println("No Change ");
  }
 
  

}
