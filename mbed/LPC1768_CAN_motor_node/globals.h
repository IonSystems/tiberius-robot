//
// globals.h : file to hold some general global defines, 
// =========
//
#include    "mbed.h"
#include    "cmsis_os.h"
#include    "SerialDriver.h"
#include    "MD03.h"
#include    "DRV8825_I2C.h"
#include    "CAN.h"
#include    "tiberius.h"
#include    "CAN_io.h"
#include    "qeihw.h"
#include    "clock_sched.h"

#ifndef     GLOBALS_H
#define     GLOBALS_H

#define     FOREVER     for(;;)
#define     HANG        for(;;)

//
// externs
//
extern SerialDriver      pc;               // allows this object to be seen in all other files
extern osMutexId sysdata_mutex, I2C_mutex, debugdata_mutex;   // mutexes
extern system_data_t   sysdata;
extern system_modes_t  sysmodes;
extern debug_data_t    debug_data;

extern DigitalOut  led1;
extern DigitalOut  led3;

extern MD03  md03;
extern CAN   can1;
extern DRV8825_I2C  DRV8825;
extern DigitalOut  probe_1_pin;

extern uint32_t   nos_clock_threads;
extern uint32_t   clock_ticks;

extern schedule_t schedule[MAX_CLOCK_THREADS];

extern unit_code_t sys_code;
extern debug_mode_t debug_mode;

extern Mail<CAN_out_queue_t, 8> CAN_out_mail_box;
extern Mail<CAN_queue_t, 8> CAN_in_mail_box;

#endif