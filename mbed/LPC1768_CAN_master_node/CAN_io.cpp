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
        SET_PROBE_1;
        if (evt.status == osEventMail) {
            CAN_out_queue_t *mail = (CAN_out_queue_t*)evt.value.p;
            can1.write(CANMessage(mail->message_id, (char *)(&mail->data[0]), mail->message_length));
            CAN_out_mail_box.free(mail);
        }
        CLR_PROBE_1;
    }
}

//********************************************
// Process messages received from CAN input channel
//
// CAN callback routine will fill this queue.
//
void CAN_in ( void const *args )
{

    FOREVER {
        osEvent evt = CAN_in_mail_box.get(osWaitForever);
        if (evt.status == osEventMail) {
            CAN_in_queue_t *mail = (CAN_in_queue_t*)evt.value.p;
            if (mail->message_id == (CMD_BASE_ID + sys_code)) {
                switch (mail->data[0]) {
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

    can1.read(msg);
    if (msg.id == (CMD_BASE_ID + sys_code)) {
        CAN_in_queue_t *CAN_message = CAN_in_mail_box.alloc();
        CAN_message->message_id = msg.id;
        for (int i=0; i<msg.len ; i++) {
            CAN_message->data[i] = msg.data[0];
        }
        CAN_message->message_length = msg.len;
        CAN_in_mail_box.put(CAN_message);
    }
    // re-attach callback for next message
    can1.attach(can_callback, CAN::RxIrq);
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
 * enable CAN id filter on LPC1768 device
 */
void disable_CAN_filter(void)
{
    LPC_CANAF->AFMR = 0x00000001;
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

    AFMR_temp = LPC_CANAF->AFMR & 0x00000001;
    LPC_CANAF->AFMR = 0x00000001;
//
// create 11-bit explicit filter rules.
// Single rule and odd number of rules need special care.
//    
    filter_list_pt = 0;
    ID_table_pt = 0;
    if (nos_standard_explicit > 0) {
        LPC_CANAF->SFF_sa = ID_table_pt << 2;  // convert to bytes
        if (nos_standard_explicit == 1) {
            mask  = ((CAN_filter_list[filter_list_pt].id_1 << 16) | (CAN_controller << 29)) & 0xE7FF0000;
            LPC_CANAF_RAM->mask[ID_table_pt] = mask; 
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
    if (nos_standard_group > 0) {
        LPC_CANAF->SFF_GRP_sa = ID_table_pt << 2; 
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
    if (nos_extended_group > 0) {
        LPC_CANAF->EFF_sa = ID_table_pt << 2;
        for (i=0 ; i < (nos_extended_explicit) ; i++) {
            LPC_CANAF_RAM->mask[ID_table_pt] = (CAN_controller << 29) | CAN_filter_list[filter_list_pt].id_1;
            ID_table_pt++;
            filter_list_pt++;    
        }
    }
//
// create 29-bit group filter rules (each rule uses 2 words of CAN RAM memory)
//
    if (nos_extended_group > 0) {
        LPC_CANAF->EFF_GRP_sa = (ID_table_pt << 2); 
        for (i=0 ; i < (nos_extended_group) ; i=i+2) {
            LPC_CANAF_RAM->mask[ID_table_pt + i]   = (CAN_controller << 29) | CAN_filter_list[filter_list_pt + i].id_1;
            LPC_CANAF_RAM->mask[ID_table_pt + i + 1] = (CAN_controller << 29) | CAN_filter_list[filter_list_pt+ i].id_2;
            filter_list_pt++;
            ID_table_pt += 2;
        } 
        LPC_CANAF->ENDofTable = ID_table_pt << 2;                
    }
//    
    LPC_CANAF->AFMR = AFMR_temp;
}

/**
 * Sort CAN baffer into an ordered format (low id's first)
 *
 * 1. standard 11-bit explicit commands 
 * 2. standard 11-bit group commands
 * 3. extended 29-bit explicit commands
 * 4. extended 29-bit group commands
 *
 * Null at this time.  Assume that set of folter masks are loaded into
 * the buffer in the corect order.
 */
void sort_CAN_buffer(void)
{
    return;
}