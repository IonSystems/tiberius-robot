#include "SerialDriver.h"

SerialDriver::SerialDriver(PinName txPin, PinName rxPin, int txBufferLength_, int rxBufferLength_, unsigned char * txBuffer_, unsigned char * rxBuffer_)
    : RawSerial(txPin, rxPin), semTxBufferFull(0), semRxBufferEmpty(0)
{    
    // check buffer length
    txBufferLength= txBufferLength_;
    if(txBufferLength <= 1)
        error("TX buffer length must be > 1 !");
        
    rxBufferLength= rxBufferLength_;
    if(rxBufferLength <= 1)
        error("RX buffer length must be > 1 !");
    
    // take or allocate buffer
    txBuffer= txBuffer_;
    if(txBuffer == NULL)
    {
        txBuffer= new unsigned char[txBufferLength];
        if(txBuffer == NULL)
            error("Cannot allocate TX buffer!");
    }
    
    rxBuffer= rxBuffer_;
    if(rxBuffer == NULL)
    {
        rxBuffer= new unsigned char[rxBufferLength];
        if(rxBuffer == NULL)
            error("Cannot allocate RX buffer!");
    }
        
    
    // reset cursors
    txIn= txOut= 0;
    rxIn= rxOut= 0;
    txCount= rxCount= 0;
    
    // reset drop counters
    numTxDrops= 0;
    numRxDrops= 0;
    
    // attach interrupt routines
    attach(this, &SerialDriver::onTxIrq, TxIrq);
    attach(this, &SerialDriver::onRxIrq, RxIrq);
    
    // we need tx interrupt not yet
    disableTxInterrupt();
}

int SerialDriver::putc(int c, unsigned int timeoutMs)
{
    // critical section, isr could modify cursors
    disableTxInterrupt();
    
    if(isTxBufferFull())
    {
        // wait for free space
        while(semTxBufferFull.wait(0) > 0);    // clear semaphore
        enableTxInterrupt();
        
        // let isr work
        semTxBufferFull.wait(timeoutMs);
        
        disableTxInterrupt();
        if(isTxBufferFull()) // still full? drop byte!
        {
            numTxDrops++;
            enableTxInterrupt();
            return 0;
        }
    }
    
    // write this byte to tx buffer
    txBuffer[txIn]= (unsigned char)c;
    txIn= (txIn+1) % txBufferLength;
    txCount++;
    
    // its over, isr can come
    enableTxInterrupt();
        
    // Let's write (isr will check writeability itself)
    onTxIrq();
    
    return 1;
}

void SerialDriver::onTxIrq()
{
    // prevent fire another TxIrq now
    disableTxInterrupt();
    
    // write as long as you can
    bool wasFull= isTxBufferFull();
    while(SerialBase::writeable() && !isTxBufferEmtpy())
    {
        // take byte from tx buffer and put it out
        SerialBase::_base_putc(txBuffer[txOut]);
        txOut= (txOut+1) % txBufferLength;
        txCount--;
    }
    
    if(wasFull && !isTxBufferFull())   // more bytes can come
        semTxBufferFull.release();
    
    // ok, let's wait for next writability,
    // if there is something to send,  
    // else we need tx interrupt not yet
    if(!isTxBufferEmtpy())
        enableTxInterrupt();
}


int SerialDriver::getc(unsigned int timeoutMs)
{    
    // Let's read (isr will check readability itself)
    onRxIrq();
    
    // critical section, isr could modify cursors
    disableRxInterrupt();
    
    if(isRxBufferEmpty())
    {
        // wait for new byte
        while(semRxBufferEmpty.wait(0) > 0);    // clear semaphore
        enableRxInterrupt();
        
        // let isr work
        semRxBufferEmpty.wait(timeoutMs);
        
        disableRxInterrupt();
        if(isRxBufferEmpty()) // still empty? nothing received!
        {
            enableRxInterrupt();
            return -1;
        }
    }
    
    // get byte from rx buffer
    int c= (int)rxBuffer[rxOut];
    rxOut= (rxOut+1) % rxBufferLength;
    rxCount--;
    
    // its over, isr can come
    enableRxInterrupt();
    
    return c;
}

void SerialDriver::onRxIrq()
{
    // prevent fire another RxIrq now
    disableRxInterrupt();
    
    // read as long as you can
    bool wasEmpty= isRxBufferEmpty();
    while(SerialBase::readable())
    {
        // get byte and store it to the RX buffer
        int c= SerialBase::_base_getc();
        if(!isRxBufferFull())
        {
            rxBuffer[rxIn]= (unsigned char)c;
            rxIn= (rxIn+1) % rxBufferLength;
            rxCount++;
        }
        else    // drop byte :(
            numRxDrops++;
    }
    
    if(wasEmpty && !isRxBufferEmpty())   // more bytes can go
        semRxBufferEmpty.release();
    
    // ok, let's wait for next readability
    enableRxInterrupt();
}


int SerialDriver::write(const unsigned char * buffer, const unsigned int length, bool block)
{
    // try to put all bytes
    for(int i= 0; i < length; i++)
        if(!putc(buffer[i], block ? osWaitForever : 0))
            return i; // putc failed, but already put i bytes
    
    return length;  // put all bytes
}
    
int SerialDriver::read(unsigned char * buffer, const unsigned int length, bool block)
{
    // try to get all bytes
    int c;
    for(int i= 0; i < length; i++)
    {
        c= getc(block ? osWaitForever : 0);
        if(c < 0)
            return i; // getc failed, but already got i bytes
        buffer[i]= (unsigned char)c;
    }
    
    return length;  // got all bytes
}


int SerialDriver::puts(const char * str, bool block)
{
    // the same as write, but get length from strlen
    const int len= strlen(str);
    return write((const unsigned char *)str, len, block);
}

int SerialDriver::printf(const char * format, ...)
{
    // Parts of this are copied from mbed RawSerial ;)
    std::va_list arg;
    va_start(arg, format);
    
    int length= vsnprintf(NULL, 0, format, arg);
    char *temp = new char[length + 1];
    if(temp == NULL)
        return 0;   // I can't work like this!    

    vsprintf(temp, format, arg);
    puts(temp, true);
    delete[] temp;
    
    va_end(arg);
    return length;
} 

// still thinking of XTN

