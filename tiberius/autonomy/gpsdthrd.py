#!/usr/bin/python

import gps
import threading

gpsd = None


class gpspol(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps.gps(mode=gps.WATCH_ENABLE)
        self.running = True

    def run(self):
        global gpsd
        # gets latest frames of gps data
        while self.running:
            # if there is data
            if gpsd.waiting():
                gpsd.next()
