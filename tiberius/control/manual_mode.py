#!/usr/bin/python

import socket
import re
import md03
import databasecoms as dtbcoms
import time


def manualmode():
    print 'enetred manual_mode'
    # sensors
    gps = "GPS."
    cmps = "COMPASS."
    srf08 = "RANGEFINDERS."
    lidar = "LIDAR."

    # Tiberius status
    tiberius_status = "TIBERIUS_STATUS."
    autonomy = "AUTONOMY_MODE"
    idle = "IDLE_MODE"
    manual = "MANUAL_MODE"

    leftf = md03.md03(0x58)
    leftr = md03.md03(0x5A)
    rightf = md03.md03(0x5B)
    rightr = md03.md03(0x59)
    accel = 0
    right = 0
    left = 0

    srf = []

    data = 0
    HOST = ''  # all available interfaces
    PORT = 58000  # arbitrary port

    # create a new socket and bind the socket to the PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    # listen only for up to 1 socket clients.
    s.listen(1)

    connection, address = s.accept()  # accept a client connection.
    print "Connected to address = {0}".format(address)

    while (dtbcoms.getdata(tiberius_status) == manual):
        print 'entered manual mode'
        try:
            # print 'BEFORE DATA = {0}'.format(data)
            data = connection.recv(1024)
            # print 'AFTER DATA = {0}'.format(data)
            # left speed data format received: Left,speed value.
            # right speed data format received: Right,speed value.
            # string matching is necessary to remove excessive values from buffers.
            # only last value received is used.

            if (data.find("Left") > -1):
                # STRING MATCHING to find the spped value for the left side
                left = re.sub(
                    r'(\w+,-?\d+.)*Left,(-?\d+).(\w+,-?\d+.)*$', r'\2', data)
                # print "LEFT = {0}".format(left)
            if (data.find("Right") > -1):
                # STRING MATCHING to find the speed value for the right side
                right = re.sub(
                    r'(\w+,-?\d+.)*Right,(-?\d+).(\w+,-?\d+.)*$', r'\2', data)
                # print "RIGHT = {0}".format(right)

            srf = dtbcoms.getdata(srf08)

            # check if there is an obsticle in front
            if ((srf[0] < 37) or (srf[1] < 37) or (srf[2] < 37)):
                # check if robot is trying to drive forward
                if ((int(left) < 0) and (int(right) < 0)):
                    leftf.move(int(left), accel)
                    leftr.move(int(left), accel)
                    rightf.move(int(right), accel)
                    rightr.move(int(right), accel)
                else:
                    print'Obsticle in front'
                    leftf.move(0, accel)
                    leftr.move(0, accel)
                    rightf.move(0, accel)
                    rightr.move(0, accel)
            # check if there is an obsticle behind
            elif ((srf[3] < 27) or (srf[5] < 27)):
                # check if robot is trying to drive back
                if ((int(left) >= 0) and (int(right) >= 0)):
                    leftf.move(int(left), accel)
                    leftr.move(int(left), accel)
                    rightf.move(int(right), accel)
                    rightr.move(int(right), accel)
                else:
                    print'Obsticle behind'
                    leftf.move(0, accel)
                    leftr.move(0, accel)
                    rightf.move(0, accel)
                    rightr.move(0, accel)
            else:
                leftf.move(int(left), accel)
                leftr.move(int(left), accel)
                rightf.move(int(right), accel)
                rightr.move(int(right), accel)

            if not data:
                break

        except KeyboardInterrupt:
            break

    leftf.move(0, accel)
    leftr.move(0, accel)
    rightf.move(0, accel)
    rightr.move(0, accel)
    connection.close()  # stop the connection if no more data is sent.
    print 'manual mode connection.close'
