#!/usr/bin/python

import math
import time
import cmps11
import md03
import rplidar
import srf08

# a function, which returns a distance between two polar coordinates


def poldist(th1, r1, th2, r2):
    d = math.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 *
                  math.cos(th2 / 180 * math.pi - th1 / 180 * math.pi))
    return d


def objdet():
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
    rotsp = 130

    cmpsh = 0
    linespol = []
    firstcnt = 0
    cnt = 0
    objsize = 41  # defines the size(cm) of an object to look for
    objtol = 3.7  # introduces tolerance parameter in cm
    drivedist = 0
    driveangle = 0
    turnang = 0
    turnangfx = 17  # defines an angle offset from the center of an object
    stopdist = 37  # defines how far(cm) from an object the robot stops

    try:
        linespol = rplidar.getlines()
        print linespol
        if (len(linespol) != 0):
            for lines in linespol:
                # looks for objects
                if (poldist(lines[0], lines[1], lines[2], lines[3]) >= objsize - objtol and
                        poldist(lines[0], lines[1], lines[2], lines[3]) <= objsize + objtol):
                    cnt += 1  # counts the number of objects
                    firstcnt += 1
                    # remembers the first object location
                    if (firstcnt == 1):
                        firstcnt += 1  # won't enter this if again
                        print 'turnang line: ', lines
                        # calculates an angle to face the center of an object
                        if (lines[2] - lines[0] < 0):
                            turnang = lines[2] - \
                                (lines[2] - lines[0] + 360) / 2
                        else:
                            turnang = lines[2] - (lines[2] - lines[0]) / 2
                        # creates an offset from the center of an object so that when the robot
                        # turns to that angle and gets rplidar data the first
                        # object will be this one
                        if (turnang - turnangfx < 0):
                            turnang = turnang - turnangfx + 360
                        else:
                            turnang = turnang - turnangfx

            # check all the objects found
            for x in xrange(0, cnt):
                print 'turnang: ', turnang
                cmpsh = cmps11.heading()
                # the robot turns until the heading is turnang
                if (turnang - cmpsh > 180):
                    cmpsh += 360
                elif (turnang - cmpsh < -180):
                    cmpsh -= 360
                while (turnang - cmpsh < -1.5 or turnang - cmpsh > 1.5):
                    cmpsh = cmps11.heading()
                    print 'cmpsh: ', cmpsh
                    if (turnang - cmpsh > 180):
                        cmpsh += 360
                    elif (turnang - cmpsh < -180):
                        cmpsh -= 360
                    # turn to the left
                    if (turnang - cmpsh < 0):
                        leftf.move(-rotsp, accel)
                        leftr.move(-rotsp, accel)
                        rightf.move(rotsp, accel)
                        rightr.move(rotsp, accel)
                    # turn to the right
                    elif (turnang - cmpsh > 0):
                        leftf.move(rotsp, accel)
                        leftr.move(rotsp, accel)
                        rightf.move(-rotsp, accel)
                        rightr.move(-rotsp, accel)
                    time.sleep(0.11)
                leftf.move(0, accel)
                leftr.move(0, accel)
                rightf.move(0, accel)
                rightr.move(0, accel)
                time.sleep(1)

                firstcnt = 0
                scndcnt = 0
                linespol = rplidar.getlines()
                print linespol
                for lines in linespol:
                    print 'firstcnt: ', firstcnt
                    print 'scndcnt: ', scndcnt
                    if (scndcnt == 2):
                        break
                    # looks for objects
                    if (poldist(lines[0], lines[1], lines[2], lines[3]) >= objsize - objtol and
                            poldist(lines[0], lines[1], lines[2], lines[3]) <= objsize + objtol):
                        firstcnt += 1
                        scndcnt += 1
                        if (firstcnt == 1):
                            print 'firstcnt line: ', lines
                            firstcnt += 1
                            # calculates the time to drive back after facing an object in order to
                            # get back to the starting position
                            drivedist = lines[1] - stopdist
                            # calculates an angle to face the center of an
                            # object
                            if (lines[2] - lines[0] < 0):
                                driveangle = lines[
                                    2] - (lines[2] - lines[0] + 360) / 2
                            else:
                                driveangle = lines[2] - \
                                    (lines[2] - lines[0]) / 2
                        if (scndcnt == 2):
                            print 'scndcnt line: ', lines
                            # calculates an angle to face the center of an
                            # object
                            if (lines[2] - lines[0] < 0):
                                turnang = lines[2] - \
                                    (lines[2] - lines[0] + 360) / 2
                            else:
                                turnang = lines[2] - (lines[2] - lines[0]) / 2
                            # creates an offset from the center of an object so that when the robot
                            # turns to that angle and gets rplidar data the
                            # first object will be this one
                            if (turnang - turnangfx < 0):
                                turnang = turnang - turnangfx + 360
                            else:
                                turnang = turnang - turnangfx

                print 'driveangle: ', driveangle
                print 'drivedist: ', drivedist
                cmpsh = cmps11.heading()
                if (driveangle - cmpsh > 180):
                    cmpsh += 360
                elif (driveangle - cmpsh < -180):
                    cmpsh -= 360
                # turns to face the center of an object
                while (driveangle - cmpsh < -1.5 or driveangle - cmpsh > 1.5):
                    cmpsh = cmps11.heading()
                    print 'cmpsh: ', cmpsh
                    if (driveangle - cmpsh > 180):
                        cmpsh += 360
                    elif (driveangle - cmpsh < -180):
                        cmpsh -= 360
                    # turn to the left
                    if (driveangle - cmpsh < 0):
                        leftf.move(-rotsp, accel)
                        leftr.move(-rotsp, accel)
                        rightf.move(rotsp, accel)
                        rightr.move(rotsp, accel)
                    # turn to the right
                    elif (driveangle - cmpsh > 0):
                        leftf.move(rotsp, accel)
                        leftr.move(rotsp, accel)
                        rightf.move(-rotsp, accel)
                        rightr.move(-rotsp, accel)
                    time.sleep(0.07)
                leftf.move(0, accel)
                leftr.move(0, accel)
                rightf.move(0, accel)
                rightr.move(0, accel)
                time.sleep(0.5)

                srfrr.doranging()
                #srffrm = srffr.getranging()
                srffcm = srffc.getranging()
                # drives forward until the robot faces the object adjusting its
                # path on the way
                while(srffcm > stopdist):
                    cmpsh = cmps11.heading()
                    print 'cmpsh: ', cmpsh
                    if (driveangle - cmpsh > 180):
                        cmpsh += 360
                    elif (driveangle - cmpsh < -180):
                        cmpsh -= 360
                    if (driveangle - cmpsh > -1.5 and driveangle - cmpsh < 1.5):
                        leftf.move(250, accel)
                        leftr.move(250, accel)
                        rightf.move(250, accel)
                        rightr.move(250, accel)
                    elif (driveangle - cmpsh < 0):
                        leftf.move(170, accel)
                        leftr.move(170, accel)
                        rightf.move(250, accel)
                        rightr.move(250, accel)
                    elif (driveangle - cmpsh > 0):
                        leftf.move(250, accel)
                        leftr.move(250, accel)
                        rightf.move(170, accel)
                        rightr.move(170, accel)
                    srfrr.doranging()
                    #srffrm = srffr.getranging()
                    srffcm = srffc.getranging()
                    # print 'front: ',srffcm
                    #srfflm = srffl.getranging()
                    time.sleep(0.11)
                leftf.move(0, accel)
                leftr.move(0, accel)
                rightf.move(0, accel)
                rightr.move(0, accel)

                time.sleep(2)
                print 'image processing'
                # add code for image processing

                # drives back to the initial location
                start = time.time()
                while(time.time() - start < drivedist / 52):
                    leftf.move(-255, accel)
                    leftr.move(-255, accel)
                    rightf.move(-255, accel)
                    rightr.move(-255, accel)
                    time.sleep(0.1)
                leftf.move(0, accel)
                leftr.move(0, accel)
                rightf.move(0, accel)
                rightr.move(0, accel)

        if (cnt == 0):
            print 'No objects detected'
        else:
            print 'Done'

    except KeyboardInterrupt:
        leftf.move(0, accel)
        leftr.move(0, accel)
        rightf.move(0, accel)
        rightr.move(0, accel)
        print 'KeyboardInterrupt in object detection'

objdet()
