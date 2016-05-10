//----------------------------------------------------------------------
//defines
//----------------------------------------------------------------------
#define CURRENT_VERSION    0x10

#define STEP_PIN          2    // D2 to step input of DRV8825
#define DIR_PIN           3    // D3 to direction input of DRV8825
#define SLEEP_PIN         7
#define RESET_PIN         8
#define BOARD_LED        13
#define END_STOP_1       14
#define END_STOP_2       15
#define END_STOP_3       16
#define END_STOP_4       17

//----------------------------------------------------------------------
//macros
//----------------------------------------------------------------------
#define STEPPER_SLEEP    digitalWrite(SLEEP_PIN, LOW);
#define STEPPER_WAKEUP   digitalWrite(SLEEP_PIN, HIGH);delay(DRV8825_WAKEUP_TIME);
#define STEPPER_RESET    digitalWrite(RESET_PIN, LOW);delayMicroseconds(50);digitalWrite(RESET_PIN, HIGH);
//----------------------------------------------------------------------
// Commands
//----------------------------------------------------------------------
enum  {
  STOP,
  POWER_DOWN,
  MOVE_ABS,
  MOVE_REL,
  MOVE_CONT,
  GET_CURRENT_POSITION,
  SET_ORIGIN,
  SET_DEFAULT_VALUES,
} DRV8825_COMMAND_SET;
//----------------------------------------------------------------------
// Errors
//----------------------------------------------------------------------
enum DRV_errors {
  DRV_OK,
  BAD_REGISTER_NO,
  BAD_COMMAND,
  BAD_MODE,
  BAD_SET_POSITION,
} ;
//----------------------------------------------------------------------
// Modes
//----------------------------------------------------------------------
enum {
  HALTED,
  RELATIVE,
  ABSOLUTE,
  CONTINUOUS,
} ;
