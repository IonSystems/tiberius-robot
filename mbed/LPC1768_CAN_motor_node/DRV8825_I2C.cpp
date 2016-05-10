/*
 * MD03 : 24v 20A H-bridge motor driver in I2C bus
 */
#include "mbed.h"
#include "DRV8825_I2C.h"
 
DRV8825_I2C::DRV8825_I2C(PinName sda, PinName scl, int i2cAddress)  : _i2c(sda, scl) {
    _writeOpcode = i2cAddress & 0xFE;
    _readOpcode  = i2cAddress | 0x01;
    
    _i2c.frequency(100000);
}
union {
    uint8_t    byte[4];
    int32_t    value;
} value32;
 
void DRV8825_I2C::write_reg(int reg, int value1, int value2) 
{
char data[3];

    data[0] = (char)reg;
    data[1] = (char)value1;
    data[2] = (char)value2;    
    _i2c.write(_writeOpcode, data, 3);
} 

char DRV8825_I2C::read_reg(int reg) 
{
char data[2];

    data[0] = reg;
    _i2c.write(_writeOpcode, data, 1);
    _i2c.read(_readOpcode, data, 1);
    return data[0];
}

void DRV8825_I2C::set_step_count(int32_t counts) 
{
    value32.value = counts;
    write_reg(STEPS_REG_0, value32.byte[0], value32.byte[1]);
    write_reg(STEPS_REG_2, value32.byte[2], value32.byte[3]);
} 
 
/* void MD03::set_speed(int speed) 
{
char data[2];

    data[0] = MD03_SPEED;
    data[1] = ((speed * 255)/100);
    _i2c.write(_writeOpcode, data, 2);
}

void MD03::set_accel(int acceleration) 
{
char data[2];

    data[0] = MD03_ACCELERATION;
    data[1] = 255 - ((acceleration * 255)/100);
    _i2c.write(_writeOpcode, data, 2);
}

void MD03::stop(void) 
{
char data[2];

    data[0] = MD03_COMMAND;
    data[1] = MD03_CMD_STOP;
    _i2c.write(_writeOpcode, data, 2);
}

void MD03::move_forward(void) 
{
char data[2];

    data[0] = MD03_COMMAND;
    data[1] = MD03_CMD_FORWARD;
    _i2c.write(_writeOpcode, data, 2);
}

void MD03::move_reverse(void) 
{
char data[2];

    data[0] = MD03_COMMAND;
    data[1] = MD03_CMD_REVERSE;
    _i2c.write(_writeOpcode, data, 2);
}

char MD03::read_reg(int reg) 
{
char data[2];

    data[0] = reg;
    _i2c.write(_writeOpcode, data, 1);
    _i2c.read(_readOpcode, data, 1);
    return data[0];
}
*/
