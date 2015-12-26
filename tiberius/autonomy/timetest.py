#!/usr/bin/python

import time
import md03

leftf = md03.md03(0x58)
leftr = md03.md03(0x5A)
rightf = md03.md03(0x5B)
rightr = md03.md03(0x59)
accel = 15

start = time.time()
while time.time()-start<1/.52:
    leftf.move(-255,accel)
    leftr.move(-255,accel)
    rightf.move(-255,accel)
    rightr.move(-255,accel)
leftf.move(0,accel)
leftr.move(0,accel)
rightf.move(0,accel)
rightr.move(0,accel)
print 'done'
