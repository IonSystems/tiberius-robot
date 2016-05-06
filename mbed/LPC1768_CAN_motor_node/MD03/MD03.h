/*
 */
#include "mbed.h"
 
#ifndef  MD03_H
#define  MD03_H
 
/*
 * list of registers
 */
#define MD03_COMMAND           0x00
#define MD03_STATUS            0x01
#define MD03_SPEED             0x02
#define MD03_ACCELERATION      0x03
#define MD03_TEMPERATURE       0x04
#define MD03_MOTOR_CURRENT     0x05
#define MD03_SOFTWARE_REV      0x07
/*
 * list of command that can be sent to command register
 */
#define MD03_CMD_STOP       0x00
#define MD03_CMD_FORWARD    0x01
#define MD03_CMD_REVERSE    0x02

class MD03 {
public:
     MD03(PinName sda, PinName scl, int i2cAddress);
     
     void set_speed(int speed);
     void set_accel(int acceleration);
     void stop(void);
     void move_forward(void);
     void move_reverse(void);
     char read_reg(int register);
     
protected:
     I2C _i2c;
     char address;
     char _writeOpcode, _readOpcode;
 };
 
 #endif
 