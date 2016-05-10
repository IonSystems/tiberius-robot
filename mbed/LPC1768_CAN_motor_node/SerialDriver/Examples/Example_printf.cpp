/// @file Example_printf.cpp
/// @brief Formatted output
/// 
/// - Uses SerialDriver with USBTX and USBRX.
/// - Has much too small buffers, but printf is blocking, so it does not matter
/// 
/// - The terminal will be flooded with text
/// - LED4 indicates parallel thread working
/// 

#if 0

#include "SerialDriver.h"

// only 4 byte of software ring buffer?
// No problem! SerialDriver uses idle blocking calls :D
SerialDriver pc(USBTX, USBRX, 4, 4);

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
    
    float f= 0.0f;    
    while(1)
    {
        // unformatted text
        pc.puts("Hi! this uses puts.\r\n");
        
        // formatted text
        pc.printf("And this is formatted. Here is the sin(%f)=%f.\r\n", f, sinf(f));
        f+= 0.25f;
    }
}

#endif
