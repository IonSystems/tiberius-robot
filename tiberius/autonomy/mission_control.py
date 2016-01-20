#!/usr/bin/python

import math
import time
import cmps11
import gps
import md03
import rplidar
import srf08
import gpsdthrd
import object_detection

# coms parameters

# sensors
gps = "GPS."
cmps = "COMPASS."
#srf08 = "RANGEFINDERS."
lidar = "LIDAR."

# mission status
mis_status = "MISSION_STATUS."
mis_start = "MISSION_START."
navigating = "NAVIGATING."
dest_reached = "DESTINATION_REACHED."
scan_objects = "SCANNING_OBJECTS"
analyse_img = "ANALYSE_IMAGE"
object_detected = "OBJECT_DETECTED"
mis_finished = "MISSION_FINISHED."
mis_paused = "MISSION_PAUSED"

# mission parameters
mis_gps = "MISSION_GPS."

# Tiberius status
tiberius_status = "TIBERIUS_STATUS."
autonomy = "AUTONOMY_MODE"
idle = "IDLE_MODE"
manual = "MANUAL_MODE"

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
rotsp = 130  # speed setting for skidding

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
# destination coordinates
lonend = math.radians(-3.321519)
latend = math.radians(55.913029)

activity = 0
state = 0
enclcnt = 0
linespol = []
lncnt = 0
linescnt = 0
linestemp0 = 0
linestemp1 = 0
linestemp00 = 0
linestemp11 = 0
angtemp = 0
drivetime = 0
driveangle = 0
fx = 0
fxdn = 0
fxup = 0
lncntup = 0
lncntdn = 0
actlcnt = 0
drspc = 110.0  # distance in cm from an object for planning a path for object avoidance
addist = 170  # distance in cm defines how far the robot should drive after it passed an object to avoid

# both gpsdist() and gpsheading() are verified using Google Earth tools
# both functions give about the same values as GE tools
# more information about both functions can be found here:
# www.movable-type.co.uk/scripts/latlong.html


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
    print 'lon: ', gpsd.fix.longitude
    print 'lat: ', gpsd.fix.latitude
    y = math.sin(lonend - lon) * math.cos(latend)
    x = math.cos(lat) * math.sin(latend) - \
        math.sin(lat) * math.cos(latend) * math.cos(lonend - lon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

# a function, which returns a distance between two polar coordinates


def poldist(th1, r1, th2, r2):
    d = math.sqrt(r1 * r1 + r2 * r2 - 2 * r1 * r2 *
                  math.cos(th2 / 180 * math.pi - th1 / 180 * math.pi))
    return d

try:
    print 'activity 0'
    linespol = rplidar.getlines()
    gpsh = gpsheading()  # heading towards the destination point
    cmpsh = cmps11.heading()  # compass heading
    print 'linespol: ', linespol
    print 'gpsh: ', gpsh
    print 'cmpsh: ', cmpsh
    # if farer than 1.21m from the destination point
    while (gpsdist() > 1.21):
        # activity 0 analyzes rplidar data and plans the path
        if (activity == 0):
            # state 0 checks if there is an obsticle on the line to the
            # destination point
            if (state == 0):
                print 'state 0'
                print 'lncnt: ', lncnt
                # if there are no obsticles in the 7m radius
                if (len(linespol) == 0):
                    activity = 1

                # if there is one obsticle in the 7m radius
                if (len(linespol) == 1):
                    linestemp0 = linespol[0][0]
                    linestemp1 = linespol[0][2]
                    # by subtracting linespol start and end angles from gpsh it is possible to find on which side of the heading towards
                    # the destination point the start and end of the line are, the difference must be kept in -180 to 180 range
                    # example(all in degrees): start = 40, end = 70, gpsheading = 50. gpsh-start=10, gpsh-end=-20
                    # since start>0 and end<0 the line is in the way of gpsh
                    if (gpsh - linestemp0 > 180):
                        linestemp0 += 360
                    elif (gpsh - linestemp0 < -180):
                        linestemp0 -= 360
                    if (gpsh - linestemp1 > 180):
                        linestemp1 += 360
                    elif (gpsh - linestemp1 < -180):
                        linestemp1 -= 360
                    # if the line is in the way or there is less than 85 cm
                    # between the path towards the destination and any of the
                    # line ends
                    if ((gpsh - linestemp0 > 0 and gpsh - linestemp1 < 0) or (poldist(linespol[0][2], linespol[0][3], gpsh, linespol[0][3]) < 85)
                            or (poldist(gpsh, linespol[0][1], linespol[0][0], linespol[0][1]) < 85)):
                        activity = 2
                        # checks which end of the line is closer and avoids the
                        # object from that side
                        if (linespol[0][1] <= linespol[0][3]):
                            # calculates the closest point to drive to in order to bypass an obsticle
                            # drivetime - distance in cm / 52 = seconds to drive, it was experimentally found that robot covers 52 cm in 1 sec
                            # driveangle - uses formula from poldist() to calculate heading to bypass an obsticle leaving drspc=110cm space
                            # between the robot and an obsticle when passing it
                            # by
                            drivetime = (linespol[0][1] + addist) / 52
                            driveangle = linespol[0][0] - math.acos((-(drspc * drspc) + math.pow(linespol[0][1], 2) + math.pow(linespol[0][1], 2))
                                                                    / (2 * math.pow(linespol[0][1], 2))) / math.pi * 180
                            if (driveangle >= 360):
                                driveangle -= 360
                            elif (driveangle < 0):
                                driveangle += 360
                        else:
                            drivetime = (linespol[0][3] + addist) / 52
                            driveangle = math.acos((-(drspc * drspc) + math.pow(linespol[0][3], 2) + math.pow(linespol[0][3], 2))
                                                   / (2 * math.pow(linespol[0][3], 2))) / math.pi * 180 + linespol[0][2]
                            if (driveangle >= 360):
                                driveangle -= 360
                            elif (driveangle < 0):
                                driveangle += 360
                    # if the line is not in the way
                    elif (poldist(linespol[0][2], linespol[0][3], gpsh, linespol[0][3]) >= 85 or
                          poldist(gpsh, linespol[0][1], linespol[0][0], linespol[0][1]) >= 85):
                        activity = 1

                if (len(linespol) > 1):
                    # introduces another line to make sure that there are no two lines between which there is a gap >180 deg
                    # if a line end is at 20deg and the next one starts at 250deg then the algorithm will check from 250 to 20
                    # rather than desired 20 to 250, so if the full loop has been done once and no passage nor line were found in the
                    # way of gpsh then another line will be introduced and the
                    # loop will be repeated
                    if (lncnt == len(linespol)):
                        angtemp = linespol[lncnt - 1][2] + 179.9
                        if (angtemp > 360):
                            angtemp -= 360
                        linespol.append(
                            [angtemp, linespol[lncnt - 1][3], angtemp, linespol[lncnt - 1][3]])
                        lncnt = 0
                        print 'introduced another line'
                        print linespol
                    linestemp0 = linespol[lncnt][0]
                    linestemp1 = linespol[lncnt][2]
                    if (gpsh - linestemp0 > 180):
                        linestemp0 += 360
                    elif (gpsh - linestemp0 < -180):
                        linestemp0 -= 360
                    if (gpsh - linestemp1 > 180):
                        linestemp1 += 360
                    elif (gpsh - linestemp1 < -180):
                        linestemp1 -= 360
                    # if the line is in the way
                    if (gpsh - linestemp0 > 0 and gpsh - linestemp1 < 0):
                        state = 1
                        lncntup = lncnt
                        lncntdn = lncnt
                    # if current line is the last one then check for the passage between the last line and
                    # the first line by using 'fx' to adjust the lines count
                    if (lncnt == len(linespol) - 1):
                        fx = len(linespol)
                    else:
                        fx = 0
                    linestemp0 = linespol[lncnt][2]
                    linestemp1 = linespol[lncnt + 1 - fx][0]
                    if (gpsh - linestemp0 > 180):
                        linestemp0 += 360
                    elif (gpsh - linestemp0 < -180):
                        linestemp0 -= 360
                    if (gpsh - linestemp1 > 180):
                        linestemp1 += 360
                    elif (gpsh - linestemp1 < -180):
                        linestemp1 -= 360
                    # check if there is a passage in the way of gpsh
                    if (gpsh - linestemp0 > 0 and gpsh - linestemp1 < 0):
                        # check if it is wider than 170cm
                        if (poldist(linespol[lncnt][2], linespol[lncnt][3],
                                    linespol[lncnt + 1 - fx][0], linespol[lncnt + 1 - fx][1]) >= 170):
                            # check which line is closer
                            if (linespol[lncnt][3] <= linespol[lncnt + 1 - fx][1]):
                                # if there is more than 85cm space between the
                                # line end and the path towards the destination
                                if (poldist(linespol[lncnt][2], linespol[lncnt][3], gpsh,
                                            linespol[lncnt][3]) >= 85):
                                    activity = 1
                                # if there is no, then introduce a point to
                                # bypass the closest line
                                else:
                                    activity = 2
                                    drivetime = (
                                        (linespol[lncnt][3] + linespol[lncnt + 1 - fx][1]) / 2 + addist) / 52
                                    driveangle = math.acos((-(drspc * drspc) + math.pow(linespol[lncnt][3], 2) + math.pow(linespol[lncnt][3], 2))
                                                           / (2 * math.pow(linespol[lncnt][3], 2))) / math.pi * 180 + linespol[lncnt][2]
                                    if (driveangle >= 360):
                                        driveangle -= 360
                                    elif (driveangle < 0):
                                        driveangle += 360
                            else:
                                if (poldist(gpsh, linespol[lncnt + 1 - fx][1], linespol[lncnt + 1 - fx][0],
                                            linespol[lncnt + 1 - fx][1]) >= 85):
                                    activity = 1
                                else:
                                    activity = 2
                                    drivetime = (
                                        (linespol[lncnt][3] + linespol[lncnt + 1 - fx][1]) / 2 + addist) / 52
                                    driveangle = linespol[lncnt + 1 - fx][0] - math.acos((-(drspc * drspc) + math.pow(linespol[lncnt + 1 - fx][1], 2)
                                                                                          + math.pow(linespol[lncnt + 1 - fx][1], 2)) / (2 * math.pow(linespol[lncnt + 1 - fx][1], 2))) / math.pi * 180
                                    if (driveangle >= 360):
                                        driveangle -= 360
                                    elif (driveangle < 0):
                                        driveangle += 360
                        else:
                            state = 1
                            lncntup = lncnt
                            lncntdn = lncnt
                lncnt += 1

            # if there is no passage in the way of gpsh then the closest passage is found in state 1
            # it starts with the line numbered 'lncnt' from state 0, 'lncntup' checks for passages clockwise direction and 'lncntdn' checks for
            # passages counterclockwise direction until they meet
            if (state == 1):
                print 'state 1'
                print 'lncntup: ', lncntup
                print 'lncntdn: ', lncntdn
                actlcnt += 1
                print 'actlcnt: ', actlcnt
                # if reached any end of the linespol list adjust the linespol count to the start (for lncntup)
                # or the end (for lncntdn) of the linespol list
                if (lncntdn == 0):
                    fxdn = len(linespol)
                else:
                    fxdn = 0
                if (lncntup == len(linespol) - 1):
                    fxup = len(linespol)
                else:
                    fxup = 0
                linestemp0 = linespol[lncntdn][0]
                linestemp1 = linespol[lncntup][2]
                if (gpsh - linestemp0 > 180):
                    linestemp0 += 360
                elif (gpsh - linestemp0 < -180):
                    linestemp0 -= 360
                if (gpsh - linestemp1 > 180):
                    linestemp1 += 360
                elif (gpsh - linestemp1 < -180):
                    linestemp1 -= 360
                # check which passage is closer and also which passage is wide
                # enough, go for the farer one if the closest one is not wide
                # enough
                if ((math.fabs(gpsh - linestemp0) < math.fabs(gpsh - linestemp1) and poldist(linespol[lncntdn - 1 + fxdn][2], linespol[lncntdn - 1 + fxdn][3],
                                                                                             linespol[lncntdn][0], linespol[lncntdn][1]) >= 170) or (poldist(linespol[lncntdn - 1 + fxdn][2], linespol[lncntdn - 1 + fxdn][3],
                                                                                                                                                             linespol[lncntdn][0], linespol[lncntdn][1]) >= 170 and poldist(linespol[lncntup][2], linespol[lncntup][3],
                                                                                                                                                                                                                            linespol[lncntup + 1 - fxup][0], linespol[lncntup + 1 - fxup][1]) < 170)):
                    activity = 2
                    enclcnt = 0
                    actlcnt = 0
                    drivetime = (linespol[lncntdn][1] + addist) / 52
                    driveangle = linespol[lncntdn][0] - math.acos((-(drspc * drspc) + math.pow(linespol[lncntdn][1], 2) +
                                                                   math.pow(linespol[lncntdn][1], 2)) / (2 * math.pow(linespol[lncntdn][1], 2))) / math.pi * 180
                    if (driveangle >= 360):
                        driveangle -= 360
                    elif (driveangle < 0):
                        driveangle += 360
                    # check if the linespol(lncntdn-1) is in the way of
                    # driveangle
                    linestemp00 = linespol[lncntdn - 1 + fxdn][0]
                    linestemp11 = linespol[lncntdn - 1 + fxdn][2]
                    if (driveangle - linestemp00 > 180):
                        linestemp00 += 360
                    elif (driveangle - linestemp00 < -180):
                        linestemp00 -= 360
                    if (driveangle - linestemp11 > 180):
                        linestemp11 += 360
                    elif (driveangle - linestemp11 < -180):
                        linestemp11 -= 360
                    if (driveangle - linestemp00 > 0 and driveangle - linestemp11 < 0):
                        drivetime = (
                            (linespol[lncntdn - 1 + fxdn][3] + linespol[lncntdn][1]) / 2 + addist) / 52
                        driveangle = math.acos((-(drspc * drspc) + math.pow(linespol[lncntdn - 1 + fxdn][3], 2) + math.pow(linespol[lncntdn - 1 + fxdn][3], 2))
                                               / (2 * math.pow(linespol[lncntdn - 1 + fxdn][3], 2))) / math.pi * 180 + linespol[lncntdn - 1 + fxdn][2]
                        if (driveangle >= 360):
                            driveangle -= 360
                        elif (driveangle < 0):
                            driveangle += 360

                elif ((math.fabs(gpsh - linestemp0) > math.fabs(gpsh - linestemp1) and poldist(linespol[lncntup][2], linespol[lncntup][3],
                                                                                               linespol[lncntup + 1 - fxup][0], linespol[lncntup + 1 - fxup][1]) >= 170) or (poldist(linespol[lncntup][2], linespol[lncntup][3],
                                                                                                                                                                                     linespol[lncntup + 1 - fxup][0], linespol[lncntup + 1 - fxup][1]) >= 170 and poldist(linespol[lncntdn - 1 + fxdn][2], linespol[lncntdn - 1 + fxdn][3],
                                                                                                                                                                                                                                                                          linespol[lncntdn][0], linespol[lncntdn][1]) < 170)):
                    activity = 2
                    enclcnt = 0
                    actlcnt = 0
                    drivetime = (linespol[lncntup][1] + addist) / 52
                    driveangle = math.acos((-(drspc * drspc) + math.pow(linespol[lncntup][3], 2) + math.pow(linespol[lncntup][3], 2))
                                           / (2 * math.pow(linespol[lncntup][3], 2))) / math.pi * 180 + linespol[lncntup][2]
                    if (driveangle >= 360):
                        driveangle -= 360
                    elif (driveangle < 0):
                        driveangle += 360
                    # check if the linespol(lncntdn+1) is in the way of
                    # driveangle
                    linestemp00 = linespol[lncntup + 1 - fxup][0]
                    linestemp11 = linespol[lncntup + 1 - fxup][2]
                    if (driveangle - linestemp00 > 180):
                        linestemp00 += 360
                    elif (driveangle - linestemp00 < -180):
                        linestemp00 -= 360
                    if (driveangle - linestemp11 > 180):
                        linestemp11 += 360
                    elif (driveangle - linestemp11 < -180):
                        linestemp11 -= 360
                    if (driveangle - linestemp00 > 0 and driveangle - linestemp11 < 0):
                        drivetime = (
                            (linespol[lncntup][3] + linespol[lncntup + 1 - fxup][1]) / 2 + addist) / 52
                        driveangle = linespol[lncntup + 1 - fxup][0] - math.acos((-(drspc * drspc) + math.pow(linespol[lncntup + 1 - fxup][1], 2)
                                                                                  + math.pow(linespol[lncntup + 1 - fxup][1], 2)) / (2 * math.pow(linespol[lncntup + 1 - fxup][1], 2))) / math.pi * 180
                        if (driveangle >= 360):
                            driveangle -= 360
                        elif (driveangle < 0):
                            driveangle += 360
                # if reached the end or the beginning of the list then jump to
                # the opposite end
                if (lncntdn == 0):
                    lncntdn = len(linespol) - 1
                else:
                    lncntdn -= 1
                if (lncntup == len(linespol) - 1):
                    lncntup = 0
                else:
                    lncntup += 1
                # check if there is no passage and that there are no two lines between which there is a gap >180 deg
                # introduces another line if there are two lines between which
                # there is a gap >180 deg
                # checks if all the passages were evaluated
                if (actlcnt == int(len(linespol) / 2) + 2):
                    if (enclcnt == 0):
                        actlcnt = 0
                        enclcnt += 1
                        lncntup = lncnt - 1  # lncnt-1 because state 0 stoped at the required line, but before leaving to state 1 lncnt was incremented
                        lncntdn = lncnt - 1
                        angtemp = linespol[len(linespol) - 1][2] + 179.9
                        if (angtemp > 360):
                            angtemp -= 360
                        linespol.append([angtemp, linespol[
                                        len(linespol) - 1][3], angtemp, linespol[len(linespol) - 1][3]])
                        print 'introduced another line'
                        print linespol
                        print 'len(linespol): ', len(linespol)
                    else:
                        print 'Tiberius is in an enclosed area'
                        break

        # if there were no obstacles detected in the way towards the destination point the robot turns to face the destination
        # and drives towards it adjusting its heading on the way by comparing
        # compass data and gpsh
        if (activity == 1):
            print 'activity 1'
            gpsh = gpsheading()
            cmpsh = cmps11.heading()
            if (gpsh - cmpsh > 180):
                cmpsh += 360
            elif (gpsh - cmpsh < -180):
                cmpsh -= 360
            # turns to face the destination point
            while (gpsh - cmpsh < -2 or gpsh - cmpsh > 2):
                cmpsh = cmps11.heading()
                print 'cmpsh: ', cmpsh
                print 'gpsh: ', gpsh
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

            # drives towards the destination point
            while (gpsdist() > 1.1):
                gpsh = gpsheading()
                cmpsh = cmps11.heading()
                print 'cmpsh: ', cmpsh
                print 'gpsh: ', gpsh
                if (gpsh - cmpsh > 180):
                    cmpsh += 360
                elif (gpsh - cmpsh < -180):
                    cmpsh -= 360
                if (gpsh - cmpsh > -1.5 and gpsh - cmpsh < 1.5):
                    leftf.move(250, accel)
                    leftr.move(250, accel)
                    rightf.move(250, accel)
                    rightr.move(250, accel)
                # if robots heading is offset more than +-1.5 degrees from gpsh
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
                srfrr.doranging()
                srffrm = srffr.getranging()
                srffcm = srffc.getranging()
                # print 'front: ',srffcm
                srfflm = srffl.getranging()
                # checks if there is any obsticle in front of
                # the robot by using srf08
                if (srffcm < 75 or srffrm < 75 or srfflm < 75):
                    print 'front right: ', srffrm
                    print 'front center: ', srffcm
                    print 'front left: ', srfflm
                    leftf.move(0, accel)
                    leftr.move(0, accel)
                    rightf.move(0, accel)
                    rightr.move(0, accel)
                    time.sleep(0.21)
                    # drives back for about 1m (for 2.1 sec) to get farer from
                    # the obsticle to plan the path from activity 0
                    start = time.time()
                    while (time.time() - start < 2.1):
                        leftf.move(-255, accel)
                        leftr.move(-255, accel)
                        rightf.move(-255, accel)
                        rightr.move(-255, accel)
                        time.sleep(0.1)
                    leftf.move(0, accel)
                    leftr.move(0, accel)
                    rightf.move(0, accel)
                    rightr.move(0, accel)
                    activity = 0
                    state = 0
                    lncnt = 0
                    print 'activity 0'
                    time.sleep(1.7)
                    gpsh = gpsheading()
                    cmpsh = cmps11.heading()
                    linespol = rplidar.getlines()
                    print 'linespol: ', linespol
                    print 'gpsh: ', gpsh
                    print 'cmpsh: ', cmpsh
                    break
                time.sleep(0.21)
            leftf.move(0, accel)
            leftr.move(0, accel)
            rightf.move(0, accel)
            rightr.move(0, accel)

        # turns the robot to face the calculated point from the
        # activity 0 and drives towards that point
        if (activity == 2):
            print 'activity 2 turning'
            print 'driveangle: ', driveangle
            cmpsh = cmps11.heading()
            if (driveangle - cmpsh > 180):
                cmpsh += 360
            elif (driveangle - cmpsh < -180):
                cmpsh -= 360
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
                time.sleep(0.11)
            leftf.move(0, accel)
            leftr.move(0, accel)
            rightf.move(0, accel)
            rightr.move(0, accel)

            start = time.time()
            print 'activity 2 driving'
            while (time.time() - start < drivetime):
                cmpsh = cmps11.heading()
                print 'cmpsh: ', cmpsh
                if (driveangle - cmpsh > 180):
                    cmpsh += 360
                elif (driveangle - cmpsh < -180):
                    cmpsh -= 360
                if (driveangle - cmpsh > -1.5 and driveangle - cmpsh < 1.5):
                    leftf.move(255, accel)
                    leftr.move(255, accel)
                    rightf.move(255, accel)
                    rightr.move(255, accel)
                elif (driveangle - cmpsh < 0):
                    leftf.move(175, accel)
                    leftr.move(175, accel)
                    rightf.move(255, accel)
                    rightr.move(255, accel)
                elif (driveangle - cmpsh > 0):
                    leftf.move(255, accel)
                    leftr.move(255, accel)
                    rightf.move(175, accel)
                    rightr.move(175, accel)
                srfrr.doranging()
                srffrm = srffr.getranging()
                srffcm = srffc.getranging()
                # print 'front: ',srffcm
                srfflm = srffl.getranging()
                if (srffcm < 55 or srffrm < 55 or srfflm < 55):
                    print 'front right: ', srffrm
                    print 'front center: ', srffcm
                    print 'front left: ', srfflm
                    leftf.move(0, accel)
                    leftr.move(0, accel)
                    rightf.move(0, accel)
                    rightr.move(0, accel)
                    time.sleep(0.21)
                    start = time.time()
                    while (time.time() - start < 2):
                        leftf.move(-255, accel)
                        leftr.move(-255, accel)
                        rightf.move(-255, accel)
                        rightr.move(-255, accel)
                        time.sleep(0.1)
                    break
            leftf.move(0, accel)
            leftr.move(0, accel)
            rightf.move(0, accel)
            rightr.move(0, accel)
            activity = 0
            state = 0
            lncnt = 0
            print 'activity 0'
            time.sleep(1.7)
            gpsh = gpsheading()
            cmpsh = cmps11.heading()
            linespol = rplidar.getlines()
            print 'linespol: ', linespol
            print 'gpsh: ', gpsh
            print 'cmpsh: ', cmpsh

    gpsp.running = False
    gpsp.join()
    print 'arrived to the destination point'
    object_detection.objdet()

except KeyboardInterrupt:
    print 'ctrl+c'
    leftf.move(0, accel)
    leftr.move(0, accel)
    rightf.move(0, accel)
    rightr.move(0, accel)
    gpsp.running = False
    gpsp.join()
    print 'KeyboardInterrupt done'
