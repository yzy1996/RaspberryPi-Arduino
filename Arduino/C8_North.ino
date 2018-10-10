#include <SparkFun_MAG3110.h>

MAG3110 mag = MAG3110(); //Instantiate MAG3110
int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7;  

void setup() {
  Serial.begin(9600);
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);
  mag.initialize(); //Initialize the MAG3110
}

void loop() {

  int x, y, z;

  if(!mag.isCalibrated()) //If we're not calibrated
  {
    if(!mag.isCalibrating()) //And we're not currently calibrating
    {
      Serial.println("Entering calibration mode");
      mag.enterCalMode(); //This sets the output data rate to the highest possible and puts the mag sensor in active mode
    }
    else
    {
      mag.calibrate(); 
    }
  }
  else
  {
    Serial.println("Calibrated!");
  }
  mag.readMag(&x, &y, &z);

  Serial.print("X: ");
  Serial.print(x);
  Serial.print(", Y: ");
  Serial.print(y);
  Serial.print(", Z: ");
  Serial.println(z);

  Serial.print("Heading: ");
  Serial.println(mag.readHeading());
  Serial.println("--------");
  if (abs(mag.readHeading()-20) >= 10)
  {
    digitalWrite(M1, 1); 
    digitalWrite(M2, 0);
    analogWrite(E1, 0); 
    analogWrite(E2, 180);
  }
  else
  {
    analogWrite(E1, 0); 
    analogWrite(E2, 0);
    Serial.println("oh my god");
  }
  delay(100);
  
}
