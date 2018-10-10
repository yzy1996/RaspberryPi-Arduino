const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = HIGH;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
  
  digitalWrite(ledPin, state);
  Serial.begin(9600);
}

void loop() {
  Serial.print("Working hard...");
  delay(1000);       
  Serial.print("done. State = ");
  Serial.println(state);
}

void blink() {
  state = !state;
  digitalWrite(ledPin, state);
}
