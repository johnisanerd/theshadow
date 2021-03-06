
// TimerOne will be used as an ISR interrupt to continuously check our switches
#include "TimerOne.h"   // Code     - https://code.google.com/archive/p/arduino-timerone/downloads
                        // Examples - https://playground.arduino.cc/Code/Timer1

// Timeout Definition
// Any given function will run for no longer than the timeout time.  If it exceeds, we shut it down.
// For safety.
unsigned long timeout_time = 10000; // Timeout if we run past 15 seconds. // 60000;   // Timeout if we run past 60 seconds.

// Choreography Start Variables
// These are the variables where we'll hold the data for choreography.
int m1_delay = 000;  // Wait 1 second for the M1 to start
int m2_delay = 1000;  // Wait 2 seconds for M2 to start.  ETC
int m3_delay = 4000;
int m4_delay = 3000;

int forward_state_machine[4] = {0,0,0,0};   // This should be reset each cycle.
                                            // 0 means it hasn't been triggered yet.
                                            // 1 means it has been triggered this cycle.

#define m1_a 52  // M1 Forward   // Purple
#define m1_b 50  // M1 Backward  // Grey wire
#define m2_a 48  // M2 Forward   // Green
#define m2_b 46  // M2 Backward  // Blue
#define m3_a 44  // M3 Forward   // Orange
#define m3_b 42  // M3 Backward  // Yellow
#define m4_a 40  // M4 Forward   // Brown
#define m4_b 38  // M4 Backward  // Red

#define m4_forw_limit  27
#define m4_back_limit  23
#define m4_forw_mag    29
#define m4_back_mag    25

#define m3_forw_limit  35
#define m3_back_limit  31
#define m3_forw_mag    37
#define m3_back_mag    33

#define m2_forw_limit  43
#define m2_back_limit  39
#define m2_forw_mag    53
#define m2_back_mag    41

#define m1_forw_limit  49
#define m1_back_limit  45
#define m1_forw_mag    51
#define m1_back_mag    47

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

void delay_minutes(int minutes){
  for(int i = 0; i < minutes; i++){
    for(int x = 0; x < 60; x++){
      delay(1000); // Delays 1 second
    }
  }
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

  // Set State Machine
  // We'll set the state machine whenever a switch is triggered, magnetic or physical.
  // This is reset each time we send a run-forward command.  
  if(forward_state_machine[0] == 0){                  // Only check if the state machine hasn't been triggered.
                                                      // If it's already been triggered, don't reset it.
    if(status_m1_back_limit || status_m1_back_mag){   // If either switch (Mag or Mech) has been triggered, 
     forward_state_machine[0] = 1;                    // Set the state machine to triggered.
    }
  }
  if(forward_state_machine[1] == 0){
    if(status_m2_back_limit || status_m2_back_mag){
      forward_state_machine[1] = 1;
    }
  }
  if(forward_state_machine[2] == 0){
    if(status_m3_back_limit || status_m3_back_mag){
      forward_state_machine[2] = 1;
    }
  }
  if(forward_state_machine[3] == 0){
    if(status_m4_back_limit || status_m4_back_mag){
      forward_state_machine[3] = 1;
    }
  }


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

void reset_forward_state_machine(){
  // Reset the State machine
  for(int i = 0; i < 4; i++){
    forward_state_machine[i] = 0;
  }
}

// Open the parachute
void go_forward(){
  reset_forward_state_machine();

  check_switches();
  // Start the timer
  unsigned long time_start = millis();

  // Run this loop while the time is less than all the delay times, and 100 ms.
  unsigned long time_now = millis()-time_start;
  while(
        (time_now < m1_delay + 100) ||
        (time_now < m2_delay + 100) ||
        (time_now < m3_delay + 100) ||
        (time_now < m4_delay + 100)
    ){

    time_now = millis()-time_start;
    check_switches();

    if((time_now > m1_delay) && (forward_state_machine[0] == 0)){
      if(status_m1_back_mag || status_m1_back_limit){   // Stop the motor if either the forward mag or limit switch is on.
        motor_stop(m1_a, m1_b);                         // Stop
      } else {motor_bwd(m1_a, m1_b);}                   // Otherwise start.
      // If mag or switch is reached and we have run 100ms forward then stop.
      if((status_m1_forw_mag || status_m1_forw_limit) && (time_now > m1_delay+100)){
        motor_stop(m1_a, m1_b);
      }
    } else {motor_stop(m1_a, m1_b);};                     // If we haven't reached the time, then stop!

    if((time_now > m2_delay) && (forward_state_machine[1] == 0)){
      if(status_m2_back_mag || status_m2_back_limit){   // Stop the motor if either the forward mag or limit switch is on.
        motor_stop(m2_a, m2_b);                         // Stop
      } else {motor_bwd(m2_a, m2_b);}                   // Otherwise start.
      // If mag or switch is reached and we have run 100ms forward then stop.
      if((status_m2_forw_mag || status_m2_forw_limit) && (time_now > m2_delay+100)){
        motor_stop(m2_a, m2_b);
      }
    } else {motor_stop(m2_a, m2_b);};                     // If we haven't reached the time, then stop!

    if((time_now > m3_delay) && (forward_state_machine[2] == 0)){
      if(status_m3_back_mag || status_m3_back_limit){   // Stop the motor if either the forward mag or limit switch is on.
        motor_stop(m3_a, m3_b);                         // Stop
      } else {motor_bwd(m3_a, m3_b);}                   // Otherwise start.
      // If mag or switch is reached and we have run 100ms forward then stop.
      if((status_m3_forw_mag || status_m3_forw_limit) && (time_now > m3_delay+100)){
        motor_stop(m3_a, m3_b);
      }
    } else {motor_stop(m3_a, m3_b);};                     // If we haven't reached the time, then stop!

    if((time_now > m4_delay) && (forward_state_machine[3] == 0)){
      if(status_m4_back_mag || status_m4_back_limit){   // Stop the motor if either the forward mag or limit switch is on.
        motor_stop(m4_a, m4_b);                         // Stop
      } else {motor_bwd(m4_a, m4_b);}                   // Otherwise start.
      // If mag or switch is reached and we have run 100ms forward then stop.
      if((status_m4_forw_mag || status_m4_forw_limit) && (time_now > m4_delay+100)){
        motor_stop(m4_a, m4_b);
      }
    } else {motor_stop(m4_a, m4_b);};                     // If we haven't reached the time, then stop!
  }

  unsigned long time_since_start = millis()-time_start;
  while(millis()-time_start < timeout_time){
    // Do nothing until switches are hit . . .
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

  check_switches();
  // Start the timer
  unsigned long time_start = millis();

  // Start running forward.  As long as no backward switch has been pressed.
  unsigned long time_now = millis()-time_start;
  while((sum_of_forward_limit_switches() == 0) && (time_now < 1000)){

    time_now = millis()-time_start;
    if(debug){Serial.println(time_now, DEC); };

    if(!status_m1_forw_mag && !status_m1_forw_limit){
      motor_fwd(m1_a, m1_b);
    } else {motor_stop(m1_a, m1_b);}

    if(!status_m2_forw_mag && !status_m2_forw_limit){
      motor_fwd(m2_a, m2_b);
    } else {motor_stop(m2_a, m2_b);}

    if(!status_m3_forw_mag && !status_m3_forw_limit){
      motor_fwd(m3_a, m3_b);
    } else {motor_stop(m3_a, m3_b);}

    if(!status_m4_forw_mag && !status_m4_forw_limit){
      motor_fwd(m4_a, m4_b);
    } else {motor_stop(m4_a, m4_b);}
  }

  // After the first switch (magnetic or mechanical) is thrown start to shut everyone down.
  Serial.println(0, DEC); // !! DO NOT REMOVE!  FOR SOME REASON THE TIMING ON THIS WORKS.

  while((sum_of_backward_switches() < 4)){
    // Do nothing until switches are hit . . .
    // Serial.println(time_now, DEC);
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
  if(status_m1_back_limit){motor_fwd(m1_a, m1_b); delay(100); motor_stop(m1_a, m1_b);};
  if(status_m2_back_limit){motor_fwd(m2_a, m2_b); delay(100); motor_stop(m2_a, m2_b);};
  if(status_m3_back_limit){motor_fwd(m3_a, m3_b); delay(100); motor_stop(m3_a, m3_b);};
  if(status_m4_back_limit){motor_fwd(m4_a, m4_b); delay(100); motor_stop(m4_a, m4_b);};

  if(status_m1_forw_limit){motor_bwd(m1_a, m1_b); delay(100); motor_stop(m1_a, m1_b);};
  if(status_m2_forw_limit){motor_bwd(m2_a, m2_b); delay(100); motor_stop(m2_a, m2_b);};
  if(status_m3_forw_limit){motor_bwd(m3_a, m3_b); delay(100); motor_stop(m3_a, m3_b);};
  if(status_m4_forw_limit){motor_bwd(m4_a, m4_b); delay(100); motor_stop(m4_a, m4_b);};

  delay(1000);  // Not in a hurry here, keep it from overheating or getting stuck.
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
  // NOTE: check_switches is called every 1,000 microseconds (us) with an interupt.

  // Before we do anything else check if the limit switches are triggered.
  // If the limit switches are triggerd then back the rope away from them.
  while((sum_of_backward_limit_switches()+sum_of_forward_limit_switches() > 0)){
    back_off_limit_switches();

  }

  /* Test Code */

  /*
  Serial.println("Go Forward.");
  go_forward();
  //delay_minutes(1); // Delay 1 minute seconds.
  delay(10000);

  Serial.println("Get Status.");
  Serial.println("State machine:");
  for(int i = 0; i < 4; i++){
    Serial.print(forward_state_machine[i], DEC);
  }
  get_status();

  Serial.println("Go Backward.");
  go_backward();
  //delay_minutes(1); // Delay 1 minute seconds.
  delay(10000);

  Serial.println("Get Status.");
  Serial.println("State machine:");
  for(int i = 0; i < 4; i++){
    Serial.print(forward_state_machine[i], DEC);
  }
  get_status();
  // delay_minutes(1); // Delay 1 minute seconds.
  */


  /* Operations Code */
  
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
