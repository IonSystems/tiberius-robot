/*
 * Information relevant to the scheduling of the set of clock initiated tasks (threads)
 */
#include "mbed.h"
 
#ifndef  CLOCK_SCHED_H
#define  CLOCK_SCHED_H

#define MAX_CLOCK_THREADS         8   // MAX number of clock related tasks
#define CLOCK_TRIGGER_SIGNAL   0x01

#define NOS_TICKS_CLOCK_THREAD    5

//*******************************************
// function templates
//
int32_t add_clk_thread(osThreadId Id, uint32_t rate);
void clock_manager ( void const *args );

//
// structure to hold info on a thread that is scheduled by clock thread
//
typedef struct {
    osThreadId  thread_id;      // thread identification number
    uint32_t    deadline;       // sample rate in units of samples/sec
    uint32_t    counter;        // countdown until next schedule time
} schedule_t;

#endif