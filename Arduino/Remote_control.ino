String recieve = "";

int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7; 

int flag = 0;

void setup() {
// initialize both serial ports:
	Serial.begin(9600);
	Serial3.begin(9600);
	for (int i = 4; i <= 7; i++) 
    pinMode(i, OUTPUT);
}
void loop() 
{
  if (flag == 0)   //shake hand
  {
    Serial.print("waiting!");
  	while (Serial3.available())  //读取Arduino传过来的
  	{
		  recieve += char(Serial3.read());
	  }
	
	  if (!recieve.compareTo("hello"))
	  {
	    Serial3.write("ack");
	    Serial.print("connecting!");
	    recieve = "";
	  }
	  
	  else if (!recieve.compareTo("ack"))
	  {
	    Serial.print("connecting ok!");
	    recieve = "";
	    flag = 1;
	  }
	  
	  if (Serial.available()) 
    {
		  int inByte = Serial.read();
		  Serial3.write("ack");
	  }
  }
  
  if (flag == 1)   //control move
  {
     if (Serial3.available())
     {
        char input = Serial3.read();
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
                analogWrite(E1, 240); 
                analogWrite(E2, 240);
                break;                
            case 'a':  //左转
                digitalWrite(M1, 1); 
                digitalWrite(M2, 1);
                analogWrite(E1, 120); 
                analogWrite(E2, 120);
                break;
            case 'd':  //右转
                analogWrite(M1, 0); 
                analogWrite(M2, 0);
                analogWrite(E1, 120); 
                analogWrite(E2, 120);
                break;
        }
    }
  }
}

