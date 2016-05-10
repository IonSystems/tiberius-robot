/*
 */
#include "mbed.h"
#include "cmsis_os.h"

#ifndef  CAN_IO_H
#define  CAN_IO_H

#define     CAN_CONTROLLER_0         0
#define     CAN_CONTROLLER_1         1
#define     MAX_CAN_FILTER_ENTRIES  20

typedef enum {EXPLICIT_11_BIT, 
              GROUP_11_BIT, 
              EXPLICIT_29_BIT, 
              GROUP_29_BIT, 
              CLEAR, 
            } CAN_filter_type_t;
                
typedef enum {UNALLOCATED, ALLOCATED}   item_state_t;

//
// Structure to hold CAN filter commands
//
struct CAN_filter_item {
    uint8_t     filter_type;
    uint8_t     state;
    uint32_t    id_1;
    uint32_t    id_2;
};

//*******************************************
// Function templates
//
void     CAN_out_speed(float measured_speed, uint32_t sequence_number);
void     can_callback();
int32_t  set_CAN_controller(uint32_t  controller);
void     init_can_filter_buffer(void);
int32_t  add_can_filter_id(uint32_t id, uint8_t mode);
int32_t  add_can_filter_group(uint16_t low_id, uint16_t high_id, uint8_t mode);
void     enable_CAN_filter(void);
void     disable_CAN_filter(void);
void     load_CAN_filter_memory(void);
void     sort_CAN_buffer(void);

#endif