/*
 ** Clock scheduler data and functions
 *
 * MBED RTOS does not easily allow a set of tasks to be schedules at
 * different sample rates. This system uses a single timer activated task 
 * to implement the necessary feature.  Each registered task is activated
 * by a SIGNAL/WAIT semaphore.
 *
 */
#include "globals.h"

uint32_t   nos_clock_threads = 0;
uint32_t   clock_ticks;

//
// structure to hold info on threads that are scheduled by clock thread
//
schedule_t schedule[MAX_CLOCK_THREADS];

/** 
 * Add thread to table of 'clock_manager' scheduled threads
 *
 * @param   Id      Id handle for a thread
 * @param   rate    rate(times/sec) at which thread is to be run
 * @return          OK is successful; FAIL if >= MAX_CLOCK_THREADS
 */
int32_t add_clk_thread(osThreadId Id, uint32_t rate)
{
    if (nos_clock_threads >= MAX_CLOCK_THREADS) {
        return -1;
        }
    schedule[nos_clock_threads].thread_id = Id;
    schedule[nos_clock_threads].deadline = (1000 / (rate * NOS_TICKS_CLOCK_THREAD));
    schedule[nos_clock_threads].counter = schedule[nos_clock_threads].deadline;
    nos_clock_threads++;
    return 0;
}

///////////////////////////////////////////////////////////
// Clock_manager : trigger clock related threads
//
// This is the single system timer.  Uses signals to activate other threads that
// have priority.
//
// 'struct schedule' contains all the required information to count down each of
// the clock controlled tasks.
//
// Algorithm
//      foreach clock scheduled task
//          decrement counter
//          if counter is zero 
//              send signal to task
//              reset associated counter
//
void clock_manager ( void const *args )
{
    uint32_t    i;

    clock_ticks++;

    for (i=0 ; i < nos_clock_threads ; i++) {
        schedule[i].counter--;
        if (schedule[i].counter == 0) {
            schedule[i].counter = schedule[i].deadline;                  // reset counter
            osSignalSet(schedule[i].thread_id, CLOCK_TRIGGER_SIGNAL);    // trigger task
        }
    }
}