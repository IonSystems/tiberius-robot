#include <Adafruit_SoftServo.h>
#define STOPPED 56
int robotArm = 0; 
int kinect2 = 1;
int sensors = 2;
int drive = 3;
int servo = 4;
int servo_position = 0;
Adafruit_SoftServo antenna_servo;



// the setup routine runs once when you press reset:
void setup() {
 // Set up the interrupt that will refresh the servo for us automagically
  OCR0A = 0xAF;            // any number is OK
  TIMSK |= _BV(OCIE0A);    // Turn on the compare interrupt (below!)
  antenna_servo.attach(servo);  
  antenna_servo.write(90);           // Tell servo to go to position per quirk
  
  // initialize the digital pin as an output.
  pinMode(robotArm, OUTPUT);
  pinMode(kinect2, OUTPUT);
  pinMode(sensors, OUTPUT);
  pinMode(drive, OUTPUT);
  delay(15); // Wait 15ms for the servo to reach the position
}

// the loop routine runs over and over again forever:
void loop() {  
    int i = 0;
    for(i = 0; i < 4; i++){
      digitalWrite(i, LOW);
    }
    delay(20);
     for(i = 0; i < 4; i++){
      digitalWrite(i, HIGH);
    }
    delay(20);

    
    antenna_servo.write(STOPPED);  
   
   
}

// We'll take advantage of the built in millis() timer that goes off
// to keep track of time, and refresh the servo every 20 milliseconds
volatile uint8_t counter = 0;
SIGNAL(TIMER0_COMPA_vect) {
  // this gets called every 2 milliseconds
  counter += 2;
  // every 20 milliseconds, refresh the servos!
  if (counter >= 20) {
    counter = 0;
    antenna_servo.refresh();
    
  }
}


    
