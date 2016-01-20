#!/usr/bin/python

import socket
#import autonomy_mode
import manual_mode
import databasecoms as dtbcoms
import time

# coms parameters

# Tiberius status
tiberius_status = "TIBERIUS_STATUS."
autonomy = "AUTONOMY_MODE"
idle = "IDLE_MODE"
manual = "MANUAL_MODE"

HOST = '192.168.2.100'
PORT = 60000
s = socket.socket()
s.connect((HOST, PORT))

data = ''

while True:
    try:
        data = dtbcoms.getdata(tiberius_status)
        print data
        if (data == manual):
            manual_mode.manualmode()
        time.sleep(0.5)

    except KeyboardInterrupt:
        print 'top_module KeyboardInterrupt'
        break
