// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define Dianostics_pin            10


// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      8

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel Diagnostics_leds = Adafruit_NeoPixel(NUMPIXELS, Dianostics_pin, NEO_GRB + NEO_KHZ800);


int delayval = 5; // delay for half a second
int data[8] = {0,0,0,0,0,0,0,0};

void setup() {
  Diagnostics_leds.begin(); // This initializes the NeoPixel library.
  Serial.begin(9600);
}

void setColour(int ledNo, int red, int green, int blue){
  Diagnostics_leds.setPixelColor(ledNo, Diagnostics_leds.Color(red, green, blue) );
}


int readSerial(){
  
 
    
    if(Serial.read() == 's'){
      //Serial.println("recieved start bit");
      int i = 0;
      
      for(i = 0; i < NUMPIXELS; i++){
        while(Serial.read() != 'd'){
            delay(1);
         }
        data[i] = Serial.parseInt();               
      }   
      
      
      
    }
   
  
  
}

void loop() {
    if (Serial.available() > 0){
      readSerial();   
      
      int i = 0;
      for(i = 0; i < NUMPIXELS; i++){
        if(data[i] == 0){
          setColour(i,255,0,0);        
        }
        else if(data[i] == 1){
          setColour(i,0,255,0);        
        }
        else if(data[i] == 2){
          setColour(i,0,0,255);          
        }
        else if(data[i] == 3){
          setColour(i,255,255,0);         
        }
        else if(data[i] == 4){
          setColour(i,0,255,255);        
        }
        else if(data[i] == 5){
          setColour(i,255,255,255);        
        }
        else{
          setColour(i,0,0,0);         
        }
      }     
     
      Diagnostics_leds.show(); 
      Serial.println("ok");
     
    }

    delay(delayval); // Delay for a period of time (in milliseconds).
    
  
}

