 /* mbed Library - QEI driver for LP1768 hardware
 * Copyright (c) 2010, hball
 * released under MIT license http://mbed.org/licence/mit
 */
 
/***********************************************************************//**
 * @file        qeihw.cpp
 * @brief       Driver file for the QEI hardware. Requires connection to
 *              internal mbed circuit nodes. Adapted from the CMSIS
 *              driver, lpc17xx_qei.c, v 2.0
 * @version     0.1
 * @date        28 Dec 2010
 * @author      hb
 **************************************************************************/
#include "mbed.h"
#include "qeihw.h"

QEIHW *QEIHW::instance;

/*********************************************************************//**
 * @brief        Create a QEI object and configure it.
 * @param _dirinv Direction invert. When = 1, complements the QEICONF register DIR bit
 * @param _sigmode Signal mode. When = 0, PhA and PhB are quadrature inputs. When = 1, PhA is direction and PhB is clock
 * @param _capmode Capture mode. When = 0, count PhA edges only (2X mode). Whe = 1, count PhB edges also (4X mode).
 * @param _invinx Invert index. When = 1, inverts the sense of the index signal
 * @return        None
 **********************************************************************/
QEIHW::QEIHW(uint32_t _dirinv, uint32_t _sigmode, uint32_t _capmode, uint32_t _invinx)
{
    /* Set up clock and power for QEI module */
    LPC_SC->PCONP |= PCONP_QEI_ENABLE;

    /* The clock for theQEI module is set to FCCLK  */
    LPC_SC->PCLKSEL1 = LPC_SC->PCLKSEL1 & ~(3UL<<0) | ((PCLKSEL_CCLK_DIV_1 & 3)<<0); 

    /* Assign the pins. They are hard-coded, not user-selected. The index
     * pin is assigned, even though it is not easily accessed on the mbed.
     * As it may be unconnected, it is given a pull-up resistor to minimize
     * power drain.
     */
    // MCI0 (PhA)
    LPC_PINCON->PINSEL3 = (LPC_PINCON->PINSEL3 & PINSEL3_MCI0_MASK) | PINSEL3_MCI0 ;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI0_MASK) | PINMODE3_MCI0;

    // MCI1 (PhB)
    LPC_PINCON->PINSEL3 = (LPC_PINCON->PINSEL3 & PINSEL3_MCI1_MASK) | PINSEL3_MCI1 ;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI1_MASK) | PINMODE3_MCI1;

    // MCI2 (Index)
    LPC_PINCON->PINSEL3 = (LPC_PINCON->PINSEL3 & PINSEL3_MCI2_MASK) | PINSEL3_MCI2 ;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI2_MASK) | PINMODE3_MCI2;
    
    // Initialize all remaining values in QEI peripheral
    LPC_QEI->QEICON = QEI_CON_RESP | QEI_CON_RESV | QEI_CON_RESI;
    LPC_QEI->QEIMAXPOS = 0xFFFFFFFF;                          // Default value
    LPC_QEI->CMPOS0 = 0x00;
    LPC_QEI->CMPOS1 = 0x00;
    LPC_QEI->CMPOS2 = 0x00;
    LPC_QEI->INXCMP = 0x00;
    LPC_QEI->QEILOAD = 0x00;
    LPC_QEI->VELCOMP = 0x00;
    LPC_QEI->FILTER = 200000;       // Default for mechanical switches.

    // Set QEI configuration value corresponding to the call parameters
    LPC_QEI->QEICONF = (
        ((_dirinv << 0) & 1) | \
        ((_sigmode << 1) & 2) | \
        ((_capmode << 2) & 4) | \
        ((_invinx <<3) & 8) );
       
    // Mask all int sources   
    LPC_QEI->QEIIEC = QEI_IECLR_BITMASK;    // Set the "clear" bits for all sources in the IE clear register              

    // Clear any pending ints    
    LPC_QEI->QEICLR = QEI_INTCLR_BITMASK;   // Set the "clear" bits for for all sources in the Interrupt clear register             
    
    /* preemption = 1, sub-priority = 1 */
    NVIC_SetPriority(QEI_IRQn, ((0x01<<3)|0x01));

    //* Attach IRQ
    instance = this;
    NVIC_SetVector(QEI_IRQn, (uint32_t)&_Qeiisr);

    /* Enable interrupt for QEI  */
    NVIC_EnableIRQ(QEI_IRQn);                       
  
}

/*********************************************************************//**
 * @brief        Resets value for each type of QEI value, such as velocity,
 *                 counter, position, etc..
 * @param[in]    ulResetType        QEI Reset Type, should be one of the following:
 *                                 - QEI_RESET_POS: Reset Position Counter
 *                                 - QEI_RESET_POSOnIDX: Reset Position Counter on Index signal
 *                                 - QEI_RESET_VEL: Reset Velocity
 *                                 - QEI_RESET_IDX: Reset Index Counter
 * @return        None
 **********************************************************************/
void QEIHW::Reset(uint32_t ulResetType)
{
    LPC_QEI->QEICON = ulResetType;
}

/*********************************************************************//**
 * @brief        De-initializes the QEI peripheral registers to their
 *                  default reset values.
 *
 * @return         None
 **********************************************************************/
void QEIHW::DeInit()
{
    /* Turn off clock and power for QEI module */
    LPC_SC->PCONP &= PCONP_QEI_DISABLE;

    /* Return pins to their default assignment (PINSEL = 0, PINMODE = PULLDOWN) */
    // MCI0 (PhA) -> LED-2 (p1.20)
    LPC_PINCON->PINSEL3 &= PINSEL3_MCI0_MASK;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI0_MASK) | PINMODE3_GPIO1p20;

    // MCI1 (PhB) -> LED-4 (p1.23)
    LPC_PINCON->PINSEL3 &= PINSEL3_MCI1_MASK;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI1_MASK) | PINMODE3_GPIO1p23;

    // MCI2 (Index) -> p1.24
    LPC_PINCON->PINSEL3 &= PINSEL3_MCI2_MASK;
    LPC_PINCON->PINMODE3 = (LPC_PINCON->PINMODE3 & PINMODE3_MCI2_MASK) | PINMODE3_GPIO1p24;
}

/*********************************************************************//**
 * @brief        Report direction (QEISTAT bit DIR)
 *                             
 * @return       State of the DIR bit (SET or RESET)
 **********************************************************************/
FlagStatus QEIHW::Direction()
{
    return ((LPC_QEI->QEISTAT & QEI_STATUS_DIR) ? SET : RESET);
}

/*********************************************************************//**
 * @brief        Get current position value in QEI peripheral
 * 
 * @return        Current position value of QEI peripheral
 **********************************************************************/
uint32_t QEIHW::GetPosition()
{
    return (LPC_QEI->QEIPOS);
}

/*********************************************************************//**
 * @brief        Set max position value for QEI peripheral
 *
 * @param[in]    ulMaxPos    Max position value to set
 * @return        None
 **********************************************************************/
void QEIHW::SetMaxPosition(uint32_t ulMaxPos)
{
    LPC_QEI->QEIMAXPOS = ulMaxPos;
}

/*********************************************************************//**
 * @brief        Set position compare value for QEI peripheral
 * @param[in]    QEIx        QEI peripheral, should be LPC_QEI
 * @param[in]    bPosCompCh    Compare Position channel, should be:
 *                             - QEI_COMPPOS_CH_0: QEI compare position channel 0
 *                             - QEI_COMPPOS_CH_1: QEI compare position channel 1
 *                             - QEI_COMPPOS_CH_2: QEI compare position channel 2
 * @param[in]    ulPosComp    Compare Position value to set
 * @return        None
 **********************************************************************/
void QEIHW::SetPositionComp( uint8_t bPosCompCh, uint32_t ulPosComp)
{
    uint32_t *tmp;

    tmp = (uint32_t *) (&(LPC_QEI->CMPOS0) + bPosCompCh * 4);
    *tmp = ulPosComp;
}

/*********************************************************************//**
 * @brief        Get current index counter of QEI peripheral
 *
 * @return        Current value of QEI index counter
 **********************************************************************/
uint32_t QEIHW::GetIndex()
{
    return (LPC_QEI->INXCNT);
}

/*********************************************************************//**
 * @brief        Set value for index compare in QEI peripheral
 * @param[in]    ulIndexComp        Compare Index Value to set
 * @return        None
 **********************************************************************/
void QEIHW::SetIndexComp( uint32_t ulIndexComp)
{
    LPC_QEI->INXCMP = ulIndexComp;
}

/*********************************************************************//**
 * @brief        Set Velocity timer reload value
 *
 * @param[in]    ulReloadValue    Velocity timer reload count
 * @return        None
 **********************************************************************/
void QEIHW::SetVelocityTimerReload( uint32_t ulReloadValue)
{   
         LPC_QEI->QEILOAD = ulReloadValue;
}

/*********************************************************************//**
 * @brief        Set Velocity timer reload value in microseconds
 *
 * @param[in]    ulReloadValue    Velocity timer reload count
 * @return        None
 **********************************************************************/
void QEIHW::SetVelocityTimerReload_us( uint32_t ulReloadValue)
{
    int div;

    //Work out CCLK
    uint32_t m = (LPC_SC->PLL0CFG & 0xFFFF) + 1;
    uint32_t n = (LPC_SC->PLL0CFG >> 16) + 1;
    uint32_t cclkdiv = LPC_SC->CCLKCFG + 1;
    uint32_t Fcco = (2 * m * XTAL_FREQ) / n;
    uint32_t cclk = Fcco / cclkdiv;
    

    
//    div = CLKPWR_GetPCLKSEL(ClkType);
    div = LPC_SC->PCLKSEL1 & PCLKSEL1_PCLK_QEI_MASK;
    switch (div)
    {
    case 0:
        div = 4;
        break;

    case 1:
        div = 1;
        break;

    case 2:
        div = 2;
        break;

    case 3:
        div = 8;
        break;
    }
    cclk /=div;
    cclk =((uint64_t)cclk / (1000000/ulReloadValue)) - 1;
    LPC_QEI->QEILOAD = (uint32_t) cclk;
}

/*********************************************************************//**
 * @brief        Get current timer counter in QEI peripheral
 * 
 * @return        Current timer counter in QEI peripheral
 **********************************************************************/
uint32_t QEIHW::GetTimer()
{
    return (LPC_QEI->QEITIME);
}

/*********************************************************************//**
 * @brief        Get current velocity pulse counter in current time period
 * 
 * @return        Current velocity pulse counter value
 **********************************************************************/
uint32_t QEIHW::GetVelocity()
{
    return (LPC_QEI->QEIVEL);
}

/*********************************************************************//**
 * @brief        Get the most recently captured velocity of the QEI. When
 *                 the Velocity timer in QEI is over-flow, the current velocity
 *                 value will be loaded into Velocity Capture register.
 * 
 * @return        The most recently measured velocity value
 **********************************************************************/
uint32_t QEIHW::GetVelocityCap()
{
    return (LPC_QEI->QEICAP);
}

/*********************************************************************//**
 * @brief        Set Velocity Compare value for QEI peripheral
 *
 * @param[in]    ulVelComp        Compare Velocity value to set
 * @return        None
 **********************************************************************/
void QEIHW::SetVelocityComp( uint32_t ulVelComp)
{
    LPC_QEI->VELCOMP = ulVelComp;
}

/*********************************************************************//**
 * @brief        Set value of sampling count for the digital filter in
 *                 QEI peripheral
 * 
 * @param[in]    ulSamplingPulse    Value of sampling count to set
 * @return        None
 **********************************************************************/
void QEIHW::SetDigiFilter( uint32_t ulSamplingPulse)
{
    LPC_QEI->FILTER = ulSamplingPulse;
}

/*********************************************************************//**
 * @brief        Check whether if specified interrupt flag status in QEI
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
 **********************************************************************/
FlagStatus QEIHW::GetIntStatus( uint32_t ulIntType)
{
    return((LPC_QEI->QEIINTSTAT & ulIntType) ? SET : RESET);
}

/*********************************************************************//**
 * @brief        Enable/Disable specified interrupt in QEI peripheral
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
 **********************************************************************/
void QEIHW::IntCmd( uint32_t ulIntType, FunctionalState NewState)
{
    if (NewState == ENABLE) {
        LPC_QEI->QEIIES = ulIntType;
    } else {
        LPC_QEI->QEIIEC = ulIntType;
    }
}

/*********************************************************************//**
 * @brief       Assert specified interrupt in QEI peripheral
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
 **********************************************************************/
void QEIHW::IntSet( uint32_t ulIntType)
{
    LPC_QEI->QEISET = ulIntType;
}

/*********************************************************************//**
 * @brief       De-assert specified interrupt (pending) in QEI peripheral
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
 **********************************************************************/
void QEIHW::IntClear( uint32_t ulIntType)
{
    LPC_QEI->QEICLR = ulIntType;
}

/*********************************************************************//**
 * @brief        Calculates the actual velocity in RPM passed via velocity
 *                 capture value and Pulse Per Revolution (of the encoder) value
 *                 parameter input.
 * 
 * @param[in]    ulVelCapValue    Velocity capture input value that can
 *                                 be got from QEI_GetVelocityCap() function
 * @param[in]    ulPPR            Pulse per round of encoder
 * @return        The actual value of velocity in RPM (Revolutions per minute)
 **********************************************************************/
uint32_t QEIHW::CalculateRPM( uint32_t ulVelCapValue, uint32_t ulPPR)
{
    uint64_t rpm, Load, edges;
    int div;
    
    // Get current Clock rate for timer input
    //Work out CCLK
    uint32_t m = (LPC_SC->PLL0CFG & 0xFFFF) + 1;
    uint32_t n = (LPC_SC->PLL0CFG >> 16) + 1;
    uint32_t cclkdiv = LPC_SC->CCLKCFG + 1;
    uint32_t Fcco = (2 * m * XTAL_FREQ) / n;
    uint32_t cclk = Fcco / cclkdiv;
    
//    div = CLKPWR_GetPCLKSEL(ClkType);
    div = LPC_SC->PCLKSEL1 & PCLKSEL1_PCLK_QEI_MASK;
    switch (div)
    {
    case 0:
        div = 4;
        break;

    case 1:
        div = 1;
        break;

    case 2:
        div = 2;
        break;

    case 3:
        div = 8;
        break;
    }
    cclk /= div;
    
    // Get Timer load value (velocity capture period)
    Load  = (uint64_t)(LPC_QEI->QEILOAD + 1);
    // Get Edge
    edges = (uint64_t)((LPC_QEI->QEICONF & QEI_CONF_CAPMODE) ? 4 : 2);
    // Calculate RPM
    rpm = ((( uint64_t)cclk * ulVelCapValue * 60) / (Load * ulPPR * edges));

    return (uint32_t)(rpm);
}

/*********************************************************************//**
 * @brief        Append interrupt handler for specific QEI interrupt source
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
 **********************************************************************/
void QEIHW::AppendISR(uint32_t ulISRType, void(*fptr)(void)) {
    int i;
    
    for(i = 0; i < 13; i++) {
        if( ulISRType == (1UL << i) ) {
            _qei_isr[i] = fptr;
            break;
        }
    }
    return;
}

/*********************************************************************//**
 * @brief        Unappend interrupt handler for specific QEI interrupt source
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
 **********************************************************************/
void QEIHW::UnAppendISR(uint32_t ulISRType) {
    int i;
    
    for(i = 0; i < 13; i++) {
        if( ulISRType == (1UL << i) ) {
            _qei_isr[i] = NULL;
            break;
        }
    }
    return;
}


void QEIHW::_Qeiisr(void)
{
    instance->Qeiisr();
}

/*********************************************************************//**
 * @brief        QEI interrupt service dispatcher. 
 * 
 * @param[in]    none
 *                                 
 * @return       none
 **********************************************************************/
void QEIHW::Qeiisr(void)  
{
    int32_t i;

    //User defined interrupt handlers. Check all possible sources, dispatch to corresponding non-null service routines.
    for(i = 0; i < 13; i++) {
        if(LPC_QEI->QEIINTSTAT & ((uint32_t)(1<<i)) ) {
            if (_qei_isr[i] != NULL) {
                _qei_isr[i]();
            }
        }
    }
    return;
}

