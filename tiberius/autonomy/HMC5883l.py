import smbus
import time
import math


bus = smbus.SMBus(1)

HMC5883l = 0x1e


# Registers
CONFIG_REG_A = 0x00
CONFIG_REG_B = 0x01

MODE_REGISTER = 0x02

DATA_OUT_X_H = 0x03
DATA_OUT_X_L = 0x04

DATA_OUT_Y_H = 0x07
DATA_OUT_Y_L = 0x08

DATA_OUT_Z_H = 0x05
DATA_OUT_Z_L = 0x06


STATUS = 0x09

ID_REG_A = 0x10
ID_REG_B = 0x11
ID_REG_C = 0x12


def SETUP():
    # Device Setup
    #
    CONFIG_A = 0b01111000
    bus.write_byte_data(HMC5883l, CONFIG_REG_A, CONFIG_A)

    CONFIG_B = 0b00100000
    bus.write_byte_data(HMC5883l, CONFIG_REG_B, CONFIG_B)


def MODE_SETUP():

    MODE = 0b00000001
    bus.write_byte_data(HMC5883l, MODE_REGISTER, MODE)
    # Delay 6ms for setup propogation
    time.sleep(0.006)


def Get_value(device, address_H):

    word = bus.read_i2c_block_data(device, address_H, 2)
    raw_data = (word[0] << 8) + (word[1])

    if (raw_data >= 0x8000):
        return -((~raw_data & 0xFFFF) + 1)
    else:
        return raw_data


def Calibration_Values():

    M_11 = 1.152
    M_12 = 0.02
    M_13 = -0.012
    M_21 = 0.014
    M_22 = 1.075
    M_23 = 0.076
    M_31 = 0.019
    M_32 = -0.028
    M_33 = 1.218

    B_x = 81.362
    B_y = -276.446
    B_z = -110.716

    return (M_11, M_12, M_13, M_21, M_22, M_23, M_31, M_32, M_33, B_x, B_y, B_z)


def reading():
    scale = 0.92
    X_nc = Get_value(HMC5883l, DATA_OUT_X_H) * scale
    Y_nc = Get_value(HMC5883l, DATA_OUT_Y_H) * scale
    Z_nc = Get_value(HMC5883l, DATA_OUT_Z_H) * scale

    coeff = Calibration_Values()

    X_c = (coeff[0] * (X_nc - coeff[9])) + (coeff[1] *
                                            (Y_nc - coeff[10])) + (coeff[2] * (Z_nc - coeff[11]))
    Y_c = (coeff[3] * (X_nc - coeff[9])) + (coeff[4] *
                                            (Y_nc - coeff[10])) + (coeff[5] * (Z_nc - coeff[11]))
    Z_c = (coeff[6] * (X_nc - coeff[9])) + (coeff[7] *
                                            (Y_nc - coeff[10])) + (coeff[8] * (Z_nc - coeff[11]))

    bearing_c = math.atan2(Y_c, X_c)
    if(bearing_c < 0):
        bearing_c += 2 * math.pi

    print "X: ", X_c, "Y: ", Y_c, "Z: ", Z_c, "Bearing: ", math.degrees(bearing_c)

SETUP()

while True:
    MODE_SETUP()
    reading()

    time.sleep(0.1)
