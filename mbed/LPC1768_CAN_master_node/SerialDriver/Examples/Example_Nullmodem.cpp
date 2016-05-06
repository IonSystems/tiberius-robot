/// @file Example_Nullmodem.cpp
/// @brief USB null modem
/// 
/// - Uses SerialDriver with USBTX and USBRX.
/// - Send back every received byte.
/// 
/// - LED1 indicates waiting for @ref SerialDriver::getc
/// - LED2 indicates waiting for @ref SerialDriver::putc
/// - LED4 indicates a parallel thread running

#if 0

#include "SerialDriver.h"

SerialDriver pc(USBTX, USBRX);
DigitalOut led1(LED1), led2(LED2), led4(LED4);

// This thread is emulating a null modem
void nullmodem(void const * argument)
{
    pc.baud(9600);
    
    int c;
    while(1)
    {
        led1= 1;
        c= pc.getc();
        led1= 0;
        
        led2= 1;
        pc.putc(c);
        led2= 0;
    }
}

int main()
{
    // Start the null modem
    Thread nullmodemTask(&nullmodem);
    
    // Do something else now  
    while(1)
    {
        Thread::wait(20);
        led4= !led4;
    }
}

#endif

