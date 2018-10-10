int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7;  
const byte interruptPin1 = 2;
const byte interruptPin2 = 3;
volatile float count1 = 0;
volatile float count2 = 0;

void setup() {
  
  Serial.begin(9600);
  pinMode(interruptPin1, INPUT_PULLUP);
  pinMode(interruptPin2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin1), interruption1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin2), interruption2, CHANGE);
  
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);
      
}

void loop() 
{
  
  if (Serial.available()) 
  {
      int input = Serial.read();
      int motor = Serial.parseInt();
      int distance = Serial.parseInt();
        
      while ((count1/100) < distance)
      {
        Serial.println(count1/100);
        Serial.println(distance);
        switch(input)
        {          //用来判断是前进还是后退
            case 'w':  //向前
            {
              Serial.println('w');
              switch(motor)
                {
                  case 1:   //slow
                    {
                      moveforward(50);
                      Serial.println("slow");
                      break;
                    }
                  case 2:   //medium
                    {
                      moveforward(150);
                      Serial.println("medium");
                      break;
                    }
                  case 3:   //max
                    {
                      moveforward(255);
                      Serial.println("max");
                      break;
                    }
                }
              break;
            }   
            case 's':  //向后
            {
              Serial.println('s');
              switch(motor)
                {
                  case 1:   //slow
                    {
                      movebackward(50);
                      break;
                    }
                  case 2:   //medium
                    {
                      movebackward(150);
                      break;
                    }
                  case 3:   //max
                    {
                      movebackward(255);
                      break;
                    }   
                }
              break;
            }
        }
      }
      stop();
  }

  
}

void interruption1() {
  count1 = count1 + 1;
}

void interruption2() {
  count2 = count2 + 1;
}

void judgestop(int count , float distance)
{
  while ((count/100) > distance)
      {
            analogWrite(E1, 0); 
            analogWrite(E2, 0);
            count = 0;
      }
}

void moveforward(int motor)
{
  digitalWrite(M1, 1); 
  digitalWrite(M2, 0);
  analogWrite(E1, motor);
  analogWrite(E2, motor);
}

void movebackward(int motor)
{
  digitalWrite(M1, 0); 
  digitalWrite(M2, 1);
  analogWrite(E1, motor);
  analogWrite(E2, motor);
}

void stop()
{
analogWrite(E1, 0); 
analogWrite(E2, 0);
count1 = 0;
}