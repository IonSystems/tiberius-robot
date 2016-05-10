/// @file Example_Bridge.cpp
/// @brief Forwarding every byte from USB to uart and vice versa
/// 
/// - Uses SerialDriver with USBTX and USBRX.
/// - Uses SerialDriver with p13 and p14.
/// 
/// - LED1 indicates forwarding pc to uart works
/// - LED2 indicates forwarding uart to pc works
/// - LED4 indicates a parallel thread running
/// 
/// - connect p13 with p14 to get a hardware null modem ;)

#if 0

#include "SerialDriver.h"

SerialDriver pc(USBTX, USBRX);
SerialDriver uart(p13, p14);
DigitalOut led1(LED1), led2(LED2), led4(LED4);

// This thread forwards from pc to uart
void forwardPc(void const * argument)
{
    // Sometimes You're the Hammer, 
    while(1)
    {    
        uart.putc(pc.getc());
        led1= !led1;    
    }
}

// This thread forwards from uart to pc
void forwardUart(void const * argument)
{
    // Sometimes You're the Nail
    while(1)
    {      
        pc.putc(uart.getc());
        led2= !led2;    
    }
}

int main()
{
    // setup serial ports
    pc.baud(9600);
    uart.baud(38400);
    
    // Start the forwarding threads
    Thread forwardPcThread(&forwardPc);
    Thread forwardUartThread(&forwardUart);
    
    // Do something else now  
    while(1)
    {
        Thread::wait(20);
        led4= !led4;
    }
}

#endif

