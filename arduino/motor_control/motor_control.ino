int relay2 = 2;   // 1st relay
int relay3 = 3;   // 2nd relay

int m1_a = 52;  // M1 Forward   // Purple
int m1_b = 50;  // M1 Backward  // Grey wire
int m2_a = 48;  // M2 Forward   // Green 
int m2_b = 46;  // M2 Backward  // Blue
int m3_a = 44;  // M3 Forward   // Orange
int m3_b = 42;  // M3 Backward  // Yellow
int m4_a = 40;  // M4 Forward   // Brown
int m4_b = 38;  // M4 Backward  // Red

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

void motor_fwd(int a, int b){
  digitalWrite(a, HIGH);   // sets the LED on
  digitalWrite(b, LOW);
}

void motor_bwd(int a, int b){
  digitalWrite(a, LOW);   // sets the LED on
  digitalWrite(b, HIGH);
}

void motor_stop(int a, int b){\
  digitalWrite(a, HIGH);    
  digitalWrite(b, HIGH);
  delay(2000);
}

void all_motors_stop(){
  digitalWrite(m1_a, HIGH);
  digitalWrite(m1_b, HIGH);
  digitalWrite(m2_a, HIGH);    
  digitalWrite(m2_b, HIGH);
  digitalWrite(m3_a, HIGH);    
  digitalWrite(m3_b, HIGH);
  digitalWrite(m4_a, HIGH);    
  digitalWrite(m4_b, HIGH);
}

void loop()
{
  motor_fwd(m1_a, m1_b);
  motor_fwd(m2_a, m2_b);
  motor_fwd(m3_a, m3_b);
  motor_fwd(m4_a, m4_b);
  delay(5000);                  // waits for a second
  motor_stop(m1_a, m1_b);
  motor_stop(m2_a, m2_b);
  motor_stop(m3_a, m3_b);
  motor_stop(m4_a, m4_b);
    
  motor_bwd(m1_a, m1_b);
  motor_bwd(m2_a, m2_b);
  motor_bwd(m3_a, m3_b);
  motor_bwd(m4_a, m4_b);  
  delay(5000);                  // waits for a second
  all_motors_stop();
  delay(1000);
}
