// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#include <Servo.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif



#define Dianostics_pin            6
#define Ring_pin                  7
#define robotArm                  2 
#define kinect2                   3 
#define sensors                   4 
#define drive                     5 
#define servo                     14 



// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS_Diagnostics     8
#define NUMPIXELS_Ring            24
#define NUM_relays                4
#define NUM_servos                1
#define servo_middle              56

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel Diagnostics_leds = Adafruit_NeoPixel(NUMPIXELS_Diagnostics, Dianostics_pin, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel Ring_leds = Adafruit_NeoPixel(NUMPIXELS_Ring, Ring_pin, NEO_GRB + NEO_KHZ800);
Servo antenna_servo;

int delayval = 5;
int data_diagnostics[8] = {0,0,0,0,0,0,0,0};
int data_ring[24] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int data_relays[4] = {0,0,0,0};
int servo_positions[1] = {75};
int relays[4] = {1,1,1,1};






void setup() {
  Diagnostics_leds.begin(); // This initializes the NeoPixel library.
  Ring_leds.begin(); // This initializes the NeoPixel library.
  Diagnostics_leds.setBrightness(64);
  Ring_leds.setBrightness(64);
  Serial.begin(115200);
  antenna_servo.attach(servo);


  pinMode(robotArm, OUTPUT);
  pinMode(kinect2, OUTPUT);
  pinMode(sensors, OUTPUT);
  pinMode(drive, OUTPUT);
  
  antenna_servo.write(servo_positions[0]); 

}

void setColourDiagnosticsLeds(int ledNo, int red, int green, int blue){
  Diagnostics_leds.setPixelColor(ledNo, Diagnostics_leds.Color(red, green, blue) );
}

void setColourRingLeds(int ledNo, int red, int green, int blue){
  Ring_leds.setPixelColor(ledNo, Ring_leds.Color(red, green, blue) );
}

void setDiagnosticLeds(){
  int i = 0;
      for(i = 0; i < NUMPIXELS_Diagnostics; i++){
        if(data_diagnostics[i] == 0){
          setColourDiagnosticsLeds(i,255,0,0);        
        }
        else if(data_diagnostics[i] == 1){
          setColourDiagnosticsLeds(i,0,255,0);        
        }
        else if(data_diagnostics[i] == 2){
          setColourDiagnosticsLeds(i,0,0,255);          
        }
        else if(data_diagnostics[i] == 3){
          setColourDiagnosticsLeds(i,255,255,0);         
        }
        else if(data_diagnostics[i] == 4){
          setColourDiagnosticsLeds(i,0,255,255);        
        }
        else if(data_diagnostics[i] == 5){
          setColourDiagnosticsLeds(i,255,255,255);        
        }
        else{
          setColourDiagnosticsLeds(i,0,0,0);         
        }
      }     
}

void setRingLeds(){
  int i = 0;
      for(i = 0; i < NUMPIXELS_Ring; i++){
        if(data_ring[i] == 0){
          setColourRingLeds(i,255,0,0);        
        }
        else if(data_ring[i] == 1){
          setColourRingLeds(i,0,255,0);        
        }
        else if(data_ring[i] == 2){
          setColourRingLeds(i,0,0,255);          
        }
        else if(data_ring[i] == 3){
          setColourRingLeds(i,255,255,0);         
        }
        else if(data_ring[i] == 4){
          setColourRingLeds(i,0,255,255);        
        }
        else if(data_ring[i] == 5){
          setColourRingLeds(i,255,255,255);        
        }
        else{
          setColourRingLeds(i,0,0,0);         
        }
      }     
}

void setRelays(){
  int i = 0;
  for(i = 0; i < NUM_relays; i++){
    if(data_relays[i] == 0){
      relays[i] = 0;      
    }else{
      relays[i] = 1; //Default to ON so we don't accidently turn stuff off.    
    }
  }     
}

void setRelayOutput(){
   int i = 0;
   for(i = 0; i < NUM_relays; i++){
      digitalWrite(robotArm + i, relays[i]);
   }
}

void setServoPositions(){
  antenna_servo.write(servo_positions[0]);      
}


int readSerial(){
  
 
    
    if(Serial.read() == 's'){
      //Serial.println("recieved start bit");
      int i = 0;
      
      for(i = 0; i < NUMPIXELS_Diagnostics + NUMPIXELS_Ring + NUM_relays + NUM_servos; i++){
        while(Serial.read() != 'd'){
            delay(1);
         }
        if( i < NUMPIXELS_Diagnostics){
          data_diagnostics[i] = Serial.parseInt();
        }else if (i < NUMPIXELS_Diagnostics + NUMPIXELS_Ring){
          data_ring[i - NUMPIXELS_Diagnostics] = Serial.parseInt();    
        }else if (i < NUMPIXELS_Diagnostics + NUMPIXELS_Ring + NUM_relays){
          data_relays[i - NUMPIXELS_Diagnostics - NUMPIXELS_Ring] = Serial.parseInt();   
        }else if (i < NUMPIXELS_Diagnostics + NUMPIXELS_Ring + NUM_relays + NUM_servos){
          servo_positions[i - NUMPIXELS_Diagnostics - NUMPIXELS_Ring - NUM_relays] = Serial.parseInt();   
        }
        

      }   


      /* // DEBUG VIEW
      Serial.println("Got data");
      Serial.println("Diagnostics:");
      for(i = 0; i < NUMPIXELS_Diagnostics; i++){
        Serial.println(data_diagnostics[i]);
      }
      Serial.println("Ring:");
      for(i = 0; i < NUMPIXELS_Ring; i++){
        Serial.println(data_ring[i]);
      }
      Serial.println("Relays:");
      for(i = 0; i < NUM_relays; i++){
        Serial.println(data_relays[i]);
      }
      Serial.println("Servos:");
      for(i = 0; i < NUM_servos; i++){
        Serial.println(servo_positions[i]);
      }
      Serial.println("End of data");
      */
      
    }
   
  
  
}

void loop() {
    if (Serial.available() > 0){
      readSerial();   
      
      setDiagnosticLeds();
      Diagnostics_leds.show(); 

      setRingLeds();
      Ring_leds.show(); 

      setRelays();
      setRelayOutput();

      setServoPositions();
      
      Serial.println("ok");
     
    }

    delay(delayval); // Delay for a period of time (in milliseconds).
    
  
}

