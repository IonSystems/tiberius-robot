#!/usr/bin/python

import math
import time
import cmps11
import gps
import md03
import rplidar
import srf08
import gpsdthrd

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
accel = 15
rotsp = 150

gpsp = gpsdthrd.gpspol()
gpsd = gpsdthrd.gpsd
gpsp.start()
gpscnt = 0
while gpsd.fix.longitude == 0:
    if (gpscnt == 0):
        if (gpscnt == 0):
            gpscnt += 1
        print 'waiting for gps'
print 'gps ready'
gpsh = 0
cmpsh = 0

lonend = math.radians(-3.321220)
latend = math.radians(55.912680)

# both dist and bearing are verified using Google Earth
# functions give about the same values


def gpsdist():
    r = 6371000
    lon = math.radians(gpsd.fix.longitude)
    lat = math.radians(gpsd.fix.latitude)
    latdel = latend - lat
    londel = lonend - lon
    a = math.sin(latdel / 2) * math.sin(latdel / 2) + \
        math.cos(lat) * math.cos(latend) * \
        math.sin(londel / 2) * math.sin(londel / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def gpsheading():
    lon = math.radians(gpsd.fix.longitude)
    lat = math.radians(gpsd.fix.latitude)
    y = math.sin(lonend - lon) * math.cos(latend)
    x = math.cos(lat) * math.sin(latend) - \
        math.sin(lat) * math.cos(latend) * math.cos(lonend - lon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

try:
    if (gpsdist() > 1.1):
        gpsh = gpsheading()
        cmpsh = cmps11.heading()
        if (gpsh - cmpsh > 180):
            cmpsh += 360
        elif (gpsh - cmpsh < -180):
            cmpsh -= 360
        while (gpsh - cmpsh < -1 or gpsh - cmpsh > 1):
            cmpsh = cmps11.heading()
            print 'cmpsh: ', cmpsh
            print 'gpsh: ', gpsh
            print 'lon: ', gpsd.fix.longitude
            print 'lat: ', gpsd.fix.latitude
            if (gpsh - cmpsh > 180):
                cmpsh += 360
            elif (gpsh - cmpsh < -180):
                cmpsh -= 360
            # turn to the left
            if (gpsh - cmpsh < 0):
                leftf.move(-rotsp, accel)
                leftr.move(-rotsp, accel)
                rightf.move(rotsp, accel)
                rightr.move(rotsp, accel)
            # turn to the right
            elif (gpsh - cmpsh > 0):
                leftf.move(rotsp, accel)
                leftr.move(rotsp, accel)
                rightf.move(-rotsp, accel)
                rightr.move(-rotsp, accel)
            time.sleep(0.27)
        leftf.move(0, accel)
        leftr.move(0, accel)
        rightf.move(0, accel)
        rightr.move(0, accel)

        while (gpsdist() > 1.1):
            gpsh = gpsheading()
            cmpsh = cmps11.heading()
            print 'cmpsh: ', cmpsh
            print 'gpsh: ', gpsh
            if (gpsh - cmpsh > 180):
                cmpsh += 360
            elif (gpsh - cmpsh < -180):
                cmpsh -= 360
            if (gpsh - cmpsh > -2 and gpsh - cmpsh < 2):
                leftf.move(250, accel)
                leftr.move(250, accel)
                rightf.move(250, accel)
                rightr.move(250, accel)
            elif (gpsh - cmpsh < 0):
                leftf.move(170, accel)
                leftr.move(170, accel)
                rightf.move(250, accel)
                rightr.move(250, accel)
            elif (gpsh - cmpsh > 0):
                leftf.move(250, accel)
                leftr.move(250, accel)
                rightf.move(170, accel)
                rightr.move(170, accel)
            time.sleep(0.27)
        leftf.move(0, accel)
        leftr.move(0, accel)
        rightf.move(0, accel)
        rightr.move(0, accel)
        print 'arrived to the destination point'
    gpsp.running = False
    gpsp.join()

except KeyboardInterrupt:
    print 'ctrl+c'
    leftf.move(0, accel)
    leftr.move(0, accel)
    rightf.move(0, accel)
    rightr.move(0, accel)
    gpsp.running = False
    gpsp.join()
