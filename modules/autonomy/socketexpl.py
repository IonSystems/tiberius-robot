#!/usr/bin/python


import socket

HOST = '192.168.2.100' # All available interfaces
PORT = 60000 # Arbitrary port

s = socket.socket()

s.connect((HOST,PORT))

data = s.recv(1024)

data = data.replace("\n","")

#s.sendall("WRITE.OBJECT_SIMILARITY,CUBE:20.14,HEX:5.21,STAR:7.34.")

#s.sendall("WRITE.MISSION_STATUS,NAVIGATING.")
#s.sendall("WRITE.MISSION_STATUS,DESTINATION_REACHED.")
#s.sendall("WRITE.MISSION_STATUS,ANALYSING_IMAGE.")
#s.sendall("WRITE.MISSION_STATUS,SCANNING_OBJECTS.")
s.sendall("WRITE.MISSION_STATUS,OBJECT_DETECTED.")

