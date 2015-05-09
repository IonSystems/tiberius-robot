#!/usr/bin/python

import threading
import time
import cmps11
import gps
import gpsdthrd
import srf08
import socket

class sensorsthrd(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        #gps thread to get latest frames of gps data
        gpsp = gpsdthrd.gpspol()
        gpsd = gpsdthrd.gpsd
        gpsp.start()
        gpscnt = 0
        #while gpsd.fix.longitude==0:
        #    if (gpscnt==0):
        #        if (gpscnt==0): gpscnt+=1
        #        print 'waiting for gps'
        print 'gps ready'
        
        srffr = srf08.srf08(0x72)
        srffc = srf08.srf08(0x71)
        srffl = srf08.srf08(0x70)
        srfrr = srf08.srf08(0x73)
        srfrc = srf08.srf08(0x74)
        srfrl = srf08.srf08(0x75)
        
        lon = 0
        lat = 0
        cmpsh = 0
        
        HOST = '192.168.2.100'
        PORT = 60000
        s = socket.socket()
        s.connect((HOST,PORT))
        
        while self.running:
            #GPS data
            #print 'time: ',time.time()
            lon = gpsd.fix.longitude
            lat = gpsd.fix.latitude
            if (str(lon)=='nan'):
                lon = 0.0
                lat = 0.0
            #print 'lat: ',lat,' lon: ',lon
            s.sendall("WRITE.GPS,LAT:"+str(lat)+",LON:"+str(lon)+".")

            #CMPS11 data
            cmpsh = cmps11.heading()
            #print 'cmps: ',cmpsh
            s.sendall("WRITE.COMPASS,"+str(cmpsh)+".")

            #SRF08 data
            srfrr.doranging()
            srffrm = srffr.getranging()
            srffcm = srffc.getranging()
            srfflm = srffl.getranging()
            srfrrm = srfrr.getranging()
            srfrcm = srfrc.getranging()
            srfrlm = srfrl.getranging()
            #print "FL:",srfflm,"FC:",srffcm,"FR:",srffrm,"RL:",srfrlm,"RC:",srfrcm,"RR:",srfrrm
            s.sendall("WRITE.RANGEFINDERS,FL:"+str(srfflm)+",FC:"+str(srffcm)+",FR:"+str(srffrm)+\
                      ",RL:"+str(srfrlm)+",RC:"+str(srfrcm)+",RR:"+str(srfrrm)+".")   

        gpsp.running = False
        gpsp.join()
        print 'gpsp closed'                        
        s.close()
