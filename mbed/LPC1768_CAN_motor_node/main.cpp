/*
 ** Motor control node for Tiberius outdoor robot
 *
 * CAN connected node to provide velocity control of a brushed DC motor with
 * a quadrature encoder on the motor side of a 100:1 gear box.
 * Connects to an Arduino Nano to control a stepper motor that drives the steering.
 *
 * Author : Jim Herd
 *
 * Uses CMSIS-RTOS interface
 */
#include "globals.h"

//*******************************************
// Define hardware objects
//
CAN can1(p30, p29);
MD03  md03(p9, p10, 0xB0);         // sda, scl - MD03 H-bridge controller
SerialDriver pc(USBTX, USBRX);     // tx, rx - buffered serial port
DRV8825_I2C  DRV8825(p9, p10, (0x05<<1));

QEIHW qei(QEI_DIRINV_NONE, QEI_SIGNALMODE_QUAD, QEI_CAPMODE_4X, QEI_INVINX_NONE );

DigitalOut  led1(LED1);
DigitalOut  led3(LED3);
DigitalOut  probe_1_pin(p26);
DigitalIn   adr_bit0(p15);
DigitalIn   adr_bit1(p16);

debug_mode_t debug_mode;
sys_mode_t   s_mode;

//*******************************************
// Function templates
//
void         init(void);
void         run_test(void);
unit_code_t  get_name(void);

//*******************************************
// task templates.
//
void motor_spd_servo ( void const *args );
void local_test_task ( void const *args );
void QEI_read ( void const *args );
void debug_task (void const *args );
// void command_task(void const *args );
void CAN_out(void const *args );
void CAN_in( void const *args );

//*******************************************
// Create threads
//
osThreadDef(motor_spd_servo, osPriorityHigh, DEFAULT_STACK_SIZE);
osThreadDef(local_test_task, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(QEI_read, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(debug_task, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(CAN_out, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(CAN_in, osPriorityNormal, DEFAULT_STACK_SIZE);

//*******************************************
// Mutex semaphores
//
osMutexId sysdata_mutex, I2C_mutex, debugdata_mutex;
osMutexDef(sysdata_mutex);          // protect system data
osMutexDef(I2C_mutex);              // protect access to I2C bus (MD03, Arduino Nano)
osMutexDef(debugdata_mutex);        // protect debug data

//*******************************************
// Define a timer for the clock scheduler
//
osTimerDef(clk_sched, clock_manager);

/********************************************
 * Data structures
 */
system_data_t     sysdata;
system_modes_t    sysmodes;
debug_data_t      debug_data;

unit_code_t sys_code = UNKNOWN;

//*******************************************
// Mail queues
//
Mail<CAN_out_queue_t, 8> CAN_out_mail_box;     // for CAN output messages
Mail<CAN_queue_t, 8> CAN_in_mail_box;          // for CAN input command;

/**
 * debug_task : send debug data to serial comms port
 *
 * Thread will be scheduled by the clock thread
 */
void debug_task (void const *args )
{
    uint32_t    speed, pwm_duty_cycle;
    
    if (debug_mode == GENERAL) {
        pc.printf("debug_task started\r\n");
    }
    FOREVER {
        osSignalWait(CLOCK_TRIGGER_SIGNAL, osWaitForever);
        
        osMutexWait(sysdata_mutex, osWaitForever);
            speed = sysdata.motor_speed;
            pwm_duty_cycle = debug_data.pwm_drive_value;
        osMutexRelease(sysdata_mutex);
 
        if (debug_mode == GENERAL) {       
//            pc.printf("Motor speed = %d :: pwm_value = %d\r\n", speed, pwm_duty_cycle);
        }
    }
}

//********************************************
// motor_spd_servo : speed control task for motor
//
// Implements simple PID controller
//
//Notes
//     * Stop motor if demanded speed is < minimum value
//     * Apply deadband to error - do nothing if in deadband
//     * Limit output to 0 to 100 (%) range
//     * Limit integral windup
//     * sequence number (repeats after 13 years)
//     * If 'enabled' is false, do calculations but do output to motor
//
void motor_spd_servo ( void const *args )
{
    float       Kp, Ki, Kd;
    float       error, previous_error;
    float       measured_speed, demanded_speed;
    float       proportional, integral, derivative, dt, raw_output, output;
    uint32_t    direction, sequence_number;
  // set all necessary varibles to zero
    previous_error = 0.0;
    proportional = 0.0; integral = 0.0; derivative = 0.0;
    dt = 1.0/SERVO_TASK_RATE;
    sequence_number = 0;
    
    FOREVER {
        sequence_number++;
      // wait for trigger signal (Typ 10Hz)
        osSignalWait(CLOCK_TRIGGER_SIGNAL, osWaitForever);
//        SET_PROBE_1;
      // get relevant shared data
        osMutexWait(sysdata_mutex, osWaitForever);
            demanded_speed = sysdata.demanded_speed;
            measured_speed = sysdata.motor_speed;
            Kp = sysdata.Kp; Ki = sysdata.Ki; Kd = sysdata.Kd;  
        osMutexRelease(sysdata_mutex);
      // don't try to run below a minimum speed
        if (abs(demanded_speed) < MINRPM) {
            if (sysdata.enabled == true) {
                osMutexWait(I2C_mutex, osWaitForever);
                  md03.set_speed(0);
                   md03.stop();
                osMutexRelease(I2C_mutex);
            }
            proportional = 0.0; integral = 0.0; derivative = 0.0; previous_error = 0.0;
            osMutexWait(debugdata_mutex, osWaitForever);
              debug_data.pwm_drive_value = 0;
            osMutexRelease(debugdata_mutex);
            if (debug_mode == PID_TEST) {       
                pc.printf("%f,%f,%f,%f,MR\r\n", demanded_speed, measured_speed, raw_output, error);
            }        
//            CLR_PROBE_1;
            continue;  // wait for next sample time
        }
        direction = FORWARD;
        if (demanded_speed < 0) {
            direction = BACKWARD;
        } 
      // compute error and check deadband
        error = demanded_speed - measured_speed;
        if (fabs(error) < SPEED_DEADBAND) {
            if (debug_mode == PID_TEST) {       
                pc.printf("%f,%f,%f,%f,DB\r\n", demanded_speed, measured_speed, raw_output, error);
            }        
//            CLR_PROBE_1;
            continue;  // wait for next sample time
        }
      // compute proportional error
        proportional = error;
      // compute integral error and apply anti-windup
        integral = integral + (error * dt);
        if (integral >  INTEGRAL_MAX) { 
            integral =  INTEGRAL_MAX; 
        }
        if (integral < -INTEGRAL_MAX) { 
            integral = -INTEGRAL_MAX; 
        } 
      // compute derivative error       
        derivative = (error - previous_error)/dt;
        raw_output = (Kp * proportional) + (Ki * integral) + (Kd * derivative);
      // convert to motor drive command
        output = raw_output;
        if (raw_output > PWM_MAX) {
            output = PWM_MAX;
        }
        if (raw_output < PWM_MIN) {
            output = PWM_MIN;
        }
      // send new value to motor drive system  
        if (sysdata.enabled == true) {      
            if (direction == FORWARD) {
                osMutexWait(I2C_mutex, osWaitForever);
                  md03.set_speed((uint32_t)(output));
                  md03.move_forward();
                osMutexRelease(I2C_mutex);    
            } else {
                osMutexWait(I2C_mutex, osWaitForever);
                  md03.set_speed((uint32_t)(output));
                  md03.move_reverse();
                osMutexRelease(I2C_mutex);                
            }
        } 
        osMutexWait(debugdata_mutex, osWaitForever);
            debug_data.pwm_drive_value = output;
        osMutexRelease(debugdata_mutex);
      // update error
        previous_error = error;
      // output measured speed on CAN bus
        CAN_out_speed(measured_speed, sequence_number);
      // Optional dump of debug data
        if (debug_mode == PID_TEST) {       
            pc.printf("%f,%f,%f,%f,OK\r\n", demanded_speed, measured_speed, raw_output, error);
        }        
//        CLR_PROBE_1;
    }
}

//********************************************
// Read quadrature encoder task
//
// Access the on-chip quadrature encode hardware of the LPC1768 chip.
//
void QEI_read ( void const *args )
{
    uint32_t vel;

    if (debug_mode == GENERAL) {
        pc.printf("QEI_read started\r\n");
    }
    FOREVER {
        osSignalWait(CLOCK_TRIGGER_SIGNAL, osWaitForever);
        vel = qei.GetVelocityCap();
        
        osMutexWait(sysdata_mutex, osWaitForever);
          sysdata.motor_speed = (((float)vel * QEI_READ_RATE) / (SLOTS_IN_DISK * 4)) * 60;
        osMutexRelease(sysdata_mutex);
    }
}
//********************************************
/* Thread 5 */
void HBridge_read ( void const *args )
{
    FOREVER {
        osSignalWait(CLOCK_TRIGGER_SIGNAL, osWaitForever);
    }
}

//********************************************
// Thread 6
void local_test_task ( void const *args )
{
    FOREVER {
        osDelay(10*1000);
  //
  // insert TOGGLE_LED1 test command into CAN input queue
  //    
//        CAN_queue_t *CAN_message = CAN_in_mail_box.alloc();
//        CAN_message->message_id = CMD_BASE_ID + sys_code;
//        CAN_message->data[0] = TOGGLE_LED1;
//        CAN_message->message_length = 1;
//        CAN_in_mail_box.put(CAN_message);
    }
/*    
    if (s_mode == TEST) {
        run_test();
        HANG;
    }
    
    osMutexWait(I2C_mutex, osWaitForever);
      md03.set_speed(0);
    osMutexRelease(I2C_mutex);  
       
    osMutexWait(sysdata_mutex, osWaitForever);
        sysdata.demanded_speed = 4500;    // rpm
    osMutexRelease(sysdata_mutex); 
    
    osDelay(30*1000);
 
    osMutexWait(sysdata_mutex, osWaitForever);
        sysdata.demanded_speed = 2000;    // rpm
    osMutexRelease(sysdata_mutex); 
    
    osDelay(20*1000); 

    osMutexWait(sysdata_mutex, osWaitForever);
        sysdata.demanded_speed = 0;
    osMutexRelease(sysdata_mutex);
    */     
}

/*********************************************
 ** init   initialise hardware and system
 */
void init(void)
{
    s_mode = RUN;    // other mode is TEST
    debug_mode = GENERAL;   //NONE;  
    
    if ((sys_code = get_name()) == UNKNOWN) {
        led1 = 1; led3 = 1;                     // error
        HANG;
    };
    
    pc.baud(COM_BAUD);

    can1.frequency(CAN_FREQUENCY);
    can1.attach(can_callback, CAN::RxIrq);
  //
  // setup CAN filter
  //
    set_CAN_controller(CAN_CONTROLLER_1);   // CAN controller 0 not used on MBED
    disable_CAN_filter();
    init_can_filter_buffer();
    add_can_filter_id((CMD_BASE_ID + sys_code), EXPLICIT_11_BIT);
//    load_CAN_filter_memory();  // ** problem
//    enable_CAN_filter();

    qei.SetDigiFilter(4UL); // 480ul
    qei.SetMaxPosition(0x0FFFFFFF);
    qei.SetVelocityTimerReload_us(QEI_VELOCITY_TIMER);  // velocity timer set to typ. 50 milliseconds

    clock_ticks = NOS_TICKS_CLOCK_THREAD;
    // set central data store to known values.
    osMutexWait(sysdata_mutex, osWaitForever);
        sysdata.demanded_speed = 0;  // rps
        sysdata.motor_speed = 0;     // rps
        sysdata.Kp = P_GAIN; 
        sysdata.Ki = I_GAIN; 
        sysdata.Kd = D_GAIN;  
        sysdata.enabled = false;
    osMutexRelease(sysdata_mutex);
    // reset debug data    
    osMutexWait(debugdata_mutex, osWaitForever);
        debug_data.pwm_drive_value = 0;    
    osMutexRelease(debugdata_mutex);
    
    osMutexWait(I2C_mutex, osWaitForever);
      md03.set_speed(0);
      md03.stop();
    osMutexRelease(I2C_mutex); 
    
//    osMutexWait(I2C_mutex, osWaitForever);   
//      DRV8825.write_reg(COMMAND_REG, MOVE_REL, 0);
//    osMutexRelease(I2C_mutex); 
}

/*********************************************
 ** get_name   Find out which wheel is driven by this unit
 */
unit_code_t  get_name(void)
{
    return (unit_code_t)((adr_bit1<<1) + adr_bit0);
}

//********************************************
// run_test
//
// Run a test (with PID disabled)
//
void run_test(void)
{
    osMutexWait(I2C_mutex, osWaitForever);
      md03.set_speed(100);
      md03.move_forward();
    osMutexRelease(I2C_mutex); 
  
    osDelay(20*1000);
    
    osMutexWait(I2C_mutex, osWaitForever);
      md03.stop();
    osMutexRelease(I2C_mutex);
} 

/*********************************************/
int main()
{
    osThreadId  temp_Id;
    CANMessage  msg;

    init();

    if (debug_mode == GENERAL) {
        pc.printf("Hardware initialised\r\n");
    }
//
// Create tasks
//
// one-off tasks
//
//    osThreadCreate(osThread(local_test_task), NULL);
//
// clock tasks
//
    temp_Id =  osThreadCreate(osThread(QEI_read), NULL);
    add_clk_thread(temp_Id, QEI_READ_RATE);
    
    temp_Id =  osThreadCreate(osThread(debug_task), NULL);
    add_clk_thread(temp_Id, DEBUG_TASK_RATE);
    
    temp_Id =  osThreadCreate(osThread(motor_spd_servo), NULL);
    add_clk_thread(temp_Id, SERVO_TASK_RATE); 
//
// Event driven tasks tasks
// 
    osThreadCreate(osThread(CAN_out), NULL);
    osThreadCreate(osThread(CAN_in), NULL);  
//
// start clock scheduler task
//
    osTimerId timer_0 = osTimerCreate(osTimer(clk_sched), osTimerPeriodic, (void *)0);
    osTimerStart(timer_0, NOS_TICKS_CLOCK_THREAD);

    FOREVER {
        led3 = !led3;
        wait(1);
    }
}
