
const int reedSwitch = 8;
int flag = 0;

int countR = 0;


//Changing variables
int lastState = LOW;
int currentState;
unsigned long pressedTime = 0;
unsigned long releasedTime = 0;

//Calculating variables
float circ = 65.973; //inches
float speedi; //inches/sec
float speedm; //kmph... speedm = 0.0914 speedi


void setup() {

  Serial.begin(9600);
  pinMode(reedSwitch, INPUT);


  //led blink program
  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  currentState = digitalRead(reedSwitch);

  if(lastState == LOW && currentState == HIGH){
    pressedTime = millis();
    countR++;
    Serial.println(countR);
  } else if(lastState == HIGH && currentState == LOW){
    releasedTime = millis();
    
  }

  long pressDuration = releasedTime - pressedTime;

  if(pressDuration < 0){
    if(flag == 0){
      //countR++;
      //Serial.println(countR);
      flag = 1;
    } else if(flag == 1){
      //Serial.println(speedm);
      flag = 0;
    }
  }


  lastState = currentState;

}
