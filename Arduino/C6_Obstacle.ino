#include <NewPing.h>

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
int E1 = 5;  
int M1 = 4; 
int E2 = 6;                      
int M2 = 7; 
const byte interruptPin1 = 2;
volatile float count1 = 0;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void moveforward()
{
  digitalWrite(M1, 1); 
  digitalWrite(M2, 0);
  analogWrite(E1, 255);
  analogWrite(E2, 255);
}

void turnleft()
{
  digitalWrite(M1, 1); 
  digitalWrite(M2, 0);
  analogWrite(E1, 0); 
  analogWrite(E2, 255);  
}

void stop()
{
  analogWrite(E1, 0); 
  analogWrite(E2, 0);
}

void setup() 
{
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  for (int i = 4; i <= 7; i++) //Pin 4 to 7 are used
      pinMode(i, OUTPUT);
  pinMode(interruptPin1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin1), interruption1, CHANGE);
}

void loop() 
{
  delay(50);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  Serial.print("Ping: ");
  Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
  Serial.println("cm");
  if (count1 >= 20000)
  {
    stop();
  }
  else
  {
    if (sonar.ping_cm() <= 50)
    {
      turnleft();
    }
    else
    {
      moveforward();
    }
  }
  

}

void interruption1() 
{
  count1 = count1 + 1;
}