//
// DRV8825_i2c_slave.
//
// Implements an I2C slave to control a DRV8825 stepper motor control unit.
// Interface is viewed as a simple set by byte registers.  Users can write a single byte
// or read a single byte.
//
// Device viewed as a set of registers, as follows
//
//     address            purpose
//      0x00       Pointer register
//      0x01       Command register
//      0x02       Status register
//      0x03       Mode register
//      0x04       Limit register
//      0x05       Error register
//      0x06       byte 0 of steps requested (LSByte)
//      0x07       byte 1 of steps requested
//      0x08       byte 2 of steps requested
//      0x09       byte 3 of steps requested (MSByte)
//      0x0A       byte 0 of current position (LSByte)
//      0x0B       byte 1 of current position
//      0x0C       byte 2 of current position
//      0x0D       byte 3 of current position (MSByte)
//      0x0E       byte 0 of run speed value (LSByte)
//      0x0F       byte 1 0f run speed value (MSByte)
//      0x10       byte 0 of max speed value (LSByte)
//      0x11       byte 1 0f max speed value (MSByte)
//      0x12       Version info
//
// J Herd April 2016
//
#include <Wire.h>
#include <AccelStepper.h>

#include "DRV8825_i2c_slave.h"

//----------------------------------------------------------------------
// instanciate libraries
//----------------------------------------------------------------------

AccelStepper steering_stepper (AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

//----------------------------------------------------------------------
// I2C definitions
//----------------------------------------------------------------------
#define  SLAVE_ADDRESS        0x05     // 7-bit address
#define  MAX_SENT_BYTES          3
//----------------------------------------------------------------------
// DRV8825 default values
//----------------------------------------------------------------------
#define RUN_SPEED           100
#define MAX_SPEED           120
#define MIN_PULSE_WIDTH      20
#define DRV8825_WAKEUP_TIME   5    // in units of mS
#define LIMIT_SWITCHES_OK  0x0F
//----------------------------------------------------------------------
// Device registers
//----------------------------------------------------------------------
enum {
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

//----------------------------------------------------------------------
//Global data
//----------------------------------------------------------------------
//
// structure to hold device register set
//
union {
  struct {
    byte register_ptr;
    byte command;
    byte status;
    byte mode;
    byte limits;
    byte error;
    long steps_requested;    // 32-bit signed
    long current_position;   // 32-bit signed
    int  runspeed;           // 16-bit signed
    int  maxspeed;           // 16-bit signed
    byte version;
  } reg;
  byte registerMap[sizeof(reg)];   //   REG_MAP_SIZE
} registers;

//----------------------------------------------------------------------
//temp variables
//----------------------------------------------------------------------
byte data1_byte, data2_byte, temp_step_reg_0, temp_step_reg_1;

//----------------------------------------------------------------------
//code
//----------------------------------------------------------------------
// setup : configure system and the related I/O
//
void setup() {
//
// setup I/O
//
  pinMode(BOARD_LED, OUTPUT);
  digitalWrite(BOARD_LED, LOW);
  pinMode(SLEEP_PIN, OUTPUT);
  STEPPER_WAKEUP;
  pinMode(RESET_PIN, OUTPUT);
  STEPPER_RESET;   // digitalWrite(RESET_PIN, HIGH);
  pinMode(END_STOP_1, INPUT_PULLUP);
  pinMode(END_STOP_2, INPUT_PULLUP);
  pinMode(END_STOP_3, INPUT_PULLUP);
  pinMode(END_STOP_4, INPUT_PULLUP);
//
// setup I2C as slave device
//
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  registers.reg.register_ptr = 0;
  registers.registerMap[VERSION_REG] = CURRENT_VERSION;
//
// configure stepper motor library parameters
//
  registers.reg.runspeed = RUN_SPEED;
  registers.reg.maxspeed = MAX_SPEED;
  steering_stepper.setSpeed(registers.reg.runspeed);
  steering_stepper.setMaxSpeed(registers.reg.maxspeed);
  steering_stepper.setMinPulseWidth(MIN_PULSE_WIDTH);
//
// setup serial port for debug messages
//
  Serial.begin(9600);
  Serial.println("Setup complete");
//
// setup system info
//
  registers.registerMap[MODE_REG] = HALTED;
//
// temp testing values
//
  registers.reg.steps_requested = 200;
}

//----------------------------------------------------------------------
// loop : Primary system code loop
//
// Notes :
//  * check limit switch inputs
//  * If stepper has reached target, stop and set to sleep
//
void loop() {
  read_limits();
  if (registers.registerMap[LIMIT_REG] != LIMIT_SWITCHES_OK) {
    steering_stepper.stop();
    registers.registerMap[MODE_REG] = HALTED;
  }
  switch (registers.registerMap[MODE_REG]) {
    case HALTED :
      STEPPER_SLEEP;
      break;
    case RELATIVE :
    case ABSOLUTE :
      steering_stepper.setSpeed(RUN_SPEED);
      steering_stepper.runSpeedToPosition();
      if (steering_stepper.distanceToGo() == 0) {
        registers.registerMap[MODE_REG] = HALTED;
      }
      break;
    case CONTINUOUS :
      steering_stepper.runSpeed();
      break;
    default :
      registers.registerMap[ERROR_REG] = BAD_MODE;
      break;
  }
  registers.reg.current_position = steering_stepper.currentPosition();
}

//----------------------------------------------------------------------
// receiveEvent : I2C data receive interrupt routine
//
// Receive a simple three byte I2C packet.
// Three bytes expected = register number + 2 data_bytes
//
void receiveEvent(int bytesReceived) {
  registers.reg.register_ptr = Wire.read();
  data1_byte = Wire.read();
  data2_byte = Wire.read();
  Serial.println(registers.reg.register_ptr);
  Serial.println(data1_byte);
  Serial.println(data2_byte);
  if (registers.reg.register_ptr > VERSION_REG) {
    registers.registerMap[ERROR_REG] = BAD_REGISTER_NO;
  } else {
    switch (registers.reg.register_ptr) {
      case REGISTER_POINTER :
        registers.registerMap[REGISTER_POINTER] = data1_byte;
        break;
      case COMMAND_REG :
        registers.registerMap[COMMAND_REG] = data1_byte;
        process_command(data1_byte);
        break;
      case STEPS_REG_0 :   // temp store until upper 2 bytes are sent
        temp_step_reg_0 = data1_byte;
        temp_step_reg_1 = data2_byte;
        break;
      case STEPS_REG_2 :   // loads REG_2/REG_3 and sets pointer to REG_2
        registers.registerMap[STEPS_REG_0] = temp_step_reg_0;
        registers.registerMap[STEPS_REG_1] = temp_step_reg_1;
        registers.registerMap[STEPS_REG_2] = data1_byte;
        registers.registerMap[STEPS_REG_3] = data2_byte;
        break;
      case MODE_REG :
        registers.registerMap[MODE_REG] = data1_byte;
        break;
      case STATUS_REG  :
      case LIMIT_REG   :
      case STEPS_REG_1 :
      case STEPS_REG_3 :
      case VERSION_REG :
        break;          // do nothing for these register writes 
      case RUN_SPEED :
        registers.registerMap[RUN_SPEED_0] = data1_byte;
        registers.registerMap[RUN_SPEED_1] = data2_byte;      
        break;
      case MAX_SPEED :
        registers.registerMap[MAX_SPEED_0] = data1_byte;
        registers.registerMap[MAX_SPEED_1] = data2_byte;      
        break;
      default :
        break;
    }
  }
}

//----------------------------------------------------------------------
// requestEvent : return a register byte value through I2C bus
//
// Register 'register-ptr' points to register value to be returned.
// This pointer will be auto incremented.
//
void requestEvent() {
  Wire.write(registers.registerMap[registers.reg.register_ptr++]);
  if (registers.reg.register_ptr > VERSION_REG) {
    registers.reg.register_ptr = 0;
  }
}

//----------------------------------------------------------------------
// process_command : Execute an I2C command
//
// If data was for 'command register' then this routine is executed.
//
void process_command(byte cmd) {
  switch (cmd) {
    case STOP :
      steering_stepper.stop();
//      STEPPER_SLEEP;
      registers.registerMap[MODE_REG] = HALTED;
      break;
    case POWER_DOWN :
//      STEPPER_SLEEP;
      registers.registerMap[MODE_REG] = HALTED;
      break;
    case MOVE_ABS :
      steering_stepper.moveTo(registers.reg.steps_requested);
      registers.registerMap[MODE_REG] = ABSOLUTE;
      STEPPER_WAKEUP;
      break;
    case MOVE_REL :
      steering_stepper.move(registers.reg.steps_requested);
      registers.registerMap[MODE_REG] = RELATIVE;
      STEPPER_WAKEUP;
      break;
    case MOVE_CONT :
      steering_stepper.move(registers.reg.steps_requested);
      registers.registerMap[MODE_REG] = CONTINUOUS;
      STEPPER_WAKEUP;
      break;
    case SET_ORIGIN :
      if (!steering_stepper.isRunning()) {
        steering_stepper.setCurrentPosition(0);
      } else {
        registers.registerMap[ERROR_REG] = BAD_SET_POSITION;
      }
      break;
    case SET_DEFAULT_VALUES :
      registers.reg.runspeed = RUN_SPEED;
      registers.reg.maxspeed = MAX_SPEED;
      registers.registerMap[MODE_REG] = HALTED;
      registers.reg.version  = CURRENT_VERSION;
      break;
    default :
      registers.registerMap[ERROR_REG] = BAD_COMMAND;
      break;
  }
}

//----------------------------------------------------------------------
// read_limits : read four limit switch inputs
//
// Data to be loaded into the command register needs to be processed
//
void read_limits(void) {

  registers.registerMap[LIMIT_REG] =
    (digitalRead(END_STOP_1) +
    (digitalRead(END_STOP_2)<<1) +
    (digitalRead(END_STOP_3)<<2) +
    (digitalRead(END_STOP_4)<<3)) & 0x0F;
}


