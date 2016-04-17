int sample = 0;

double totalCharge = 0;
double averageAmps = 0;
double ampSeconds = 0;
double ampHours = 0;
double wattHours = 0;
unsigned long seconds = 0;


void setup()
{
  //Set ADC reference voltage to 1.1V
  
  Serial.begin(9600);
}

void loop()
{
    double amps = getCurrentAverage(100);
    double voltage = getVoltageAverage(100);
    float watts = amps * voltage;
    sample = sample + 1;
    
    seconds =  millis() / 1000.0;
    totalCharge = totalCharge + amps;
    averageAmps = totalCharge / sample;
    ampSeconds = averageAmps*seconds;
    ampHours = ampSeconds/3600;
    wattHours = voltage * ampHours;


  
    //Get the current of the sensor and print to serial.
    
    Serial.print("Volts = " );
    Serial.print(voltage);
    Serial.print("\t Current (amps) = ");
    Serial.print(amps);
    Serial.print("\t Power (Watts) = ");
    Serial.print(watts);
    Serial.print("\t Time (hours) = ");
    Serial.print(seconds/3600.0);
    Serial.print("\t Amp Hours (ah) = ");
    Serial.print(ampHours);
    Serial.print("\t Watt Hours (wh) = ");
    Serial.println(wattHours);
   delay(100);
}

double getVoltageAverage(int AVnum)
{
   double voltage;
   double vsum=0;
   double val;
  

   for (int i=0; i<AVnum; i++)
   {
      val = analogRead(0);
   
      voltage = 0.07916 * val + 0; 
      vsum=vsum+voltage;
   
   }
   
   voltage = vsum / AVnum;  

   if (voltage<0.0) voltage = 0.0;
   return voltage;
}

double getCurrentAverage(int AVnum)
{
   double current;
   double isum=0;
   double val;
  

   for (int i=0; i<AVnum; i++)
   {
      val = analogRead(2);
   
      current = 0.1199 * val + 0; 
      isum=isum+current;
   
   }
   
   current = isum / AVnum;  

   if (current<0.0) current = 0.0;
   return current;
}

