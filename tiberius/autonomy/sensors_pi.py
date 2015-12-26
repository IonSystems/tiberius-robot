#!/usr/bin/python

import time
import rplidar
import sensthrd
import socket
import re

#establishing connection with database pi
HOST = '192.168.2.100'
PORT = 60000
s = socket.socket()
s.connect((HOST,PORT))

#running srf08, smps11 and gps as a thread since it
#takes about 1 second for lidar data to be processed and sent
#and it takes about 20ms (when run as a thread) for the rest
#of the sensors data to be processed and sent
sensors = sensthrd.sensorsthrd()
sensors.start()

linespol = []

try:
    while(1):
        #LIDAR data
        linespol = rplidar.getlines()
        lnstr=""
        if (len(linespol)!=0):
            #send linespol list as a string of values separated by commas
            for lncnt in xrange(0,len(linespol)):
                lnstr+=str(linespol[lncnt])
            lnstr = lnstr.replace("[","")
            lnstr = lnstr.replace("]",", ")
            lnstr = re.sub(r'(.*), $',r'\1',lnstr)
        else:
            lnstr = 'EMPTY'
        #print 'lidar: ',lnstr
        s.sendall("WRITE.LIDAR,"+str(lnstr)+".")               

except KeyboardInterrupt:
    sensors.running = False
    sensors.join()
    print 'sensthrd closed'
    s.close()
    print 'KeyboardInterrupt done'
