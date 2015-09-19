#!/usr/bin/python

import gpsdthrd
import rplidar
import time

gpsp = gpsdthrd.gpspol()
gpsd = gpsdthrd.gpsd

try:
  gpsp.start()
  gpscnt = 0
  while gpsd.fix.longitude==0:
      if (gpscnt==0):
          if (gpscnt==0): gpscnt+=1
          print 'waiting for gps'
  print 'gps ready'
  print 'lat: ', gpsd.fix.latitude
  print 'lon: ', gpsd.fix.longitude
  print rplidar.getlines()
  gpsp.running = False
  gpsp.join()
except KeyboardInterrupt:
  print 'KeyboardInt'
  gpsp.running = False
  gpsp.join()
print 'done'
