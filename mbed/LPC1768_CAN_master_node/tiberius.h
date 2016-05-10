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
// CAN data
//
#define     CAN_FREQUENCY        500000
//
// CAN message IDs
//
#define    CMD_BASE_ID     0x100
#define    SPEED_BASE_ID   0x200

//********************
// thread clock rates (samples per second)
//
#define    DEBUG_TASK_RATE    1

//********************
// enum defines
//
enum dir {FORWARD, BACKWARD};
//
// UDP related constants
//
#define     UDP_PACKET_SIZE     32  
#define     UDP_IN_PORT         43442   // 0xA962
#define     UDP_OUT_PORT        43443

//********************
// System data structure
//
typedef struct  {

} system_modes_t;

typedef struct  {
 
} debug_data_t;

typedef struct {
    uint8_t     data[UDP_PACKET_SIZE];
    uint32_t    port;
} UDP_queue_t;

typedef struct {
  uint32_t    message_id; 
  uint8_t     data[8]; 
  uint32_t    message_length;
} CAN_out_queue_t;

typedef struct {
  uint32_t    message_id;
  uint8_t     data[8]; 
  uint32_t    message_length; 
} CAN_in_queue_t;

typedef struct {
  uint8_t     data[32]; 
} local_cmd_queue_t;

typedef enum {FRONT_LEFT, FRONT_RIGHT, BACK_LEFT, BACK_RIGHT, UNKNOWN} unit_code_t;
typedef enum {NONE, GENERAL} debug_mode_t;

typedef enum {
    TOGGLE_LED1 = 1,
    SET_PWM,
} commands_t;
 
typedef enum {
    LOCAL, 
    CANBUS
} cmd_dest_t;

typedef enum {
    SUCCESS                    =  0, 
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