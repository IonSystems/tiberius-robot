import time
import sys
from tiberius.utils import detection
#If not running on a raspberry pi, use the dummy smbus library to allow simulation of I2C transactions.
if detection.detect_pi():
    import serial


#####Global Variables######################################
#be sure to declare the variable as 'global var' in the fxn
ser = 0

#####FUNCTIONS#############################################
#initialize serial connection
def init_serial():
    COMNUM = 1 #set you COM port # here
    global ser #must be declared in each fxn used
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    ser.open() #open the serial port

    # print port open or closed
    if ser.isOpen():
        print 'Open: ' + ser.portstr
#####SETUP################################################
#this is a good spot to run your initializations
init_serial()

#####MAIN LOOP############################################
while 1:
    #prints what is sent in on the serial port
    #temp = raw_input('Type what you want to send, hit enter:\n\r')
    #ser.write(temp) #write to the serial port
    bytes = ser.readline() #reads in bytes followed by a newline
    print bytes #print to the console
    time.sleep(0.1)
#hit ctr-c to close python window
