/*
 ** Tiberius primary CAN network bridge node
 *
 * Node provides a bridge between the Tiberius ethernet system and the
 * Tiberius CAN I/O network.
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
SerialDriver pc(USBTX, USBRX);     // tx, rx - buffered serial port
EthernetInterface eth;
UDPSocket tiberius_UDP_socket;

DigitalOut  led1(LED1);
DigitalOut  led2(LED2);
DigitalOut  led3(LED3);
DigitalOut  led4(LED4);
DigitalOut  probe_1_pin(p26);

debug_mode_t debug_mode;

//*******************************************
// Function templates
//
void         init(void);
void         run_test(void);

//*******************************************
// Static network parameters
//
static const char*          mbedIp       = "192.168.0.200";  //IP
static const char*          mbedMask     = "255.255.255.0";  // Mask
static const char*          mbedGateway  = "192.168.0.1";    //Gateway

#define  STATIC_IP

//*******************************************
// task templates.
//
void test_injection_task ( void const *args );
void debug_task (void const *args );
void CAN_out(void const *args );
void CAN_in( void const *args );
void UDP_out(void const *args );
void UDP_in( void const *args );
void execute_local_cmds( void const *args );

//*******************************************
// Create threads
//
osThreadDef(test_injection_task, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(debug_task, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(CAN_out, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(CAN_in, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(UDP_out, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(UDP_in, osPriorityNormal, DEFAULT_STACK_SIZE);
osThreadDef(execute_local_cmds, osPriorityNormal, DEFAULT_STACK_SIZE);

//*******************************************
// Mutex semaphores
//
osMutexId sysdata_mutex, debugdata_mutex;
osMutexDef(sysdata_mutex);          // protect system data
osMutexDef(debugdata_mutex);        // protect debug data

//*******************************************
// Define a timer for the clock scheduler
//
osTimerDef(clk_sched, clock_manager);

/********************************************
 * Data structures
 */
system_modes_t    sysmodes;
debug_data_t      debug_data;

unit_code_t sys_code = UNKNOWN;

/********************************************
 * Mail queues
 */
Mail<CAN_out_queue_t, 8> CAN_out_mail_box;     // CAN to UDP packet queue
Mail<CAN_in_queue_t, 8> CAN_in_mail_box;       // UDP to CAN command queue
Mail<local_cmd_queue_t, 8> local_cmd_mail_box;       // UDP to local command queue

Mail<UDP_queue_t, 8> UDP_out_mail_box;         // for UDP output messages

//
// format of command byte in UDP packet
//
union {
    uint8_t     value;
    struct {
        unsigned int    unused      : 5;
        unsigned int    reply       : 1;
        unsigned int    destination : 2;
    } bits;
} cmd; 

/********************************************
 * Task code
 */

/**
 * debug_task : send debug data to serial comms port
 *
 * Thread will be scheduled by the clock thread
 */
void debug_task (void const *args )
{
    if (debug_mode == GENERAL) {
        pc.printf("debug_task started\r\n");
    }
    FOREVER {
        osSignalWait(CLOCK_TRIGGER_SIGNAL, osWaitForever);

        osMutexWait(sysdata_mutex, osWaitForever);
        ;
        osMutexRelease(sysdata_mutex);

        if (debug_mode == GENERAL) {
            pc.printf("dummy\r\n");
        }
    }
}

//********************************************
// UDP output task
//
// Read items from UDP queue and send onto ethernet.
//
void UDP_out ( void const *args )
{
    FOREVER {
        osEvent evt = UDP_out_mail_box.get(osWaitForever);
        if (evt.status == osEventMail) {
            UDP_queue_t *mail = (UDP_queue_t*)evt.value.p;

            UDP_out_mail_box.free(mail);
        }
    }
}

//********************************************
// UDP input task
//
// Read UDP packets and dispatch to relevant queue.
// Data stored as a byte array.
// Byte 0 specifies the type of command.
//
void UDP_in ( void const *args )
{
    char buffer[64];

    UDPSocket MBED_server;
    MBED_server.bind(UDP_IN_PORT);
    Endpoint client;

    FOREVER {
        uint32_t byte_cnt = MBED_server.receiveFrom(client, buffer, sizeof(buffer));
        cmd.value = buffer[0];
        pc.printf("Buffer[0] = %x\r\n", buffer[0]);
        pc.printf("destination = %d\r\n", cmd.bits.destination);
        switch(cmd.bits.destination) {  // first byte contains type of command
            //
            // Commands to be executed on this mode
            //
            case LOCAL:
                switch (buffer[1]) {
                    case TOGGLE_LED1 :
                        led1 = !led1;
                        break;
                    default :
                        break;
                }
                break;
            //
            // commands to be copied to CAN bus.
            //
            case CANBUS:
                CAN_out_queue_t *message = CAN_out_mail_box.alloc();
                memcpy(message, &buffer[1], 16);
                pc.printf("Message ID = %d\r\n", message->message_id);
                pc.printf("Message byte0 = %d\r\n", message->data[0]);
                pc.printf("Message length = %d\r\n", message->message_length);
                CAN_out_mail_box.put(message);
                break;
                //
                //
                //
            default:
                break;
        }
    }
}

/**
 * Task to inject known data into CAN and ethernet system for test purposes
 *
 */
void test_injection_task ( void const *args )
{
    FOREVER {
        osDelay(1*1000);
//        CAN_out_queue_t *message = CAN_out_mail_box.alloc();
//        message->message_id = CMD_BASE_ID + FRONT_RIGHT;  // sys_code
//        message->data[0] = TOGGLE_LED1;
//        message->message_length = 1;
//        CAN_out_mail_box.put(message);
    }
}

/**
 * Task to process local commands that have come via UDP channel
 *
 */
void execute_local_cmds ( void const *args )
{
    FOREVER {
        osEvent evt = local_cmd_mail_box.get(osWaitForever);
        if (evt.status == osEventMail) {
            local_cmd_queue_t *command = (local_cmd_queue_t*)evt.value.p;
            switch (command->data[0]) {
                case TOGGLE_LED1 :
                    led1 = !led1;
                    break;
                default:
                    break;
            }
            local_cmd_mail_box.free(command);
        }
    }
}

/*********************************************
 ** init   initialise hardware and system
 */
void init(void)
{
//    s_mode = RUN;    // other mode is TEST
    debug_mode = NONE;
    //
    // Setup virtual COM port
    //
    pc.baud(COM_BAUD);
    //
    // Setup internet connection
    //
    #ifdef STATIC_IP
        eth.init(mbedIp,mbedMask,mbedGateway); // static IP
    #else
        eth.init();                            //Use DHCP
    #endif
    eth.connect();
    tiberius_UDP_socket.init();
    pc.printf("IP Address is %s\n", eth.getIPAddress());
    //
    // Setup CANbus
    //
    can1.frequency(CAN_FREQUENCY);
    can1.attach(can_callback, CAN::RxIrq);
    //
    // setup CAN filter
    //
    set_CAN_controller(CAN_CONTROLLER_0);
    disable_CAN_filter();
    init_can_filter_buffer();
    add_can_filter_id((CMD_BASE_ID + sys_code), EXPLICIT_11_BIT);
    load_CAN_filter_memory();
//    enable_CAN_filter();

    clock_ticks = NOS_TICKS_CLOCK_THREAD;
}

//********************************************
// run_test
//
// Run a test (with PID disabled)
//
void run_test(void)
{
    osDelay(20*1000);
}

/*********************************************/
int main()
{
osThreadId  temp_Id;

    init();

    if (debug_mode == GENERAL) {
        pc.printf("Hardware initialised\r\n");
    }
//
// Create tasks
//
// one-off tasks
//
    osThreadCreate(osThread(test_injection_task), NULL);
//
// clock tasks
//
    temp_Id =  osThreadCreate(osThread(debug_task), NULL);
    add_clk_thread(temp_Id, DEBUG_TASK_RATE);
//
// Event driven tasks tasks
//
    osThreadCreate(osThread(execute_local_cmds), NULL);
    osThreadCreate(osThread(CAN_out), NULL);
    osThreadCreate(osThread(CAN_in), NULL);
    osThreadCreate(osThread(UDP_out), NULL);
    osThreadCreate(osThread(UDP_in), NULL);
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
