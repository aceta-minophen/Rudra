#include <Wire.h>

/* Define declination of location from where measurement going to be done. 
e.g. here we have added declination from location Pune city, India. 
we can get it from http://www.magnetic-declination.com */
#define Declination       -0.00669
#define hmc5883l_address  0x1E


void setup() {
  Serial.begin(9600); /* begin serial for debug */
  Wire.begin(D6, D5); /* join i2c bus with SDA=D6 and SCL=D5 of NodeMCU */
  hmc5883l_init();
}

void loop() {
  Serial.print("Heading Angle : ");
  Serial.println(hmc5883l_GetHeading());
  delay(150);
}

void hmc5883l_init(){   /* Magneto initialize function */
  Wire.beginTransmission(hmc5883l_address);
  Wire.write(0x00);
  Wire.write(0x70); //8 samples per measurement, 15Hz data output rate, Normal measurement 
  Wire.write(0xA0); //
  Wire.write(0x00); //Continuous measurement mode
  Wire.endTransmission();
  delay(500);
}

int hmc5883l_GetHeading(){
  int16_t x, y, z;
  double Heading;
  Wire.beginTransmission(hmc5883l_address);
  Wire.write(0x03);
  Wire.endTransmission();
  /* Read 16 bit x,y,z value (2's complement form) */
  Wire.requestFrom(hmc5883l_address, 6);
  x = (((int16_t)Wire.read()<<8) | (int16_t)Wire.read());
  z = (((int16_t)Wire.read()<<8) | (int16_t)Wire.read());
  y = (((int16_t)Wire.read()<<8) | (int16_t)Wire.read());

  Heading = atan2((double)y, (double)x) + Declination;
  if (Heading>2*PI) /* Due to declination check for >360 degree */
   Heading = Heading - 2*PI;
  if (Heading<0)    /* Check for sign */
   Heading = Heading + 2*PI;
  return (Heading* 180 / PI);/* Convert into angle and return */
}

/* Uncomment below function for reading status register */
uint8_t readStatus(){
  Wire.beginTransmission(hmc5883l_address);
  Wire.write(0x09);
  Wire.endTransmission();
  Wire.requestFrom(hmc5883l_address, 1);
  return (uint8_t) Wire.read();
}
