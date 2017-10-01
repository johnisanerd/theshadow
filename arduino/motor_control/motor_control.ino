
// TimerOne will be used as an ISR interrupt to continuously check our switches
#include "TimerOne.h"   // Code     - https://code.google.com/archive/p/arduino-timerone/downloads
                        // Examples - https://playground.arduino.cc/Code/Timer1

#define m1_a 52  // M1 Forward   // Purple
#define m1_b 50  // M1 Backward  // Grey wire
#define m2_a 48  // M2 Forward   // Green
#define m2_b 46  // M2 Backward  // Blue
#define m3_a 44  // M3 Forward   // Orange
#define m3_b 42  // M3 Backward  // Yellow
#define m4_a 40  // M4 Forward   // Brown
#define m4_b 38  // M4 Backward  // Red

#define m4_forw_limit  23
#define m4_back_limit  27
#define m4_forw_mag    25
#define m4_back_mag    29

#define m3_forw_limit  31
#define m3_back_limit  35
#define m3_forw_mag    33
#define m3_back_mag    37

#define m2_forw_limit  39
#define m2_back_limit  43
#define m2_forw_mag    41
#define m2_back_mag    53

#define m1_forw_limit  45
#define m1_back_limit  49
#define m1_forw_mag    47
#define m1_back_mag    51

int status_m4_forw_limit = 0;
int status_m4_back_limit = 0;
int status_m4_forw_mag   = 0;
int status_m4_back_mag   = 0;

int status_m3_forw_limit = 0;
int status_m3_back_limit = 0;
int status_m3_forw_mag   = 0;
int status_m3_back_mag   = 0;

int status_m2_forw_limit = 0;
int status_m2_back_limit = 0;
int status_m2_forw_mag   = 0;
int status_m2_back_mag   = 0;

int status_m1_forw_limit = 0;
int status_m1_back_limit = 0;
int status_m1_forw_mag   = 0;
int status_m1_back_mag   = 0;

// Timeout Definition
// Any given function will run for no longer than the timeout time.  If it exceeds, we shut it down.
// For safety.
unsigned long timeout_time = 60000;   // Timeout if we run past 60 seconds.

// Choreography Start Variables
// These are the variables where we'll hold the data for choreography.
int m1_delay = 1000;  // Wait 1 second for the M1 to start
int m2_delay = 2000;  // Wait 2 seconds for M2 to start.  ETC
int m3_delay = 3000;
int m4_delay = 4000;

long last_command_in = 0;

bool debug = false;

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

  pinMode(m3_forw_limit, INPUT);
  pinMode(m3_back_limit, INPUT);
  pinMode(m3_forw_mag, INPUT);
  pinMode(m3_back_mag, INPUT);

  pinMode(m2_forw_limit, INPUT);
  pinMode(m2_back_limit, INPUT);
  pinMode(m2_forw_mag, INPUT);
  pinMode(m2_back_mag, INPUT);

  pinMode(m1_forw_limit, INPUT);
  pinMode(m1_back_limit, INPUT);
  pinMode(m1_forw_mag, INPUT);
  pinMode(m1_back_mag, INPUT);


  Timer1.initialize(1000);         // initialize timer1, call long microseconds=1000000
  Timer1.attachInterrupt(check_switches);  // attaches callback() as a timer overflow interrupt


  // Open serial communications and wait for port to open:
  Serial.begin(2000000);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  if(debug){Serial.println("Setup and initialized!");};

}

void check_switches(){
  status_m4_forw_limit = digitalRead(m4_forw_limit);
  status_m4_back_limit = digitalRead(m4_back_limit);
  status_m4_forw_mag   = digitalRead(m4_forw_mag);
  status_m4_back_mag   = digitalRead(m4_back_mag);

  status_m3_forw_limit = digitalRead(m3_forw_limit);
  status_m3_back_limit = digitalRead(m3_back_limit);
  status_m3_forw_mag   = digitalRead(m3_forw_mag);
  status_m3_back_mag   = digitalRead(m3_back_mag);

  status_m2_forw_limit = digitalRead(m2_forw_limit);
  status_m2_back_limit = digitalRead(m2_back_limit);
  status_m2_forw_mag   = digitalRead(m2_forw_mag);
  status_m2_back_mag   = digitalRead(m2_back_mag);

  status_m1_forw_limit = digitalRead(m1_forw_limit);
  status_m1_back_limit = digitalRead(m1_back_limit);
  status_m1_forw_mag   = digitalRead(m1_forw_mag);
  status_m1_back_mag   = digitalRead(m1_back_mag);


  if(debug){
    Serial.println(" - - - ");
    /* Serial.print("status_m4_forw_limit: "); */  Serial.print(status_m1_forw_limit, DEC);
    /* Serial.print("status_m4_back_limit: "); */ Serial.print(status_m1_back_limit, DEC);
    /* Serial.print("status_m4_forw_mag: "); */ Serial.print(status_m1_forw_mag, DEC);
    /* Serial.print("status_m4_back_mag: "); */ Serial.println(status_m1_back_mag, DEC);

    /* Serial.print("status_m4_forw_limit: "); */  Serial.print(status_m2_forw_limit, DEC);
    /* Serial.print("status_m4_back_limit: "); */ Serial.print(status_m2_back_limit, DEC);
    /* Serial.print("status_m4_forw_mag: "); */ Serial.print(status_m2_forw_mag, DEC);
    /* Serial.print("status_m4_back_mag: "); */ Serial.println(status_m2_back_mag, DEC);

    /* Serial.print("status_m4_forw_limit: "); */  Serial.print(status_m3_forw_limit, DEC);
    /* Serial.print("status_m4_back_limit: "); */ Serial.print(status_m3_back_limit, DEC);
    /* Serial.print("status_m4_forw_mag: "); */ Serial.print(status_m3_forw_mag, DEC);
    /* Serial.print("status_m4_back_mag: "); */ Serial.println(status_m3_back_mag, DEC);

    /* Serial.print("status_m4_forw_limit: "); */  Serial.print(status_m4_forw_limit, DEC);
    /* Serial.print("status_m4_back_limit: "); */ Serial.print(status_m4_back_limit, DEC);
    /* Serial.print("status_m4_forw_mag: "); */ Serial.print(status_m4_forw_mag, DEC);
    /* Serial.print("status_m4_back_mag: "); */ Serial.println(status_m4_back_mag, DEC);
    // delay(1000);
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
  delay(1000);    // Delay 1 second.  Prevents motor burnout.
}


////////////////////////////////////////////////////////////////////////////////////////

int sum_of_forward_switches(){
  check_switches();
  int sum = status_m4_forw_limit +
            status_m3_forw_limit +
            status_m2_forw_limit +
            status_m1_forw_limit +
            status_m4_forw_mag +
            status_m3_forw_mag +
            status_m2_forw_mag +
            status_m1_forw_mag;
  return sum;
}

int sum_of_forward_limit_switches(){
  check_switches();
  int sum = status_m4_forw_limit +
            status_m3_forw_limit +
            status_m2_forw_limit +
            status_m1_forw_limit;
  return sum;
}

void go_forward(){

  // Start the timer
  unsigned long time_start = millis();

  // Start running forward.  Get all the motors started!
  // We run everything forward as long as not limit switches are pushed.  This prevents
  // the magnets from overflowing from fwd to bwd and stopping everything.
  while(sum_of_forward_limit_switches() == 0){

      unsigned long time_now = millis()-time_start;
      if(debug){Serial.println(time_now, DEC);};

      if(time_now > m1_delay){
          // If the timer is greater than 1 second, start M1
          motor_fwd(m1_a, m1_b);
      }
      if(time_now > m2_delay){
          // If the timer is greater than 2 second, start M2
          motor_fwd(m2_a, m2_b);
      }
      if(time_now > m3_delay){
          // If the timer is greater than 3 second, start M3
          motor_fwd(m3_a, m3_b);
      }
      if(time_now > m4_delay){
          // If the timer is greater than 4 second, start M4
          motor_fwd(m4_a, m4_b);
      }
      unsigned long time_since_start = millis()-time_start;
      // Run in this state until we've passed all motor delays.
      if(
        (time_since_start > m4_delay+100) &&
        (time_since_start > m3_delay) &&
        (time_since_start > m2_delay) &&
        (time_since_start > m1_delay)
      ){
        break;
      }
  }

  // After the first switch is thrown start to shut everyone down.

  while((sum_of_forward_switches() < 4)){
    // Do nothing until switches are hit . . .
    if(status_m1_forw_mag || status_m1_forw_limit){
      motor_stop(m1_a, m1_b);
    }
    if(status_m2_forw_mag || status_m2_forw_limit){
      motor_stop(m2_a, m2_b);
    }
    if(status_m3_forw_mag || status_m3_forw_limit){
      motor_stop(m3_a, m3_b);
    }
    if(status_m4_forw_mag || status_m4_forw_limit){
      motor_stop(m4_a, m4_b);
    }

    unsigned long time_since_start = millis()-time_start;
    if(time_since_start > timeout_time){
      all_motors_stop();  // Shutdown all four motors.
      break;
    }
  }
  all_motors_stop();  // Shutdown all four motors.
}

int sum_of_backward_switches(){
  check_switches();
  int sum = status_m4_back_limit +
            status_m3_back_limit +
            status_m2_back_limit +
            status_m1_back_limit +
            status_m4_back_mag +
            status_m3_back_mag +
            status_m2_back_mag +
            status_m1_back_mag;
  return sum;
}

int sum_of_backward_limit_switches(){
  check_switches();
  int sum = status_m4_back_limit +
            status_m3_back_limit +
            status_m2_back_limit +
            status_m1_back_limit;
  return sum;
}

void go_backward(){

  // Start the timer
  unsigned long time_start = millis();

  // Start running forward.  As long as no backward switch has been pressed.
  unsigned long time_now = millis()-time_start;
  while((sum_of_backward_limit_switches() == 0) && (time_now < 1000)){

      time_now = millis()-time_start;
      if(debug){Serial.println(time_now, DEC); };
      motor_bwd(m1_a, m1_b);
      motor_bwd(m2_a, m2_b);
      motor_bwd(m3_a, m3_b);
      motor_bwd(m4_a, m4_b);
  }

  // After the first switch (magnetic or mechanical) is thrown start to shut everyone down.
  Serial.println(0, DEC); // !! DO NOT REMOVE!  FOR SOME REASON THE TIMING ON THIS WORKS.

  while((sum_of_backward_switches() < 4)){
    // Do nothing until switches are hit . . .
    // Serial.println(time_now, DEC);
    if(status_m1_back_mag || status_m1_back_limit){
      motor_stop(m1_a, m1_b);
    }
    if(status_m2_back_mag || status_m2_back_limit){
      motor_stop(m2_a, m2_b);
    }
    if(status_m3_back_mag || status_m3_back_limit){
      motor_stop(m3_a, m3_b);
    }
    if(status_m4_back_mag || status_m4_back_limit){
      motor_stop(m4_a, m4_b);
    }

    unsigned long time_since_start = millis()-time_start;
    if(time_since_start > timeout_time){
      all_motors_stop();  // Shutdown all four motors.
      break;
    }
  }
  all_motors_stop();  // Shutdown all four motors.
}


void get_status(){

	Serial.print(status_m1_forw_limit, DEC);
	Serial.print(status_m1_back_limit, DEC);
	Serial.print(status_m1_forw_mag, DEC);
	Serial.print(status_m1_back_mag, DEC);

	Serial.print(status_m2_forw_limit, DEC);
	Serial.print(status_m2_back_limit, DEC);
	Serial.print(status_m2_forw_mag, DEC);
	Serial.print(status_m2_back_mag, DEC);

	Serial.print(status_m3_forw_limit, DEC);
	Serial.print(status_m3_back_limit, DEC);
	Serial.print(status_m3_forw_mag, DEC);
	Serial.print(status_m3_back_mag, DEC);

	Serial.print(status_m4_forw_limit, DEC);
	Serial.print(status_m4_back_limit, DEC);
	Serial.print(status_m4_forw_mag, DEC);
	Serial.print(status_m4_back_mag, DEC);

	Serial.println(" ");
}

// We will call this function if we detect any of the mechanical
// limit switches pressed.  This is to give some more breathing
// room to the switches, prevent any drift from being called.
void back_off_limit_switches(){
  // Check if any switches are pressed, then run the motor
  // 0.5 seconds in the opposit direction.
  if(status_m1_forw_limit){motor_fwd(m1_a, m1_b); delay(100); motor_stop(m1_a, m1_b);};
  if(status_m2_forw_limit){motor_fwd(m2_a, m2_b); delay(100); motor_stop(m2_a, m2_b);};
  if(status_m3_forw_limit){motor_fwd(m3_a, m3_b); delay(100); motor_stop(m3_a, m3_b);};
  if(status_m4_forw_limit){motor_fwd(m4_a, m4_b); delay(100); motor_stop(m4_a, m4_b);};
  delay(2000);  // Not in a hurry here, keep it from overheating or getting stuck.
  
  if(status_m1_back_limit){motor_bwd(m1_a, m1_b); delay(100); motor_stop(m1_a, m1_b);};
  if(status_m2_back_limit){motor_bwd(m2_a, m2_b); delay(100); motor_stop(m2_a, m2_b);};
  if(status_m3_back_limit){motor_bwd(m3_a, m3_b); delay(100); motor_stop(m3_a, m3_b);};
  if(status_m4_back_limit){motor_bwd(m4_a, m4_b); delay(100); motor_stop(m4_a, m4_b);};
  delay(2000);  // Not in a hurry here, keep it from overheating or getting stuck.

}

void serialListen() {
  while (Serial.available()) {
    long inInt = Serial.parseInt();
    if((inInt == 1) || (inInt ==2) || (inInt ==3) || (inInt ==4)){
      last_command_in = inInt;
      Serial.println(inInt, DEC);
    }
  }
}


// Stop			- 1 - Stop
// Go Forward	- 2 - Initiate the going forward
// Go Backward	- 3 - Initiate the going backward
// Get Status	- 4 - Get status of all switches.

void loop()
{
  // NOTE: check_switches is called every 1,000 microseconds (us) with an intterupt.

  // Before we do anything else check if the limit switches are triggered.
  // If the limit switches are triggerd then back the rope away from them.
  while((sum_of_backward_limit_switches()+sum_of_forward_limit_switches() > 0)){
    back_off_limit_switches();
    
  }
  serialListen();
  if(last_command_in == 1){
	  if(debug){Serial.println("Received Command: Stop.");};
	  all_motors_stop();
  }
  else if(last_command_in == 2){
	  if(debug){Serial.println("Received Command Forward.");};
	  go_forward();
	  last_command_in = 1;
  }
  else if(last_command_in == 3){
	  if(debug){Serial.println("Received Command Backward.");};
	  go_backward();
	  last_command_in = 1;
  }
  else if(last_command_in == 4){
	  if(debug){Serial.println("Received Command Status.");};
	  get_status();
	  last_command_in = 1;
  }
  else{

  }
}


