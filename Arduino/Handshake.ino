// Pi to Arduino Serial Communication Test
String recieve = "";

void setup() {
// initialize both serial ports:
	Serial.begin(9600);
	Serial3.begin(9600);
}
void loop() {
// read from port 3, send to port 0:
	while (Serial3.available()) {
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
	}
// read from port 0, send to port 3:
	if (Serial.available()) {
		int inByte = Serial.read();
		Serial3.write("ack");
	}
}