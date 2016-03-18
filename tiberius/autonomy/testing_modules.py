#!/usr/bin/python

import math
import cmps11
import rplidar
#import databasecoms as dtbcom
import md03
import srf08
import time
import re

srffr = srf08.srf08(0x72)
srffc = srf08.srf08(0x71)
srffl = srf08.srf08(0x70)
srfrr = srf08.srf08(0x73)
srfrc = srf08.srf08(0x74)
srfrl = srf08.srf08(0x75)

leftf = md03.md03(0x58)
leftr = md03.md03(0x5A)
rightf = md03.md03(0x5B)
rightr = md03.md03(0x59)
accel = 0
a = 0
linespol = []
lnstr = ''
lstflt = []


def poldist(th1, r1, th2, r2):
    d = math.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 *
                  math.cos(th2 / 180 * math.pi - th1 / 180 * math.pi))
    return d

try:
    while 1:
        leftf.move(255, accel)
        time.sleep(1)
    '''linespol = dtbcom.getdata("RANGEFINDERS.")
    print linespol
    print dtbcom.getdata("COMPASS.")

    while 1:
        print 'cmps11: ', cmps11.heading()
        srfrr.doranging()
        srffrm = srffr.getranging()
        print 'front right: ',srffrm
        srffcm = srffc.getranging()
        print 'front center: ',srffcm
        srfflm = srffl.getranging()
        print 'front left: ',srfflm
        srfrrm = srfrr.getranging()
        #print 'rear right: ',srfrrm
        srfrcm = srfrc.getranging()
        #print 'rear center: ',srfrcm
        srfrlm = srfrl.getranging()
        #print 'rear left: ',srfrlm
        time.sleep(1)
        
    linespol = rplidar.getlines()
    if (len(linespol)!=0):
        for lncnt in xrange(0,len(linespol)):
            lnstr+=str(linespol[lncnt])
        lnstr = lnstr.replace("[","")
        lnstr = lnstr.replace("]"," ,")
        lnstr = re.sub(r'(.*),$',r'\1',lnstr)
    else:
        lnstr = 'EMPTY'
    print linespol
    print ''
    print lnstr
    if (lnstr!='EMPTY'):
        lststr = lnstr.split(",")
        for cnt in xrange(0,len(lststr),4):
            lstflt.append([float(lststr[cnt]),float(lststr[cnt+1]),\
                           float(lststr[cnt+2]),float(lststr[cnt+3])])
    else:
        lstflt = []
    print ''
    print lstflt
    print 'len(lstflt): ',len(lstflt)
    
            

        #print poldist(166.365,234.1,156.209,247.8)
    linespol = rplidar.getlines()
    if (len(linespol)!=0):
        for lncnt in xrange(0,len(linespol)):
            lnstr+=str(linespol[lncnt])
        lnstr = lnstr.replace("[","")
        lnstr = lnstr.replace("]"," ,")
        lnstr = re.sub(r'(.*),$',r'\1',lnstr)
    else:
        lnstr = 'EMPTY'
    print linespol
    print ''
    print lnstr
        
        a=a+50
        if (a==250): a=0
        leftf.move(255,accel)
        leftr.move(0,accel)
        rightf.move(0,accel)
        rightr.move(0,accel)


    

    m1 = md03.md03(0x58,True)
    st = input('key')
    print st
    if (st==1):
        m1.move(0,0)

    d = srf08.srf08(0x74)
    srf1 = srf08.srf08(0x70)
    d.doranging()
    a = srf1.getranging()
    print a
    start = time.time()
    leftf.move(255,accel)
    leftr.move(255,accel)
    rightf.move(255,accel)
    rightr.move(255,accel)
    while time.time()-start<1:
        print cmps11.heading()
    leftf.move(0,accel)
    leftr.move(0,accel)
    rightf.move(0,accel)
    rightr.move(0,accel)

    while True:
        print cmps11.heading()
        time.sleep(0.7)
try:
    linespol = rplidar.getlines()
    print linespol
    print cmps11.heading()'''


except KeyboardInterrupt:
    print 'keyboardint'
    leftf.move(0, accel)
    leftr.move(0, accel)
    rightf.move(0, accel)
    rightr.move(0, accel)
