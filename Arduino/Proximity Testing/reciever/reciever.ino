const int trigPin = 9;
const int echoPin = 10;
// defines variables
long duration;
int distance, Pdistance;
void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
Serial.begin(9600); // Starts the serial communication
}
void loop() {
Pdistance=distance;
Calc();
distance= duration*0.034;
if (Pdistance==distance || Pdistance==distance+1 || Pdistance==distance-1  )
{
Serial.print("Measured Distance: ");
Serial.println(distance/2);
}
//Serial.print("Distance: ");
//Serial.println(distance/2);
delay(500);
}
void Calc()
{
duration=0;
Trigger_US();
while (digitalRead(echoPin)==HIGH);
delay(2);
Trigger_US();
duration = pulseIn(echoPin, HIGH);
}
void Trigger_US()
{
// Fake trigger the US sensor
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
}
