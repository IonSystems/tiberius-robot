/*
 ** Routines to support CAN input/output
 *
 */
#include "globals.h"

//
// buffer for CAN filter commands
//
struct    CAN_filter_item  CAN_filter_list[MAX_CAN_FILTER_ENTRIES];
uint32_t  CAN_filter_list_pt;
uint32_t  CAN_controller;
uint8_t   nos_standard_explicit, nos_standard_group, nos_extended_explicit, nos_extended_group;

//
// Union structure to allow easy access to the bytes of ints/floats
//
union {
    float       float_val;
    uint16_t    u16_val[2];
    int16_t     s16_val[2];
    uint32_t    u32_val;
    int32_t     s32_val;
    uint8_t     u8[4];
} data;


//********************************************
// CAN output task
//
// Read items from CAN queue and send onto CAN bus.
//
void CAN_out ( void const *args )
{
    FOREVER {
        osEvent evt = CAN_out_mail_box.get(osWaitForever);
//        SET_PROBE_1;
        if (evt.status == osEventMail) {
            CAN_out_queue_t *mail = (CAN_out_queue_t*)evt.value.p;
            can1.write(CANMessage(mail->message_id, (char *)(&mail->data[0]), mail->message_length));
            CAN_out_mail_box.free(mail);
        }
//        CLR_PROBE_1;
    }
}

//********************************************
// Process messages received from CAN input channel
//
// CAN callback routine will fill this queue.
//
void CAN_in ( void const *args )
{
    float    f_value;
    uint32_t pwm_value, direction, reg_value;

    FOREVER {
        osEvent evt = CAN_in_mail_box.get(osWaitForever);
        if (debug_mode == GENERAL) {
            pc.printf("CAN in\r\n");
        }
        if (evt.status == osEventMail) {
            CAN_queue_t *mail = (CAN_queue_t*)evt.value.p;
            if (mail->message_id == (CMD_BASE_ID + sys_code)) {
                switch (mail->data[0]) {
                    case PID_P_GAIN :
                        memcpy(&f_value, &mail->data[0], 4);
                        break;
                    case TOGGLE_LED1 :
                        led1 = !led1;
                        break;  
                    case MOTOR_SPEED :
                        break;
                    case MOTOR_PWM :
                        pc.printf("direction = %d\r\n", mail->data[1]);
                        pc.printf("pwm value = %d\r\n", mail->data[2]);
                        direction = mail->data[1];
                        pwm_value = mail->data[2];
                        if (pwm_value > 100) {  // set upper limit to 100
                            pwm_value = 100;
                        }
                        if (pwm_value < 5) {    // lower limit to zero
                            pwm_value = 0;
                        }
                        if (direction == FORWARD) {
                            osMutexWait(I2C_mutex, osWaitForever);
                              md03.set_speed(pwm_value);
                              md03.move_forward();
                            osMutexRelease(I2C_mutex);    
                        } else {
                            osMutexWait(I2C_mutex, osWaitForever);
                              md03.set_speed(pwm_value);
                              md03.move_reverse();
                            osMutexRelease(I2C_mutex);                
                        }
                        break; 
                    case STEERING_MOVE_REL :
                    case STEERING_MOVE_ABS :
                        pc.printf("command = %d\r\n", mail->data[1]);
                        pc.printf("byte 1  = %d\r\n", mail->data[2]);
                        pc.printf("byte 2  = %d\r\n", mail->data[3]);
                        osMutexWait(I2C_mutex, osWaitForever);
                          reg_value = DRV8825.read_reg(CUR_POS_REG_0);
                        osMutexRelease(I2C_mutex); 
                        pc.printf("limit register = %d\r\n", reg_value);
                        osMutexWait(I2C_mutex, osWaitForever);
                          DRV8825.write_reg(STEPS_REG_0, mail->data[1], mail->data[2]);
                          DRV8825.write_reg(STEPS_REG_2, mail->data[3], mail->data[4]);  
                          if (mail->data[0] == STEERING_MOVE_REL) {
                              DRV8825.write_reg(COMMAND_REG, MOVE_REL, 0);
                          } else {
                              DRV8825.write_reg(COMMAND_REG, MOVE_ABS, 0);
                          }  
                        osMutexRelease(I2C_mutex); 
                        break;                                                             
                    case STEERING_ANGLE :
                        break;                              
                    default:
                        break;
                }
            }
            CAN_in_mail_box.free(mail);
        }
    }
}

/**
 * CAN read callback function
 *
 * Called when a CAN message is received.  Messages relevant to this system
 * are copied into a CAN queue to be dealt with by task 'CAN_in'.
 */
void can_callback()
{
    CANMessage msg;

    SET_PROBE_1;
    can1.read(msg);
    if (msg.id == (CMD_BASE_ID + sys_code)) {
        CAN_queue_t *CAN_message = CAN_in_mail_box.alloc();
        CAN_message->message_id = msg.id;
        for (int i=0; i<msg.len ; i++) {
            CAN_message->data[i] = msg.data[i];
        }
        CAN_message->message_length = msg.len;
        CAN_in_mail_box.put(CAN_message);
    }
    // re-attach callback for next message
    can1.attach(can_callback, CAN::RxIrq);
    CLR_PROBE_1;
}

//********************************************
// Send speed CAN message
//
// Collect data for a measured speed CAN message and place in the
// CAN message output queue.
//
void CAN_out_speed(float measured_speed, uint32_t sequence_number)
{
    CAN_out_queue_t *speed_message = CAN_out_mail_box.alloc();

    // format data
    speed_message->message_id = SPEED_BASE_ID + sys_code;
    data.float_val = measured_speed;
    speed_message->data[0] = data.u8[0];
    speed_message->data[1] = data.u8[1];
    speed_message->data[2] = data.u8[2];
    speed_message->data[3] = data.u8[3];
    data.u32_val = sequence_number;
    speed_message->data[4] = data.u8[0];
    speed_message->data[5] = data.u8[1];
    speed_message->data[6] = data.u8[2];
    speed_message->data[7] = data.u8[3];
    speed_message->message_length = 8;
    // submit CAN message data structure the CAN mail queue
    CAN_out_mail_box.put(speed_message);
} 

/**
 * set active CAN controller
 *
 * Ensure that filter list buffer is initialised to a cleared state.
 */
int32_t set_CAN_controller(uint32_t  controller)
{
    switch (controller) {
      case CAN_CONTROLLER_0:
        CAN_controller = controller;
        break;
      case CAN_CONTROLLER_1:
        CAN_controller = controller;
        break; 
      default:
        return BAD_CAN_CONTROLLER;
    }
    return SUCCESS;
}       

/**
 * initialise filter list buffer
 *
 * Ensure that filter list buffer is initialised to a cleared state.
 */
void init_can_filter_buffer(void)
{
    for (int i=0 ; i < MAX_CAN_FILTER_ENTRIES ; i++) {
        CAN_filter_list[i].filter_type = CLEAR;
        CAN_filter_list[i].state = UNALLOCATED;
    }
    CAN_filter_list_pt = 0;
  // clear id mode counters
    nos_standard_explicit = 0;
    nos_standard_group    = 0;
    nos_extended_explicit = 0;
    nos_extended_group    = 0;
}

/**
 *  add CAN id into next available slot in CAN filter buffer. Checks for
 *  buffer full condition.
 *
 * @param   id    id of CAN packet to be recognised by filter
 * @param   mode  EXPLICIT_11_BIT or EXPLICIT_29_BIT
 * @return        SUCCESS or CAN_FILTER_BUFFER_OVERFLOW
 */
int32_t add_can_filter_id(uint32_t id, uint8_t mode)
{
    if (CAN_filter_list_pt >= MAX_CAN_FILTER_ENTRIES) {
        return  CAN_FILTER_BUFFER_OVERFLOW;
    }
    CAN_filter_list[CAN_filter_list_pt].filter_type = mode;
    CAN_filter_list[CAN_filter_list_pt].state = UNALLOCATED;
    CAN_filter_list[CAN_filter_list_pt].id_1 = id;
    CAN_filter_list_pt++;
    if (mode == EXPLICIT_11_BIT) {
        nos_standard_explicit++;
    } else {
        nos_extended_explicit++;
    }
    return SUCCESS;
}

/**
 * add an id range into the next available slot in the CAN filter buffer.
 * Recognise id in range     (low_id <= id <= id_high)
 * Checks for buffer full condition.
 *
 * @param   low_id    low end of id group
 * @param   high_id   high end of id group
 * @param   mode      GROUP_11_BIT or GROUP_29_BIT
 * @return            SUCCESS or CAN_FILTER_BUFFER_OVERFLOW
 */
int32_t add_can_filter_group(uint16_t low_id, uint16_t high_id, uint8_t mode)
{
    if (CAN_filter_list_pt >= MAX_CAN_FILTER_ENTRIES) {
        return  CAN_FILTER_BUFFER_OVERFLOW;
    }
    CAN_filter_list[CAN_filter_list_pt].filter_type = mode;
    CAN_filter_list[CAN_filter_list_pt].state = UNALLOCATED;
    CAN_filter_list[CAN_filter_list_pt].id_1 = low_id;
    CAN_filter_list[CAN_filter_list_pt].id_2 = high_id;
    CAN_filter_list_pt++;
    return SUCCESS;
}

/**
 * enable CAN id filter on LPC1768 device
 */
void enable_CAN_filter(void)
{
    LPC_CANAF->AFMR = 0x00000000;
}

/**
 * disable LPC1768 CAN id filter and allow all packets to be received
 */
void disable_CAN_filter(void)
{
    LPC_CANAF->AFMR = 0x00000002;
}

/**
 * load CAN buffer into CAN subsystem 512 word RAM buffer
 *
 * 1. save current state of filter enable/disable state
 * 2. scan through buffer 
 */
void load_CAN_filter_memory(void)
{
    uint32_t  AFMR_temp, i, filter_list_pt, ID_table_pt, mask, nos_rules, odd_rule;

    AFMR_temp = LPC_CANAF->AFMR;
    LPC_CANAF->AFMR = 0x00000001;
//
// create 11-bit explicit filter rules.
// Single rule and odd number of rules need special care.
//    
    filter_list_pt = 0;
    ID_table_pt = 0;                            // word pointer
    LPC_CANAF->SFF_sa = ID_table_pt << 2;       // convert to bytes
    if (nos_standard_explicit > 0) {
//        LPC_CANAF->SFF_sa = ID_table_pt << 2;  // convert to bytes
        if (nos_standard_explicit == 1) {
            mask  = ((CAN_filter_list[filter_list_pt].id_1 << 16) | (CAN_controller << 29)) & 0xE7FF0000;
            LPC_CANAF_RAM->mask[ID_table_pt] = mask; //  0x21013000
            filter_list_pt++;
            ID_table_pt++;
        } else {
            nos_rules = nos_standard_explicit / 2;
            odd_rule  = nos_standard_explicit % 2;
            for (i=0 ; i < nos_rules ; i++) {
                mask  = ((CAN_filter_list[filter_list_pt ].id_1 << 16) | (CAN_controller << 29)) & 0xE7FF0000;
                mask |= (((CAN_filter_list[filter_list_pt + 1].id_1) | (CAN_controller << 13)) & 0x0000E7FF);
                LPC_CANAF_RAM->mask[ID_table_pt + i] = mask;
                filter_list_pt += 2;
                ID_table_pt++;                
            }
            if (odd_rule == 1) {
                mask  = ((CAN_filter_list[filter_list_pt].id_1 << 16) | (CAN_controller << 29)) & 0xE7FF0000;
                LPC_CANAF_RAM->mask[ID_table_pt] = mask; 
                filter_list_pt++;
                ID_table_pt++;  
            }
        }
    }
//
// create 11-bit group filter rules
//
    LPC_CANAF->SFF_GRP_sa = ID_table_pt << 2; 
    if (nos_standard_group > 0) {
//        LPC_CANAF->SFF_GRP_sa = ID_table_pt << 2; 
        for (i=0 ; i < (nos_standard_group) ; i++) {
            mask  = ((CAN_filter_list[filter_list_pt].id_1 << 16) | (CAN_controller << 29)) & 0xE7FF0000;
            mask |= (((CAN_filter_list[filter_list_pt].id_2) | (CAN_controller << 13)) & 0x0000E7FF);
            LPC_CANAF_RAM->mask[ID_table_pt] = mask;
            filter_list_pt++;
            ID_table_pt++;
        }
    }
//
// create 29-bit explicit filter rules
//
    LPC_CANAF->EFF_sa = ID_table_pt << 2;
    if (nos_extended_group > 0) {
//        LPC_CANAF->EFF_sa = ID_table_pt << 2;
        for (i=0 ; i < (nos_extended_explicit) ; i++) {
            LPC_CANAF_RAM->mask[ID_table_pt] = (CAN_controller << 29) | CAN_filter_list[filter_list_pt].id_1;
            ID_table_pt++;
            filter_list_pt++;    
        }
    }
//
// create 29-bit group filter rules (each rule uses 2 words of CAN RAM memory)
//
    LPC_CANAF->EFF_GRP_sa = (ID_table_pt << 2); 
    LPC_CANAF->ENDofTable = (ID_table_pt << 2);
    if (nos_extended_group > 0) {
//        LPC_CANAF->EFF_GRP_sa = (ID_table_pt << 2); 
        for (i=0 ; i < (nos_extended_group) ; i=i+2) {
            LPC_CANAF_RAM->mask[ID_table_pt + i]   = (CAN_controller << 29) | CAN_filter_list[filter_list_pt + i].id_1;
            LPC_CANAF_RAM->mask[ID_table_pt + i + 1] = (CAN_controller << 29) | CAN_filter_list[filter_list_pt+ i].id_2;
            filter_list_pt++;
            ID_table_pt += 2;
        }
        LPC_CANAF->EFF_GRP_sa = (ID_table_pt << 2);
        LPC_CANAF->ENDofTable = (ID_table_pt << 2);                
    }
//    
//    LPC_CANAF->AFMR = AFMR_temp;   // AFMR_temp;
}

/**
 * Sort CAN baffer into an ordered format (low id's first)
 *
 * 1. standard 11-bit explicit commands 
 * 2. standard 11-bit group commands
 * 3. extended 29-bit explicit commands
 * 4. extended 29-bit group commands
 *
 * Null at this time.  Assume that set of filter masks are loaded into
 * the buffer in the corect order.
 */
void sort_CAN_buffer(void)
{
    return;
}