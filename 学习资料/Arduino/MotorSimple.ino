//Note
//Pin 4 = Direction control for Motor 2
//Pin 5 = PWM control for Motor 2
//Pin 6 = PWM control for Motor 1
//Pin 7 = Direction control for Motor 1
int E1 = 5;  
int M1 = 4; 
int E2 = 6;                      
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
            case '1':
                analogWrite(E1, 0); //0 power == stop
                analogWrite(E2, 0);
                break;
            case '2':
                analogWrite(E1, 191); //191 = 75% power
                analogWrite(E2, 191);
                break;
           case '3':
                analogWrite(E1, 255); //255 = max power
                analogWrite(E2, 255);
                break;

        }
     }
}


