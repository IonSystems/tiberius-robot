#! usr/bin/env python

import pyodbc
import subprocess
import socket
from DatabaseClient import DatabaseClient

# ******************************************** DATABASE *******************************************
try:
   subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)
  # cnxn=pyodbc.connect('DSN=8001')
except subprocess.CalledProcessError:
   print 'ERROR OPENING DATABASE'
   

cnxn= pyodbc.connect('DSN=8001')
cursor=cnxn.cursor()


#INITIALIZE DATABASE VALUES WHEN STARTING THE SERVER

params_TS = [('FALSE','AM'),('TRUE','IM'),('FALSE','MM')]
params_MP = [('NULL','LONG'),('NULL','LAT'),('NULL','SELOBJ')]
params_OS = [('NULL','OBJ1'),('NULL','OBJ2'),('NULL','OBJ3')]
params_MS = [('FALSE','ST0'),('FALSE','ST1'),('FALSE','ST2'),('FALSE','ST3'),('FALSE','ST4'),('FALSE','ST5'),('TRUE','ST6'),('FALSE','ST7')]
params_PV = [('NULL','ST0'),('NULL','ST1'),('NULL','ST2'),('NULL','ST3'),('NULL','ST4'),('NULL','ST5'),('NULL','ST6'),('FALSE','ST7')]
params_LD = [('NULL','LD0'),('NULL','LD1'),('NULL','LD2'),('NULL','LD3'),('NULL','LD4'),('NULL','LD5'),('NULL','LD6'),('NULL','LD7'),('NULL','LD8'),('NULL','LD9'),('NULL','LD10'),('NULL','LD11'),('NULL','LD12'),('NULL','LD13'),('NULL','LD14'),('NULL','LD15'),('NULL','LD16'),('NULL','LD17'),('NULL','LD18'),('NULL','LD19'),('NULL','LD20'),('NULL','LD21'),('NULL','LD22'),('NULL','LD23'),('NULL','LD24'),('NULL','LD25')]

cursor.executemany("update tiberius_status set value=? where ID=?",params_TS)
cnxn.commit()
cursor.executemany("update mission_parameters set value=? where ID=?",params_MP)
cnxn.commit()
cursor.executemany("update object_similarity set similarity=? where ID=?",params_OS)
cnxn.commit()
cursor.executemany("update mission_status set value=? where ID=?",params_MS)
cnxn.commit()
cursor.executemany("update mission_status set pause_value=? where ID=?",params_PV)
cnxn.commit()
cursor.executemany("update LIDAR_data set value=? where ID=?",params_LD)
cnxn.commit()

cursor.execute("delete from compass_data where id<>?",'')    # ZERO ALL COMPASS DATA
cnxn.commit()
cursor.execute("insert into compass_data values(?,?,?)", 'CP' ,'0','0')
cnxn.commit()
cursor.execute("delete from GPS_data where id<>?",'')        # ZERO ALL GPS DATA
cnxn.commit()
cursor.execute("insert into GPS_data values(?,?,?,?)",'GPS','0','0','0')
cnxn.commit()
cursor.execute("delete from RANGEFINDERS_data where id<>?",'')    # ZERO ALL RANGEFINDER DATA
cnxn.commit()
cursor.execute("insert into RANGEFINDERS_data values(?,?,?,?,?,?,?,?)",'RF','0','0','0','0','0','0','0') # ZERO ALL RANGEFINDER DATA
cnxn.commit()

#cursor.execute("delete from LIDAR_data where id<>?",'')    # ZERO ALL LIDAR DATA
#cnxn.commit()
#cursor.execute("insert into LIDAR_data values(?,?,?)",'LD','0','0') # ZERO ALL LIDAR DATA
#cnxn.commit()


# ******************************************* SERVER SOCKET ***************************************
HOST = '' # All available interfaces
PORT = 60000 # Arbitrary port

# Create a new socket and bind the socket to the PORT
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket.allow_reuse_adress = True
server.bind((HOST,PORT))


# Listen for up to 5 socket clients.
server.listen(5)

try:
   # Always listen for a socket client.
   while 1:
     
      client = DatabaseClient(server.accept(),cnxn) # start a new database client
    
      client.start() # run the client on a thread
    
except KeyboardInterrupt:
   client.running = False
   print client.count()
      
      
      
      
