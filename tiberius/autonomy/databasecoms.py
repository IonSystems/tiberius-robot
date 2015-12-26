#!/usr/bin/python

import socket

#establish connection to the databse pi
HOST = '192.168.2.100'
PORT = 60000
s = socket.socket()
s.connect((HOST,PORT))

#coms parameters

#sensors
gps = "GPS."
cmps = "COMPASS."
srf08 = "RANGEFINDERS."
lidar = "LIDAR."

#mission status
mis_status = "MISSION_STATUS."
mis_start = "MISSION_START."
navigating = "NAVIGATING."
dest_reached = "DESTINATION_REACHED."
scan_objects = "SCANNING_OBJECTS"
analyse_img = "ANALYSE_IMAGE"
object_detected = "OBJECT_DETECTED"
mis_finished = "MISSION_FINISHED."
mis_paused = "MISSION_PAUSED"

#mission parameters
mis_gps = "MISSION_GPS."

#Tiberius status
tiberius_status = "TIBERIUS_STATUS."
autonomy = "AUTONOMY_MODE"
idle = "IDLE_MODE"
manual = "MANUAL_MODE"


def getdata(parameter):
    try:
        lststr = []
        lstflt = []
        
        if (parameter==gps):
            s.sendall("READ.GPS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            lststr = data.split(",")
            lstflt = ([float(lststr[0]),float(lststr[1])])
            return lstflt
        
        elif (parameter==cmps):
            s.sendall("READ.COMPASS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            return float(data)
        
        elif (parameter==srf08):
            s.sendall("READ.RANGEFINDERS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            lststr = data.split(",")
            lstflt = ([float(lststr[0]),float(lststr[1]),float(lststr[2]),\
                       float(lststr[3]),float(lststr[4]),float(lststr[5])])
            return lstflt
        
        elif (parameter==lidar):
            s.sendall("READ.LIDAR.")
            data = s.recv(2048)
            data = data.replace("\n","")
            if (data!='EMPTY'):
                #creates a list with 1 member per row
                lststr = data.split(",")
                #creates a list with 4 members per row
                #the same list as linespol produced by rplidar.py
                for cnt in xrange(0,len(lststr),4):
                    lstflt.append([float(lststr[cnt]),float(lststr[cnt+1]),\
                                   float(lststr[cnt+2]),float(lststr[cnt+3])])
            else:
                lstflt = []
            return lstflt
        
        elif (parameter==tiberius_status):
            s.sendall("READ.TIBERIUS_STATUS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            return data

        elif (parameter==mis_status):
            s.sendall("READ.MISSION_STATUS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            return data

        elif (parameter==mis_start):
            s.sendall("WRITE.MISSION_START.")
            return

        elif (parameter==navigating):
            s.sendall("WRITE.NAVIGATING.")
            return

        elif (parameter==dest_reached):
            s.sendall("WRITE.DESTINATION_REACHED.")
            return

        elif (parameter==scan_objects):
            s.sendall("WRITE.SCANNING_OBJECTS.")
            return

        elif (parameter==analyse_img):
            s.sendall("WRITE.ANALYSE_IMAGE.")
            return

        elif (parameter==mis_finished):
            s.sendall("WRITE.MISSION_FINISHED.")
            return

        if (parameter==mis_gps):
            s.sendall("READ.MISSION_GPS.")
            data = s.recv(2048)
            data = data.replace("\n","")
            lststr = data.split(",")
            lstflt = ([float(lststr[0]),float(lststr[1])])
            return lstflt
        
    except KeyboardInterrupt:
        s.close()
        print 'KeyboardInterrupt done in getdata()'
            

