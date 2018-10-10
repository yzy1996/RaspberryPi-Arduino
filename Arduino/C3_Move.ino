//Note
//Pin 4 = Direction control for Motor 2
//Pin 5 = PWM control for Motor 2
//Pin 6 = PWM control for Motor 1
//Pin 7 = Direction control for Motor 1
int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7;  

void setup() {

  Serial.begin( 9600 );
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);

}

void loop() {

  if (Serial.available()) {
        char input = Serial.read();
        switch(input){
            case 'x':  //停止
                analogWrite(E1, 0); 
                analogWrite(E2, 0);
                break;
            case 'w':  //向前
                digitalWrite(M1, 1); 
                digitalWrite(M2, 0);
                analogWrite(E1, 255); 
                analogWrite(E2, 255);
                break;
            case 's':  //向后
                digitalWrite(M1, 0); 
                digitalWrite(M2, 1);
                analogWrite(E1, 255); 
                analogWrite(E2, 255);
                break;                
            case 'a':  //左转
                digitalWrite(M1, 1); 
                digitalWrite(M2, 0);
                analogWrite(E1, 0); 
                analogWrite(E2, 255);
                break;
            case 'd':  //右转
                analogWrite(M1, 1); 
                analogWrite(M2, 0);
                analogWrite(E1, 255); 
                analogWrite(E2, 0);
                break;
        }
     }
}


