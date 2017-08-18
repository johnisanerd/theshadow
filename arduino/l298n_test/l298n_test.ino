/*  Motor Control Truth Tables:  https://www.bananarobotics.com/shop/How-to-use-the-L298N-Dual-H-Bridge-Motor-Driver
 *  A Max:
 *  VMax:
*/
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
  int pwmOutput1 = map(abs(m1), 0, 100, 0 , 255);  // Map the potentiometer value from 0 to 255
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
  int pwmOutput2 = map(abs(m2), 0, 100, 0 , 255);  // Map the potentiometer value from 0 to 255
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
  Serial.begin(115200);
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

int get_power(){
  // 125 is full power, 254 is full negative power.
  
  char buffer[] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
  while (!Serial.available()); // Wait for characters
  Serial.readBytesUntil('n', buffer, 7);
  int incomingValue = atoi(buffer);
  Serial.println(incomingValue);
  return incomingValue;
}

void loop() {
  int power = get_power();
  set_motors(power,power);
  set_motors(power,power);  
}
