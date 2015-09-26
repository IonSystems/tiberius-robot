#! usr/bin/env python

import socket
import datetime
import pyodbc
import subprocess
import time
import re

ID_index=0

HOST = '192.168.2.100'
PORT=60000

#s=socket.socket()
#s.connect((HOST,PORT))

try:
   subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)
 
except subprocess.CalledProcessError:
   print 'ERROR OPENING DATABASE'
   

cnxn= pyodbc.connect('DSN=8001')
cursor=cnxn.cursor()
#now=datetime.datetime.time(datetime.datetime.now())
#message="WRITE.COMPASS,1.23"
message="RANGEFINDERS,FL:00,FC:00,FR:00,RL:00,RC:00,RR:00"

for ID_index in range(0,200):

   live_FL=re.sub(r'.*FL:(\d+\.?\d*),.*',r'\1',message)
   live_FC=re.sub(r'.*FC:(\d+\.?\d*),.*',r'\1',message)
   live_FR=re.sub(r'.*FR:(\d+\.?\d*),.*',r'\1',message)
   live_RL=re.sub(r'.*RL:(\d+\.?\d*),.*',r'\1',message)
   live_RC=re.sub(r'.*RC:(\d+\.?\d*),.*',r'\1',message)
   live_RR=re.sub(r'.*RR:(\d+\.?\d*).*',r'\1',message)
  

   ID=str(ID_index)
   now=str(datetime.datetime.time(datetime.datetime.now()))
   cursor.execute("insert into RANGEFINDERS_data values(?,?,?,?,?,?,?,?)",'RF'+ID,live_FL,live_FC,live_FR,live_RL,live_RC,live_RR,now)
   cnxn.commit()

#print ""

#if (ID_index==200):

#cursor.execute("select value from compass_data where ID=?",'CPas'+ID)
#row=cursor.fetchone()

        
#if row:
      
#   compass_value=row.value
#   print 'The latest compass data:',compass_value


#print "LIVE_FL= {0}".format(live_FL)
#print "LIVE_FC= {0}".format(live_FC)
#print "LIVE_FR = {0}".format(live_FR)
#print "LIVE_RL = {0}".format(live_RL)
#print "LIVE_RC = {0}".format(live_RC)
#print "LIVE_RR = {0}".format(live_RR)






#





















#MISSION STATUS TEST

#s.sendall("WRITE.AUTONOMY_MODE,LAT:1.123456,LON:2.234567,OBJ:HEX.")
#s.sendall("WRITE.OBJECT_SIMILARITY,CUBE:1.12,HEX:2.23,STAR:3.33.")
#s.sendall("WRITE.IDLE_MODE")
#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row
#
#time.sleep(5)

#s.sendall("WRITE.MISSION_STATUS,NAVIGATING")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row

#time.sleep(5)


#s.sendall("WRITE.MISSION_STATUS,DESTINATION_REACHED")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row

#time.sleep(5)

#s.sendall("WRITE.MISSION_STATUS,SCANNING OBJECTS")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row

#time.sleep(5)

#s.sendall("WRITE.MISSION_STATUS,ANALYSING_IMAGE")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row

#time.sleep(5)

#s.sendall("WRITE.MISSION_STATUS,OBJECT_DETECTED")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row

#time.sleep(5)

#s.sendall("WRITE.MISSION_STATUS,MISSION_FINISHED")

#cursor.execute("select * from mission_status")
#row=cursor.fetchall()
#print row
