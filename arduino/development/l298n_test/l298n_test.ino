/*  Motor Control Truth Tables:  https://www.bananarobotics.com/shop/How-to-use-the-L298N-Dual-H-Bridge-Motor-Driver
 *  A Max:
 *  Send a test "-123,0321" 
*/

// Motor Controller 1 Pins
#define enA 9
#define enB 8
#define in1 6
#define in2 7
#define in3 5
#define in4 4

int rotDirection = 0;


void set_motors(int m1, int m2){
  ///////////////////
  // Motor 1
  //////////////////
  // int pwmOutput1 = map(abs(m1), 0, 100, 0 , 255);  // Map the potentiometer value from 0 to 255
  int pwmOutput1(abs(m1));
  analogWrite(enA, pwmOutput1);                    // Send PWM signal to L298N Enable pin
  
  if(m1 < 0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } 
  else if(m1 > 0){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else{
    int pwmOutput1 = 255;                            // Map the potentiometer value from 0 to 255
    analogWrite(enA, pwmOutput1);                    // Send PWM signal to L298N Enable pin
    digitalWrite(in1, HIGH);
    digitalWrite(in2, HIGH);
  }

  ///////////////////
  // Motor 2
  //////////////////
  // int pwmOutput2 = map(abs(m2), 0, 100, 0 , 255);  // Map the potentiometer value from 0 to 255
  int pwmOutput2(abs(m2));
  analogWrite(enB, pwmOutput2);                    // Send PWM signal to L298N Enable pin
  
  if(m1 < 0){
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  } 
  else if(m1 > 0){
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  }
  else{
    int pwmOutput2 = 255;                            // Map the potentiometer value from 0 to 255
    analogWrite(enB, pwmOutput2);                    // Send PWM signal to L298N Enable pin
    digitalWrite(in3, HIGH);
    digitalWrite(in4, HIGH);
  }
}

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(1000000);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  
  pinMode(in1, INPUT);
  pinMode(in2, INPUT);
  pinMode(in3, INPUT);
  pinMode(in4, INPUT);

  // Set initial rotation direction
  set_motors(0,0);
}

int power1 = 0; // Global motor power 1
int power2 = 0; // Global motor power 2

int serial_get_power(){
  // Send a test "-123,0321" 
  char buffer1[] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
  char buffer2[] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
  // while (!Serial.available()); // Wait for characters
  if(Serial.available()){ 
    Serial.readBytesUntil(',', buffer1, 5);
    Serial.readBytesUntil('n', buffer2, 5);
    int incomingValue1 = atoi(buffer1);
    int incomingValue2 = atoi(buffer2);
    Serial.print(incomingValue1);
    Serial.print(",");
    Serial.println(incomingValue2);

    power1 = incomingValue1;
    power2 = incomingValue2;
    
    return 0;
  }
  else{
    return -1;
  }
}

void loop() {
  /*
  serial_get_power();
  set_motors(power1,power2);
  */
  int run_time = 5000;
  set_motors(255,255);
  delay(run_time);
  set_motors(0,0);
  delay(1000);
  
  set_motors(-255,-255);
  delay(run_time);
  set_motors(0,0);
  delay(1000);
  
}


