int ledPin = 13; // LED connected to digital pin 13


int m1d1 = 23;   // Limit Switch - Motor 1, Direction 1
int m1d2 = 25;   // Limit Switch - Motor 1, Direction 2
int m2d1 = 27;   // Limit Switch - Motor 2, Direction 1
int m2d2 = 29;   // Limit Switch - Motor 2, Direction 2
int m3d1 = 31;   // Limit Switch - Motor 3, Direction 1
int m3d2 = 33;   // Limit Switch - Motor 3, Direction 2
int m4d1 = 35;   // Limit Switch - Motor 4, Direction 1
int m4d2 = 37;   // Limit Switch - Motor 4, Direction 2
int m5d1 = 39;   // Limit Switch - Motor 5, Direction 1
int m5d2 = 41;   // Limit Switch - Motor 5, Direction 2

int val = 0;     // variable to store the read value

void setup()
{
  pinMode(ledPin, OUTPUT);      // sets the digital pin 13 as output
  pinMode(m1d1, INPUT);      // sets the digital pin in
  pinMode(m1d2, INPUT);      // sets the digital pin in 
  pinMode(m2d1, INPUT);      // sets the digital pin  in
  pinMode(m2d2, INPUT);      // sets the digital pin  in
  pinMode(m3d1, INPUT);      // sets the digital pin  in
  pinMode(m3d2, INPUT);      // sets the digital pin  in
  pinMode(m4d1, INPUT);      // sets the digital pin  in
  pinMode(m4d2, INPUT);      // sets the digital pin  in
  pinMode(m5d1, INPUT);      // sets the digital pin  in
  pinMode(m5d2, INPUT);      // sets the digital pin  in
}

void check_limit_switches(){
  // Check status of limit switches.
  int m1d1_status = digitalRead(m1d1);   // read the input pin
  int m1d2_status = digitalRead(m1d2);   // read the input pin
  int m2d1_status = digitalRead(m2d1);   // read the input pin
  int m2d2_status = digitalRead(m2d2);   // read the input pin
  int m3d1_status = digitalRead(m3d1);   // read the input pin
  int m3d2_status = digitalRead(m3d2);   // read the input pin
  int m4d1_status = digitalRead(m4d1);   // read the input pin
  int m4d2_status = digitalRead(m4d2);   // read the input pin
  int m5d1_status = digitalRead(m5d1);   // read the input pin
  int m5d2_status = digitalRead(m5d2);   // read the input pin  

  
  // If any limits have been reached, shut down motors.
  if(m1d1 > 0){ /*stop motor*/};
  if(m1d2 > 0){ /*stop motor*/};
  if(m2d1 > 0){ /*stop motor*/};
  if(m2d2 > 0){ /*stop motor*/};
  if(m3d1 > 0){ /*stop motor*/};
  if(m3d2 > 0){ /*stop motor*/};
  if(m4d1 > 0){ /*stop motor*/};
  if(m4d2 > 0){ /*stop motor*/};
  if(m5d1 > 0){ /*stop motor*/};
  if(m5d2 > 0){ /*stop motor*/};
}

void loop()
{
  check_limit_switches();

  digitalWrite(ledPin, val);    // sets the LED to the button's value
}
