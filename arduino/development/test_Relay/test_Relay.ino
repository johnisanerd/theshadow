int relay2 = 2;   // 1st relay
int relay3 = 3;   // 2nd relay

void setup()
{
  pinMode(relay2, OUTPUT);      // sets the digital pin as output
  pinMode(relay3, OUTPUT);
}

void fwd(){
  digitalWrite(relay2, HIGH);   // sets the LED on
  digitalWrite(relay3, LOW);
}

void bwd(){
  digitalWrite(relay2, LOW);    
  digitalWrite(relay3, HIGH);
}

void stp(){
  digitalWrite(relay2, HIGH);    
  digitalWrite(relay3, HIGH);
  delay(2000);
}

void loop()
{
  fwd();
  delay(5000);                  // waits for a second
  stp();

  bwd();
  delay(5000);                  // waits for a second
  stp();

}
