/*
 */
#include "mbed.h"
 
#ifndef  DRV8825_I2C_H
#define  DRV8825_I2C_H
 
//
// Device registers
//
enum DRV8825_REGISTER_SET {
  REGISTER_POINTER,   // for read command
  COMMAND_REG,
  STATUS_REG,
  MODE_REG,
  LIMIT_REG,
  ERROR_REG,
  STEPS_REG_0,
  STEPS_REG_1,
  STEPS_REG_2,
  STEPS_REG_3,
  CUR_POS_REG_0,
  CUR_POS_REG_1,
  CUR_POS_REG_2,
  CUR_POS_REG_3,
  RUN_SPEED_0,
  RUN_SPEED_1,
  MAX_SPEED_0,
  MAX_SPEED_1,  
  VERSION_REG,
};
//
// Commands
//
enum DRV8825_COMMAND_SET {
  STOP,
  POWER_DOWN,
  MOVE_ABS,
  MOVE_REL,
  MOVE_CONT,
  GET_CURRENT_POSITION,
  SET_ORIGIN,
  SET_DEFAULT_VALUES,
};
//
// Set of error codes
//
enum DRV_errors {
  DRV_OK,
  BAD_REGISTER_NO,
  BAD_COMMAND,
  BAD_MODE,
  BAD_SET_POSITION,
} ;

class DRV8825_I2C {
public:
     DRV8825_I2C(PinName sda, PinName scl, int i2cAddress);
    
    void  write_reg(int reg, int value1, int value2); 
    char  read_reg(int reg);
    void  set_step_count(int32_t counts);
       
protected:
     I2C _i2c;
     char address;
     char _writeOpcode, _readOpcode;
 };
 
 #endif
 