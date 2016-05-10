//
// globals.h : file to hold some general global defines, 
// =========
//
#include    "mbed.h"
#include    "cmsis_os.h"
#include    "SerialDriver.h"
#include    "CAN.h"
#include    "EthernetInterface.h"
#include    "tiberius.h"
#include    "CAN_io.h"
#include    "clock_sched.h"

#ifndef     GLOBALS_H
#define     GLOBALS_H

#define     FOREVER     for(;;)
#define     HANG        for(;;)

//
// externs
//
extern SerialDriver      pc;               // allows this object to be seen in all other files
extern osMutexId sysdata_mutex, debugdata_mutex;   // mutexes
extern system_modes_t  sysmodes;
extern debug_data_t    debug_data;

extern DigitalOut  led1;
extern DigitalOut  led2;
extern DigitalOut  led3;
extern DigitalOut  led4;

extern CAN   can1;
extern DigitalOut  probe_1_pin;
extern EthernetInterface eth;
extern UDPSocket tiberius_UDP_socket;

extern uint32_t   nos_clock_threads;
extern uint32_t   clock_ticks;

extern schedule_t schedule[MAX_CLOCK_THREADS];

extern unit_code_t sys_code;

extern Mail<CAN_out_queue_t, 8> CAN_out_mail_box;
extern Mail<CAN_in_queue_t, 8> CAN_in_mail_box;
extern Mail<local_cmd_queue_t, 8> local_cmd_mail_box;

#endif