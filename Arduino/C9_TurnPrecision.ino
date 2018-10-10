#include <SparkFun_MAG3110.h>

MAG3110 mag = MAG3110(); //Instantiate MAG3110
int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7;  
int record = 0;
float ddgree;

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
    digitalWrite(M1, 0); 
    digitalWrite(M2, 1);
    analogWrite(E1, 0); 
    analogWrite(E2, 200);
  }
  else   //矫正好了
  {
    Serial.println("Calibrated!");
    analogWrite(E1, 0);   //停下来
    analogWrite(E2, 0);
    
    if (record == 0) {
      ddgree = mag.readHeading();  //保留最初的角度信息
      record = 1;
    }
    
    if (Serial.available()) {
        int input = Serial.read();
        int degree = Serial.parseInt();
        
        switch(input)
          {          //用来判断是前进还是后退
            case 'a':  //向左
            {
              while ((mag.readHeading()-ddgree) < degree)
              {
                digitalWrite(M1, 1); 
                digitalWrite(M2, 0);
                analogWrite(E1, 180); 
                analogWrite(E2, 0);
                record = 0;
              }
              analogWrite(E1, 0); 
              analogWrite(E2, 0);
              break;
            }
            
            case 'd':  //向右
            {
              while ((-mag.readHeading()+ddgree) < degree)
              {
                digitalWrite(M1, 1); 
                digitalWrite(M2, 0);
                analogWrite(E1, 0); 
                analogWrite(E2, 180);
                record = 0;
              }
              analogWrite(E1, 0); 
              analogWrite(E2, 0);
              break;
            }
          }
    }
  }

  Serial.print("Heading: ");
  Serial.println(mag.readHeading());
  Serial.println(ddgree);
  Serial.println("--------");
  delay(1000);
  
}
