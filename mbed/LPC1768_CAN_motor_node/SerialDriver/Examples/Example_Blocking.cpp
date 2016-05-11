/// @file Example_Blocking.cpp
/// @brief Test blocking write / read
/// 
/// - Uses SerialDriver with USBTX and USBRX.
/// - Has much too small buffers, to how far can it get?
/// 
/// - Testing how much bytes were transmitted, with too small TX buffer and forced non blocking
/// - Waiting till 10 bytes are received
/// - LED4 indicates parallel thread working
/// 

#if 0

#include "SerialDriver.h"

SerialDriver pc(USBTX, USBRX, 4, 32);

// This thread is running in parallel
DigitalOut led4(LED4);
void parallel(void const * argument)
{
    while(1)
    {
        Thread::wait(20);
        led4= !led4;
    }
}

int main()
{
    // Start the other thread
    Thread parallelTask(&parallel);
    
    
    const char * completeText= "This is a complete text. How much will you receive?";
    const int completeTextLength= strlen(completeText);
    int writtenBytes;
    
    
    const int readBufferLength= 10;
    unsigned char readBuffer[readBufferLength];
    int receivedBytes= 0;
    
    while(1)
    {
        // write non blocking, how much get transmitted?
        writtenBytes= pc.write((const unsigned char*)completeText, completeTextLength, false);
        
        // now print the result
        pc.printf("\r\nOnly %i of %i bytes were transmitted using non blocking write.\r\n", writtenBytes, completeTextLength);
        
        
        // wait for 10 bytes
        pc.printf("I wait for my 10 bytes. Send them!\r\n", writtenBytes, completeTextLength);
        receivedBytes+= pc.read(readBuffer, readBufferLength);
        
        // now print result
        pc.printf("Received %i bytes since start.\r\n\r\n", receivedBytes);
        
        
        // wait a bit
        Thread::wait(1000);
    }
}

#endif
