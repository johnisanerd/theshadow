int relay2 = 2;   // 1st relay
int relay3 = 3;   // 2nd relay

int m1_a = 52;
int m1_b = 50;
int m2_a = 48;
int m2_b = 46;
int m3_a = 44;
int m3_b = 42;
int m4_a = 40;
int m4_b = 38;

void setup()
{
  pinMode(relay2, OUTPUT);      // sets the digital pin as output
  pinMode(relay3, OUTPUT);

  pinMode(m1_a, OUTPUT);
  pinMode(m1_b, OUTPUT);
  pinMode(m2_a, OUTPUT);
  pinMode(m2_b, OUTPUT);
  pinMode(m3_a, OUTPUT);
  pinMode(m3_b, OUTPUT);
  pinMode(m4_a, OUTPUT);
  pinMode(m4_b, OUTPUT);

  // Turn off all relays to start!
  digitalWrite(m1_a, HIGH);
  digitalWrite(m1_b, HIGH);
  digitalWrite(m2_a, HIGH);
  digitalWrite(m2_b, HIGH);
  digitalWrite(m3_a, HIGH);
  digitalWrite(m3_b, HIGH);
  digitalWrite(m4_a, HIGH);
  digitalWrite(m4_b, HIGH);
  
}

void m1_fwd(){
  // digitalWrite(relay2, HIGH);   // sets the LED on
  // digitalWrite(relay3, LOW);

  digitalWrite(m1_a, HIGH);   // sets the LED on
  digitalWrite(m1_b, LOW);
  
}

void m1_bwd(){
  // digitalWrite(relay2, LOW);    
  // digitalWrite(relay3, HIGH);
  digitalWrite(m1_a, LOW);    
  digitalWrite(m1_b, HIGH);
  
}

void m1_stp(){
  // digitalWrite(relay2, HIGH);    
  // digitalWrite(relay3, HIGH);

  digitalWrite(m1_a, HIGH);    
  digitalWrite(m1_b, HIGH);
  
  delay(2000);
}

void loop()
{
  m1_fwd();
  delay(5000);                  // waits for a second
  m1_stp();

  m1_bwd();
  delay(5000);                  // waits for a second
  m1_stp();

}
