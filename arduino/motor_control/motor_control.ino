
int m1_a = 52;  // M1 Forward   // Purple
int m1_b = 50;  // M1 Backward  // Grey wire
int m2_a = 48;  // M2 Forward   // Green 
int m2_b = 46;  // M2 Backward  // Blue
int m3_a = 44;  // M3 Forward   // Orange
int m3_b = 42;  // M3 Backward  // Yellow
int m4_a = 40;  // M4 Forward   // Brown
int m4_b = 38;  // M4 Backward  // Red

int m4_forw_limit = 23;
int m4_back_limit = 27;
int m4_forw_mag   = 25;
int m4_back_mag   = 29;

int status_m4_forw_limit = false;
int status_m4_back_limit = false;
int status_m4_forw_mag   = false;
int status_m4_back_mag   = false;


bool debug = true;

void setup()
{
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

  pinMode(m4_forw_limit, INPUT);
  pinMode(m4_back_limit, INPUT);
  pinMode(m4_forw_mag, INPUT);
  pinMode(m4_back_mag, INPUT);

  // Open serial communications and wait for port to open:
  Serial.begin(2000000);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("Setup and initialized!");
  
}

void check_switches(){
  status_m4_forw_limit = digitalRead(m4_forw_limit);
  status_m4_back_limit = digitalRead(m4_back_limit);
  status_m4_forw_mag   = digitalRead(m4_forw_mag);
  status_m4_back_mag   = digitalRead(m4_back_mag);

  if(debug){
    Serial.println(" - - - ");
    /* Serial.print("status_m4_forw_limit: "); */  Serial.println(status_m4_forw_limit, DEC);
    /* Serial.print("status_m4_back_limit: "); */ Serial.println(status_m4_back_limit, DEC);
    /* Serial.print("status_m4_forw_mag: "); */ Serial.println(status_m4_forw_mag, DEC);
    /* Serial.print("status_m4_back_mag: "); */ Serial.println(status_m4_back_mag, DEC);   
  }
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
  // delay(2000);
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
  delay(1000);
}

void loop()
{
  check_switches();

  if(status_m4_forw_limit){
    motor_fwd(m4_a, m4_b);
  }
  else{
    motor_stop(m4_a, m4_b);
  }
  // delay(5000);                  // waits for a second
  // all_motors_stop();

}
