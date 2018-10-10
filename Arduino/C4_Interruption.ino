const byte interruptPin1 = 2;
const byte interruptPin2 = 3;
volatile float count1 = 0;
volatile float count2 = 0;

void setup() {
  pinMode(interruptPin1, INPUT_PULLUP);
  pinMode(interruptPin2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin1), interruption1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(interruptPin2), interruption2, CHANGE);
  Serial.begin(9600);
}

void loop() {
  Serial.print("Left Distance = ");
  Serial.print(count1/200);
  Serial.print("cm | ");
  Serial.print("Right Distance =");
  Serial.print(count2/200);
  Serial.println("cm");
  delay(1000);
}

void interruption1() {
  count1 = count1 + 1;
}

void interruption2() {
  count2 = count2 + 1;
}
