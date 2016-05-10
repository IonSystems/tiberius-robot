 /* mbed Library - QEIhw
 * Copyright (c) 2010, hball
 * released under MIT license http://mbed.org/licence/mit
 */
 
/***********************************************************************//**
 * @file        qeihw.h
 * @brief       Header file for the qeihw driver. Adapted from the CMSIS
 *              header, lpc17xx_qei.h, v 2.0
 * @version     0.0
 * @date        10 Dec 2010
 * @author      hb
 **************************************************************************/


#ifndef MBED_QEIHW_H
#define MBED_QEIHW_H

/* Includes ------------------------------------------------------------------- */
#include "mbed.h"


/* Public Types --------------------------------------------------------------- */

/* Flag Status type definition */
typedef enum {RESET = 0, SET = !RESET} FlagStatus, IntStatus, SetState;

/* Functional State Definition */
typedef enum {DISABLE = 0, ENABLE = !DISABLE} FunctionalState;


/* Other definitions    */
#define XTAL_FREQ       12000000

/* Public Functions ----------------------------------------------------------- */
/** @defgroup QEI_Public_Functions QEI Public Functions
*/

/** QEI hardware interface class
* Requires mbed hardware modification: connect
* encoder PhA to p1.20, and PhB to p1.23.
*
* Example:
* @code
* // Display changes in encoder position and direction 
#include "mbed.h"
* #include "qeihw.h"
*
* DigitalOut led1(LED1);
* DigitalOut led3(LED3);
* QEIHW qei(QEI_DIRINV_NONE, QEI_SIGNALMODE_QUAD, QEI_CAPMODE_2X, QEI_INVINX_NONE );
*
* int main() {
*     int32_t temp, position = 0;                      
*     qei.SetDigiFilter(480UL);
*     qei.SetMaxPosition(0xFFFFFFFF);
*    
*     while(1) {
*         while(position == (temp = qei.GetPosition()) );
*         position = temp;  
*         printf("New position = %d.\r\n", temp);
*         led1 = qei.Direction() == SET ? 1 : 0;
*         led3 = !led1;
*         wait(0.1);
*     }
* }
* @endcode
*/

class QEIHW {
public:

    /** Create a QEI object and configure it
     *
     * @param _dirinv Direction invert. When = 1, complements the QEICONF register DIR bit
     * @param _sigmode Signal mode. When = 0, PhA and PhB are quadrature inputs. When = 1, PhA is direction and PhB is clock
     * @param _capmode Capture mode. When = 0, count PhA edges only (2X mode). Whe = 1, count PhB edges also (4X mode).
     * @param _invinx Invert index. When = 1, inverts the sense of the index signal
     */
    QEIHW( uint32_t _dirinv, uint32_t _sigmode, uint32_t _capmode, uint32_t _invinx); 

/**  Resets value for each type of QEI value, such as velocity, position, etc.
 *                 
 * @param[in]    ulResetType        QEI Reset Type, should be one of the following:
 *                                 - QEI_RESET_POS: Reset Position Counter
 *                                 - QEI_RESET_POSOnIDX: Reset Position Counter on Index signal
 *                                 - QEI_RESET_VEL: Reset Velocity
 *                                 - QEI_RESET_IDX: Reset Index Counter
 */
void Reset(uint32_t ulResetType);
       
/** Powers down the QEI block, returns pins to GPIO mode
 *
 */
void DeInit();

/** Report direction (QEISTAT bit DIR)
 *                             
 * @return       State of the DIR bit (SET or RESET)
 */
FlagStatus Direction();

/**
 * @brief        Get current position value in QEI peripheral
 * 
 * @return        Current position value of QEI peripheral
 */
uint32_t GetPosition();

/** Set max position value for QEI peripheral
 *
 * @param[in]    ulMaxPos    Max position value to set
 * @return        None
 */
void SetMaxPosition(uint32_t ulMaxPos);

/** Set position compare value for QEI peripheral
 * @param[in]    bPosCompCh    Compare Position channel, should be:
 *                             - QEI_COMPPOS_CH_0: QEI compare position channel 0
 *                             - QEI_COMPPOS_CH_1: QEI compare position channel 1
 *                             - QEI_COMPPOS_CH_2: QEI compare position channel 2
 * @param[in]    ulPosComp    Compare Position value to set
 * @return        None
 */
void SetPositionComp( uint8_t bPosCompCh, uint32_t ulPosComp);

/** Get current index counter of QEI peripheral
 *
 * @return        Current value of QEI index counter
 */
uint32_t GetIndex();

/** Set value for index compare in QEI peripheral
 * @param[in]    ulIndexComp        Compare Index Value to set
 * @return        None
 */
void SetIndexComp( uint32_t ulIndexComp);

/** Set Velocity timer reload value
 *
 * @param[in]    ulReloadValue    Velocity timer reload count
 * @return        None
 */
void SetVelocityTimerReload( uint32_t ulReloadValue);

/** Set Velocity timer reload value in microseconds
 *
 * @param[in]    ulReloadValue    Velocity timer reload count
 * @return        None
 */
void SetVelocityTimerReload_us( uint32_t ulReloadValue);

/** Get current timer counter in QEI peripheral
 * 
 * @return        Current timer counter in QEI peripheral
 */
uint32_t GetTimer();

/** Get current velocity pulse counter in current time period
 * 
 * @return        Current velocity pulse counter value
 */
uint32_t GetVelocity();

/** Get the most recently measured velocity of the QEI. When
 *                 the Velocity timer in QEI is over-flow, the current velocity
 *                 value will be loaded into Velocity Capture register.
 * 
 * @return        The most recently measured velocity value
 */
uint32_t GetVelocityCap();

/** Set Velocity Compare value for QEI peripheral
 *
 * @param[in]    ulVelComp        Compare Velocity value to set
 * @return        None
 */
void SetVelocityComp( uint32_t ulVelComp);

/** Set value of sampling count for the digital filter in
 *                 QEI peripheral
 * 
 * @param[in]    ulSamplingPulse    Value of sampling count to set
 * @return        None
 */
void SetDigiFilter( uint32_t ulSamplingPulse);

/** Check whether if specified interrupt flag status in QEI
 *                 peripheral is set or not
 * 
 * @param[in]    ulIntType        Interrupt Flag Status type, should be:
                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
                                                        index count interrupt
                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 * @return        New State of specified interrupt flag status (SET or RESET)
 */
FlagStatus GetIntStatus( uint32_t ulIntType);

/** Enable/Disable specified interrupt in QEI peripheral
 * 
 * @param[in]    ulIntType        Interrupt Flag Status type, should be:
 *                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
 *                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
 *                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
 *                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
 *                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
 *                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
 *                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
 *                                                        index count interrupt
 *                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
 *                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
 *                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 * @param[in]    NewState        New function state, should be:
 *                                - DISABLE
 *                                - ENABLE
 * @return        None
 */
void IntCmd( uint32_t ulIntType, FunctionalState NewState);

/** Asserts specified interrupt in QEI peripheral
 * 
 * @param[in]    ulIntType        Interrupt Flag Status type, should be:
                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
                                                        index count interrupt
                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 * @return        None
 */
void IntSet( uint32_t ulIntType);

/** De-asserts specified interrupt (pending) in QEI peripheral
 * 
 * @param[in]    ulIntType        Interrupt Flag Status type, should be:
                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
                                                        current position interrupt
                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
                                                        index count interrupt
                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 * @return        None
 */
void IntClear( uint32_t ulIntType);

/**  Append interrupt handler for specific QEI interrupt source
 *
 * @param[in]    ulISRType        Interrupt Flag Status type, should be:
 *                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
 *                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
 *                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
 *                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
 *                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
 *                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
 *                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
 *                                                        index count interrupt
 *                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
 *                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
 *                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 *                                 
 * @return       none
 */
void AppendISR(uint32_t ulISRType, void(*fptr)(void));

/**  Unappend interrupt handler for specific QEI interrupt source
 * 
 * @param[in]    ulISRType        Interrupt Flag Status type, should be:
 *                                - QEI_INTFLAG_INX_Int: index pulse was detected interrupt
 *                                - QEI_INTFLAG_TIM_Int: Velocity timer over flow interrupt
 *                                - QEI_INTFLAG_VELC_Int: Capture velocity is less than compare interrupt
 *                                - QEI_INTFLAG_DIR_Int: Change of direction interrupt
 *                                - QEI_INTFLAG_ERR_Int: An encoder phase error interrupt
 *                                - QEI_INTFLAG_ENCLK_Int: An encoder clock pulse was detected interrupt
 *                                - QEI_INTFLAG_POS0_Int: position 0 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS1_Int: position 1 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_POS2_Int: position 2 compare value is equal to the
 *                                                        current position interrupt
 *                                - QEI_INTFLAG_REV_Int: Index compare value is equal to the current
 *                                                        index count interrupt
 *                                - QEI_INTFLAG_POS0REV_Int: Combined position 0 and revolution count interrupt
 *                                - QEI_INTFLAG_POS1REV_Int: Combined position 1 and revolution count interrupt
 *                                - QEI_INTFLAG_POS2REV_Int: Combined position 2 and revolution count interrupt
 *                                 
 * @return       none
 */
void UnAppendISR(uint32_t ulISRType);


/**
 * @brief        Calculates the actual velocity in RPM passed via velocity
 *                 capture value and Pulse Per Revolution (of the encoder) value
 *                 parameter input.
 * 
 * @param[in]    ulVelCapValue    Velocity capture input value that can
 *                                 be got from QEI_GetVelocityCap() function
 * @param[in]    ulPPR            Pulse per round of encoder
 * @return        The actual value of velocity in RPM (Revolutions per minute)
 */
uint32_t CalculateRPM( uint32_t ulVelCapValue, uint32_t ulPPR);


/* Public Macros -------------------------------------------------------------- */
/* QEI Reset types */
#define QEI_RESET_POS            QEI_CON_RESP        /**< Reset position counter */
#define QEI_RESET_POSOnIDX        QEI_CON_RESPI        /**< Reset Posistion Counter on Index */
#define QEI_RESET_VEL            QEI_CON_RESV        /**< Reset Velocity */
#define QEI_RESET_IDX            QEI_CON_RESI        /**< Reset Index Counter */

/* QEI Direction Invert Type Option */
#define QEI_DIRINV_NONE        ((uint32_t)(0))        /**< Direction is not inverted */
#define QEI_DIRINV_CMPL        ((uint32_t)(1))        /**< Direction is complemented */

/* QEI Signal Mode Option */
#define QEI_SIGNALMODE_QUAD        ((uint32_t)(0))        /**< Signal operation: Quadrature phase mode */
#define QEI_SIGNALMODE_CLKDIR    ((uint32_t)(1))        /**< Signal operation: Clock/Direction mode */

/* QEI Capture Mode Option */
#define QEI_CAPMODE_2X            ((uint32_t)(0))        /**< Capture mode: Only Phase-A edges are counted (2X) */
#define QEI_CAPMODE_4X            ((uint32_t)(1))        /**< Capture mode: BOTH PhA and PhB edges are counted (4X)*/

/* QEI Invert Index Signal Option */
#define QEI_INVINX_NONE            ((uint32_t)(0))        /**< Invert Index signal option: None */
#define QEI_INVINX_EN            ((uint32_t)(1))        /**< Invert Index signal option: Enable */

/* QEI timer reload option */
#define QEI_TIMERRELOAD_TICKVAL    ((uint8_t)(0))    /**< Reload value in absolute value */
#define QEI_TIMERRELOAD_USVAL    ((uint8_t)(1))    /**< Reload value in microsecond value */

/* QEI Flag Status type */
#define QEI_STATUS_DIR            ((uint32_t)(1<<0))    /**< Direction status */

/* QEI Compare Position channel option */
#define QEI_COMPPOS_CH_0            ((uint8_t)(0))        /**< QEI compare position channel 0 */
#define QEI_COMPPOS_CH_1            ((uint8_t)(1))        /**< QEI compare position channel 1 */
#define QEI_COMPPOS_CH_2            ((uint8_t)(2))        /**< QEI compare position channel 2 */

/* QEI interrupt flag type */
#define QEI_INTFLAG_INX_Int            ((uint32_t)(1<<0))    /**< index pulse was detected interrupt */
#define QEI_INTFLAG_TIM_Int            ((uint32_t)(1<<1))    /**< Velocity timer over flow interrupt */
#define QEI_INTFLAG_VELC_Int        ((uint32_t)(1<<2))    /**< Capture velocity is less than compare interrupt */
#define QEI_INTFLAG_DIR_Int            ((uint32_t)(1<<3))    /**< Change of direction interrupt */
#define QEI_INTFLAG_ERR_Int            ((uint32_t)(1<<4))    /**< An encoder phase error interrupt */
#define QEI_INTFLAG_ENCLK_Int        ((uint32_t)(1<<5))    /**< An encoder clock pulse was detected interrupt */
#define QEI_INTFLAG_POS0_Int        ((uint32_t)(1<<6))    /**< position 0 compare value is equal to the
                                                        current position interrupt */
#define QEI_INTFLAG_POS1_Int        ((uint32_t)(1<<7))    /**< position 1 compare value is equal to the
                                                        current position interrupt */
#define QEI_INTFLAG_POS2_Int        ((uint32_t)(1<<8))    /**< position 2 compare value is equal to the
                                                        current position interrupt */
#define QEI_INTFLAG_REV_Int            ((uint32_t)(1<<9))    /**< Index compare value is equal to the current
                                                        index count interrupt */
#define QEI_INTFLAG_POS0REV_Int        ((uint32_t)(1<<10))    /**< Combined position 0 and revolution count interrupt */
#define QEI_INTFLAG_POS1REV_Int        ((uint32_t)(1<<11))    /**< Combined position 1 and revolution count interrupt */
#define QEI_INTFLAG_POS2REV_Int        ((uint32_t)(1<<12))    /**< Combined position 2 and revolution count interrupt */

/* QEI Process position reporting options */
#define QEI_PROCESS_OPERATE            0;
#define QEI_PROCESS_RESET              1;
#define QEI_PROCESS_INCREMENTAL        0;
#define QEI_PROCESS_ACCUMULATE         1;
#define QEI_PROCESS_LINEAR             0;
#define QEI_PROCESS_WEIGHTED           1;

private:
static void _Qeiisr(void);
void Qeiisr(void);  
static QEIHW *instance;

void(*_qei_isr[13])();


/* Private Macros ------------------------------------------------------------- */
/* --------------------- BIT DEFINITIONS -------------------------------------- */
/* Quadrature Encoder Interface Control Register Definition --------------------- */
/*********************************************************************//**
 * Macro defines for QEI Control register
 **********************************************************************/
#define QEI_CON_RESP        ((uint32_t)(1<<0))        /**< Reset position counter */
#define QEI_CON_RESPI        ((uint32_t)(1<<1))        /**< Reset Posistion Counter on Index */
#define QEI_CON_RESV        ((uint32_t)(1<<2))        /**< Reset Velocity */
#define QEI_CON_RESI        ((uint32_t)(1<<3))        /**< Reset Index Counter */
#define QEI_CON_BITMASK        ((uint32_t)(0x0F))        /**< QEI Control register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Configuration register
 **********************************************************************/
#define QEI_CONF_DIRINV        ((uint32_t)(1<<0))        /**< Direction Invert */
#define QEI_CONF_SIGMODE    ((uint32_t)(1<<1))        /**< Signal mode */
#define QEI_CONF_CAPMODE    ((uint32_t)(1<<2))        /**< Capture mode */
#define QEI_CONF_INVINX        ((uint32_t)(1<<3))        /**< Invert index */
#define QEI_CONF_BITMASK    ((uint32_t)(0x0F))        /**< QEI Configuration register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Status register
 **********************************************************************/
#define QEI_STAT_DIR        ((uint32_t)(1<<0))        /**< Direction bit */
#define QEI_STAT_BITMASK    ((uint32_t)(1<<0))        /**< QEI status register bit-mask */

/* Quadrature Encoder Interface Interrupt registers definitions --------------------- */
/*********************************************************************//**
 * Macro defines for QEI Interrupt Status register
 **********************************************************************/
#define QEI_INTSTAT_INX_Int            ((uint32_t)(1<<0))    /**< Indicates that an index pulse was detected */
#define QEI_INTSTAT_TIM_Int            ((uint32_t)(1<<1))    /**< Indicates that a velocity timer overflow occurred */
#define QEI_INTSTAT_VELC_Int        ((uint32_t)(1<<2))    /**< Indicates that capture velocity is less than compare velocity */
#define QEI_INTSTAT_DIR_Int            ((uint32_t)(1<<3))    /**< Indicates that a change of direction was detected */
#define QEI_INTSTAT_ERR_Int            ((uint32_t)(1<<4))    /**< Indicates that an encoder phase error was detected */
#define QEI_INTSTAT_ENCLK_Int        ((uint32_t)(1<<5))    /**< Indicates that and encoder clock pulse was detected */
#define QEI_INTSTAT_POS0_Int        ((uint32_t)(1<<6))    /**< Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_INTSTAT_POS1_Int        ((uint32_t)(1<<7))    /**< Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_INTSTAT_POS2_Int        ((uint32_t)(1<<8))    /**< Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_INTSTAT_REV_Int            ((uint32_t)(1<<9))    /**< Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_INTSTAT_POS0REV_Int        ((uint32_t)(1<<10))    /**< Combined position 0 and revolution count interrupt. Set when
                                                        both the POS0_Int bit is set and the REV_Int is set */
#define QEI_INTSTAT_POS1REV_Int        ((uint32_t)(1<<11))    /**< Combined position 1 and revolution count interrupt. Set when
                                                        both the POS1_Int bit is set and the REV_Int is set */
#define QEI_INTSTAT_POS2REV_Int        ((uint32_t)(1<<12))    /**< Combined position 2 and revolution count interrupt. Set when
                                                        both the POS2_Int bit is set and the REV_Int is set */
#define QEI_INTSTAT_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Status register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Interrupt Set register
 **********************************************************************/
#define QEI_INTSET_INX_Int            ((uint32_t)(1<<0))    /**< Set Bit Indicates that an index pulse was detected */
#define QEI_INTSET_TIM_Int            ((uint32_t)(1<<1))    /**< Set Bit Indicates that a velocity timer overflow occurred */
#define QEI_INTSET_VELC_Int            ((uint32_t)(1<<2))    /**< Set Bit Indicates that capture velocity is less than compare velocity */
#define QEI_INTSET_DIR_Int            ((uint32_t)(1<<3))    /**< Set Bit Indicates that a change of direction was detected */
#define QEI_INTSET_ERR_Int            ((uint32_t)(1<<4))    /**< Set Bit Indicates that an encoder phase error was detected */
#define QEI_INTSET_ENCLK_Int        ((uint32_t)(1<<5))    /**< Set Bit Indicates that and encoder clock pulse was detected */
#define QEI_INTSET_POS0_Int            ((uint32_t)(1<<6))    /**< Set Bit Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_INTSET_POS1_Int            ((uint32_t)(1<<7))    /**< Set Bit Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_INTSET_POS2_Int            ((uint32_t)(1<<8))    /**< Set Bit Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_INTSET_REV_Int            ((uint32_t)(1<<9))    /**< Set Bit Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_INTSET_POS0REV_Int        ((uint32_t)(1<<10))    /**< Set Bit that combined position 0 and revolution count interrupt */
#define QEI_INTSET_POS1REV_Int        ((uint32_t)(1<<11))    /**< Set Bit that Combined position 1 and revolution count interrupt */
#define QEI_INTSET_POS2REV_Int        ((uint32_t)(1<<12))    /**< Set Bit that Combined position 2 and revolution count interrupt */
#define QEI_INTSET_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Set register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Interrupt Clear register
 **********************************************************************/
#define QEI_INTCLR_INX_Int            ((uint32_t)(1<<0))    /**< Clear Bit Indicates that an index pulse was detected */
#define QEI_INTCLR_TIM_Int            ((uint32_t)(1<<1))    /**< Clear Bit Indicates that a velocity timer overflow occurred */
#define QEI_INTCLR_VELC_Int            ((uint32_t)(1<<2))    /**< Clear Bit Indicates that capture velocity is less than compare velocity */
#define QEI_INTCLR_DIR_Int            ((uint32_t)(1<<3))    /**< Clear Bit Indicates that a change of direction was detected */
#define QEI_INTCLR_ERR_Int            ((uint32_t)(1<<4))    /**< Clear Bit Indicates that an encoder phase error was detected */
#define QEI_INTCLR_ENCLK_Int        ((uint32_t)(1<<5))    /**< Clear Bit Indicates that and encoder clock pulse was detected */
#define QEI_INTCLR_POS0_Int            ((uint32_t)(1<<6))    /**< Clear Bit Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_INTCLR_POS1_Int            ((uint32_t)(1<<7))    /**< Clear Bit Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_INTCLR_POS2_Int            ((uint32_t)(1<<8))    /**< Clear Bit Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_INTCLR_REV_Int            ((uint32_t)(1<<9))    /**< Clear Bit Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_INTCLR_POS0REV_Int        ((uint32_t)(1<<10))    /**< Clear Bit that combined position 0 and revolution count interrupt */
#define QEI_INTCLR_POS1REV_Int        ((uint32_t)(1<<11))    /**< Clear Bit that Combined position 1 and revolution count interrupt */
#define QEI_INTCLR_POS2REV_Int        ((uint32_t)(1<<12))    /**< Clear Bit that Combined position 2 and revolution count interrupt */
#define QEI_INTCLR_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Clear register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Interrupt Enable register
 **********************************************************************/
#define QEI_INTEN_INX_Int            ((uint32_t)(1<<0))    /**< Enabled Interrupt Bit Indicates that an index pulse was detected */
#define QEI_INTEN_TIM_Int            ((uint32_t)(1<<1))    /**< Enabled Interrupt Bit Indicates that a velocity timer overflow occurred */
#define QEI_INTEN_VELC_Int            ((uint32_t)(1<<2))    /**< Enabled Interrupt Bit Indicates that capture velocity is less than compare velocity */
#define QEI_INTEN_DIR_Int            ((uint32_t)(1<<3))    /**< Enabled Interrupt Bit Indicates that a change of direction was detected */
#define QEI_INTEN_ERR_Int            ((uint32_t)(1<<4))    /**< Enabled Interrupt Bit Indicates that an encoder phase error was detected */
#define QEI_INTEN_ENCLK_Int            ((uint32_t)(1<<5))    /**< Enabled Interrupt Bit Indicates that and encoder clock pulse was detected */
#define QEI_INTEN_POS0_Int            ((uint32_t)(1<<6))    /**< Enabled Interrupt Bit Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_INTEN_POS1_Int            ((uint32_t)(1<<7))    /**< Enabled Interrupt Bit Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_INTEN_POS2_Int            ((uint32_t)(1<<8))    /**< Enabled Interrupt Bit Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_INTEN_REV_Int            ((uint32_t)(1<<9))    /**< Enabled Interrupt Bit Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_INTEN_POS0REV_Int        ((uint32_t)(1<<10))    /**< Enabled Interrupt Bit that combined position 0 and revolution count interrupt */
#define QEI_INTEN_POS1REV_Int        ((uint32_t)(1<<11))    /**< Enabled Interrupt Bit that Combined position 1 and revolution count interrupt */
#define QEI_INTEN_POS2REV_Int        ((uint32_t)(1<<12))    /**< Enabled Interrupt Bit that Combined position 2 and revolution count interrupt */
#define QEI_INTEN_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Enable register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Interrupt Enable Set register
 **********************************************************************/
#define QEI_IESET_INX_Int            ((uint32_t)(1<<0))    /**< Set Enable Interrupt Bit Indicates that an index pulse was detected */
#define QEI_IESET_TIM_Int            ((uint32_t)(1<<1))    /**< Set Enable Interrupt Bit Indicates that a velocity timer overflow occurred */
#define QEI_IESET_VELC_Int            ((uint32_t)(1<<2))    /**< Set Enable Interrupt Bit Indicates that capture velocity is less than compare velocity */
#define QEI_IESET_DIR_Int            ((uint32_t)(1<<3))    /**< Set Enable Interrupt Bit Indicates that a change of direction was detected */
#define QEI_IESET_ERR_Int            ((uint32_t)(1<<4))    /**< Set Enable Interrupt Bit Indicates that an encoder phase error was detected */
#define QEI_IESET_ENCLK_Int            ((uint32_t)(1<<5))    /**< Set Enable Interrupt Bit Indicates that and encoder clock pulse was detected */
#define QEI_IESET_POS0_Int            ((uint32_t)(1<<6))    /**< Set Enable Interrupt Bit Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_IESET_POS1_Int            ((uint32_t)(1<<7))    /**< Set Enable Interrupt Bit Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_IESET_POS2_Int            ((uint32_t)(1<<8))    /**< Set Enable Interrupt Bit Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_IESET_REV_Int            ((uint32_t)(1<<9))    /**< Set Enable Interrupt Bit Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_IESET_POS0REV_Int        ((uint32_t)(1<<10))    /**< Set Enable Interrupt Bit that combined position 0 and revolution count interrupt */
#define QEI_IESET_POS1REV_Int        ((uint32_t)(1<<11))    /**< Set Enable Interrupt Bit that Combined position 1 and revolution count interrupt */
#define QEI_IESET_POS2REV_Int        ((uint32_t)(1<<12))    /**< Set Enable Interrupt Bit that Combined position 2 and revolution count interrupt */
#define QEI_IESET_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Enable Set register bit-mask */

/*********************************************************************//**
 * Macro defines for QEI Interrupt Enable Clear register
 **********************************************************************/
#define QEI_IECLR_INX_Int            ((uint32_t)(1<<0))    /**< Clear Enabled Interrupt Bit Indicates that an index pulse was detected */
#define QEI_IECLR_TIM_Int            ((uint32_t)(1<<1))    /**< Clear Enabled Interrupt Bit Indicates that a velocity timer overflow occurred */
#define QEI_IECLR_VELC_Int            ((uint32_t)(1<<2))    /**< Clear Enabled Interrupt Bit Indicates that capture velocity is less than compare velocity */
#define QEI_IECLR_DIR_Int            ((uint32_t)(1<<3))    /**< Clear Enabled Interrupt Bit Indicates that a change of direction was detected */
#define QEI_IECLR_ERR_Int            ((uint32_t)(1<<4))    /**< Clear Enabled Interrupt Bit Indicates that an encoder phase error was detected */
#define QEI_IECLR_ENCLK_Int            ((uint32_t)(1<<5))    /**< Clear Enabled Interrupt Bit Indicates that and encoder clock pulse was detected */
#define QEI_IECLR_POS0_Int            ((uint32_t)(1<<6))    /**< Clear Enabled Interrupt Bit Indicates that the position 0 compare value is equal to the
                                                        current position */
#define QEI_IECLR_POS1_Int            ((uint32_t)(1<<7))    /**< Clear Enabled Interrupt Bit Indicates that the position 1compare value is equal to the
                                                        current position */
#define QEI_IECLR_POS2_Int            ((uint32_t)(1<<8))    /**< Clear Enabled Interrupt Bit Indicates that the position 2 compare value is equal to the
                                                        current position */
#define QEI_IECLR_REV_Int            ((uint32_t)(1<<9))    /**< Clear Enabled Interrupt Bit Indicates that the index compare value is equal to the current
                                                        index count */
#define QEI_IECLR_POS0REV_Int        ((uint32_t)(1<<10))    /**< Clear Enabled Interrupt Bit that combined position 0 and revolution count interrupt */
#define QEI_IECLR_POS1REV_Int        ((uint32_t)(1<<11))    /**< Clear Enabled Interrupt Bit that Combined position 1 and revolution count interrupt */
#define QEI_IECLR_POS2REV_Int        ((uint32_t)(1<<12))    /**< Clear Enabled Interrupt Bit that Combined position 2 and revolution count interrupt */
#define QEI_IECLR_BITMASK            ((uint32_t)(0x1FFF))    /**< QEI Interrupt Enable Clear register bit-mask */

/*********************************************************************//**
 * Macro defines for PCONP register QEI-related bits
 **********************************************************************/
#define PCONP_QEI_ENABLE             ((uint32_t)(1<<18))     /**< QEI peripheral power enable bit */
#define PCONP_QEI_DISABLE            ~((uint32_t)(1<<18))     /**< QEI peripheral power disable bit-mask */

/*********************************************************************//**
 * Macro defines for PCLKSELx register QEI-related bits
 **********************************************************************/
#define PCLKSEL_CCLK_DIV_1              1UL                 /**< Set PCLK to CCLK/1 */
#define PCLKSEL_CCLK_DIV_2              2UL                 /**< Set PCLK to CCLK/2 */
#define PCLKSEL_CCLK_DIV_4              0UL                 /**< Set PCLK to CCLK/4 */
#define PCLKSEL_CCLK_DIV_8              3UL                 /**< Set PCLK to CCLK/8 */
#define PCLKSEL1_PCLK_QEI_MASK          ((uint32_t)(3<<0))  /**< PCLK_QEI PCLK_QEI bit field mask */
/*********************************************************************//**
 * Macro defines for PINSEL3 register QEI-related bits
 **********************************************************************/
#define PINSEL3_MCI0                ((uint32_t)(1<<8))     /**< MCIO (PhA) pin select */
#define PINSEL3_MCI0_MASK          ~((uint32_t)(3<<8))     /**< MCIO (PhA) pin mask */
#define PINSEL3_MCI1                ((uint32_t)(1<<14))    /**< MCI1 (PhB) pin select */
#define PINSEL3_MCI1_MASK          ~((uint32_t)(3<<14))    /**< MCI2 (PhB) pin mask */
#define PINSEL3_MCI2                ((uint32_t)(1<<16))    /**< MCI2 (Index) pin select */
#define PINSEL3_MCI2_MASK          ~((uint32_t)(3<<16))    /**< MCI2 (Index) pin mask */

/*********************************************************************//**
 * Macro defines for PINMODE3 register QEI-related bits
 **********************************************************************/
#define PIN_PULL_UP                     0UL
#define PIN_REPEATER                    1UL
#define PIN_NORESISTOR                  2UL
#define PIN_PULL_DOWN                   3UL     

#define PINMODE3_MCI0                ((uint32_t)(PIN_NORESISTOR<<8))     /**< MCIO (PhA) resistor selection */
#define PINMODE3_GPIO1p20            ((uint32_t)(PIN_PULL_DOWN<<8))      /**< GPIO 1.20) resistor selection */
#define PINMODE3_MCI0_MASK          ~((uint32_t)(3<<8))                  /**< MCIO (PhA) resistor mask */

#define PINMODE3_MCI1                ((uint32_t)(PIN_NORESISTOR<<14))    /**< MCI1 (PhB) resistor selection */
#define PINMODE3_GPIO1p23            ((uint32_t)(PIN_PULL_DOWN<<14))      /**< GPIO 1.23) resistor selection */
#define PINMODE3_MCI1_MASK          ~((uint32_t)(3<<14))                 /**< MCI1 (PhB) resistor mask */

#define PINMODE3_MCI2                ((uint32_t)(PIN_PULL_UP<<16))       /**< MCI2 (Index) resistor selection */
#define PINMODE3_GPIO1p24            ((uint32_t)(PIN_PULL_DOWN<<16))      /**< GPIO 1.24) resistor selection */
#define PINMODE3_MCI2_MASK          ~((uint32_t)(3<<16))                 /**< MCI2 (Index) resistor mask */

};


#endif /* MBED_QEI_H */
/* --------------------------------- End Of File ------------------------------ */
