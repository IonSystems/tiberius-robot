/*
* General constants and typedef structres for Tiberius motor control system
 */
#ifndef  TIBERIUS_H
#define  TIBERIUS_H

#define VERSION   0x10

//********************
// COM port data
//
#define     COM_BAUD    115200

//********************
// Motor data
//
#define     MOTOR_GEAR_RATIO    100
#define     SLOTS_IN_DISK        36
#define     MAXRPM             5000.0
#define     MINRPM              100.0
#define     SPEED_DEADBAND        5.0
#define     PWM_MAX             100
#define     PWM_MIN               0

//********************
// CAN data
//
#define     CAN_FREQUENCY        500000
#define     QEI_VELOCITY_TIMER    50000
//
// CAN message IDs
//
#define    CMD_BASE_ID     0x100
#define    SPEED_BASE_ID   0x200

//********************
// thread clock rates (samples per second)
//
#define    SERVO_TASK_RATE   10
#define    QEI_READ_RATE     20
#define    DEBUG_TASK_RATE    1

//********************
// Initial PID gain settings
//
#define     P_GAIN          0.02
#define     I_GAIN          0.1
#define     D_GAIN          0.00
#define     INTEGRAL_MAX    1000  

//********************
// enum defines
//
enum dir {FORWARD, BACKWARD};

//********************
// System data structure
//
typedef struct  {
    float       demanded_speed;  // rpm
    float       motor_speed;     // rpm of motor without gearbox
    float       Kp, Ki, Kd;      // gains for PID speed loop
    bool        enabled;         // used to enable/disable servo calculations
} system_data_t;

typedef struct  {
    uint8_t     operation;
    uint8_t     communication;
    uint8_t     speed_control;
} system_modes_t;

typedef struct  {
    uint16_t    pwm_drive_value; // current pwm duty cycle value
} debug_data_t;

typedef struct {
  uint32_t    message_id; 
  uint8_t     data[8]; 
  uint32_t     message_length;
} CAN_out_queue_t;

typedef struct {
  uint32_t    message_id;
  uint8_t     data[8]; 
  uint32_t    message_length; 
} CAN_queue_t;

typedef enum {FRONT_LEFT, FRONT_RIGHT, BACK_LEFT, BACK_RIGHT, UNKNOWN} unit_code_t;
typedef enum {NONE, GENERAL, PID_TEST} debug_mode_t;
typedef enum {TEST, RUN} sys_mode_t;
typedef enum {PID_P_GAIN = 0,
              TOGGLE_LED1,
              MOTOR_SPEED,
              MOTOR_PWM,
              STEERING_MOVE_REL,
              STEERING_MOVE_ABS,
              STEERING_ANGLE,
} CAN_cmds_t;

typedef enum {SUCCESS                    =  0, 
              FAIL                       = -1,
              CAN_FILTER_BUFFER_OVERFLOW = -2,
              BAD_CAN_CONTROLLER         = -3,
} error_codes_t;

//********************
// macros
//
#define SET_PROBE_1     probe_1_pin=1
#define CLR_PROBE_1     probe_1_pin=0

#endif