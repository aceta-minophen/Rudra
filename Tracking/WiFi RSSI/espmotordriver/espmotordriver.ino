// Motor A
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 14;

// Motor B
int motor2Pin1 = 25;
int motor2Pin2 = 33;
int enable2Pin = 32;

// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 230;

void setup()
{
    // sets the pins as outputs:
    pinMode(motor1Pin1, OUTPUT);
    pinMode(motor1Pin2, OUTPUT);
    pinMode(enable1Pin, OUTPUT);
    pinMode(motor2Pin1, OUTPUT);
    pinMode(motor2Pin2, OUTPUT);
    pinMode(enable2Pin, OUTPUT);

    // configure LED PWM functionalitites
    ledcSetup(pwmChannel, freq, resolution);

    // attach the channel to the GPIO to be controlled
    ledcAttachPin(enable1Pin, pwmChannel);
    ledcAttachPin(enable2Pin, pwmChannel);

    Serial.begin(115200);

    // testing
    Serial.print("Testing DC Motor...");
}

void loop()
{
    // Move the DC motor forward at maximum speed
    /*Serial.println("Moving Forward");
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    delay(20000);

    // Stop the DC motor
    Serial.println("Motor stopped");
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    delay(1000);

    // Move DC motor backwards at maximum speed
    Serial.println("Moving Backwards");
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    delay(20000);*/

    // Stop the DC motor
    Serial.println("Motor stopped");
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
    delay(1000);

    // Move DC motor forward with increasing speed
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
    while (dutyCycle >= 140)
    {
        ledcWrite(pwmChannel, dutyCycle);
        Serial.print("Forward with duty cycle: ");
        Serial.println(dutyCycle);
        dutyCycle = dutyCycle - 5;
        delay(10000);
    }
    dutyCycle = 230;

    delay(1000);
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
    while (dutyCycle >= 140)
    {
        ledcWrite(pwmChannel, dutyCycle);
        Serial.print("backward with duty cycle: ");
        Serial.println(dutyCycle);
        dutyCycle = dutyCycle - 5;
        delay(10000);
    }
    dutyCycle = 230;
}
