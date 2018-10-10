String recieve = "";

int E1 = 5;  //左轮
int M1 = 4; 
int E2 = 6;  //右轮              
int M2 = 7; 
int flagg = 1;
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
     if (Serial3.available())
     {
        char input = Serial3.read();
		if (input == 'm') //move
		{
			flagg = 1;
		}
		if (input == 'n') //auto 
		{
			flagg = 0;
		}
		if (flagg == 1)
		{
			switch(input){
				case 'x':  //停止
					{
					  analogWrite(E1, 0); 
					  analogWrite(E2, 0);
					  break;
					}
				case 'w':  //向前
					{
					  digitalWrite(M1, 1); 
					  digitalWrite(M2, 0);
					  analogWrite(E1, 240); 
					  analogWrite(E2, 255);
					  break;
					}
				case 's':  //向后
					{
					  digitalWrite(M1, 0); 
					  digitalWrite(M2, 1);
					  analogWrite(E1, 240); 
					  analogWrite(E2, 240);
					  break; 
					}
				case 'a':  //左转
					{
					  digitalWrite(M1, 1); 
					  digitalWrite(M2, 1);
					  analogWrite(E1, 120); 
					  analogWrite(E2, 120);
					  break;
					}
				case 'd':  //右转
					{
					  analogWrite(M1, 0); 
					  analogWrite(M2, 0);
					  analogWrite(E1, 120); 
					  analogWrite(E2, 120);
					  break;
					}
			}
		}
		if (flagg == 0)
		{
			switch(input){
            case 'x':  //停止
                {
                  analogWrite(E1, 0); 
                  analogWrite(E2, 0);
                  break;
                }
            case 'w':  //向前
                {
                  digitalWrite(M1, 1); 
                  digitalWrite(M2, 0);
                  analogWrite(E1, 190); 
                  analogWrite(E2, 200);
                  delay(600);
                  analogWrite(E1, 0); 
                  analogWrite(E2, 0);
                  break;
                  break;
                }
            case 's':  //向后
                {
                  digitalWrite(M1, 0); 
                  digitalWrite(M2, 1);
                  analogWrite(E1, 180); 
                  analogWrite(E2, 180);
                  delay(300);
                  analogWrite(E1, 0); 
                  analogWrite(E2, 0);
                  break;
                  break; 
                }
            case 'a':  //左转
                {
                  digitalWrite(M1, 1); 
                  digitalWrite(M2, 1);
                  analogWrite(E1, 150); 
                  analogWrite(E2, 150);
                  delay(200);
                  analogWrite(E1, 0); 
                  analogWrite(E2, 0);
                  break;
                }
            case 'd':  //右转
                {
                  analogWrite(M1, 0); 
                  analogWrite(M2, 0);
                  analogWrite(E1, 150); 
                  analogWrite(E2, 150);
                  delay(200);
                  analogWrite(E1, 0); 
                  analogWrite(E2, 0);
                  break;
                }
			}
		}
    }
}

