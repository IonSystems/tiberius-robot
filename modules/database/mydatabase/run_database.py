#! usr/bin/env python

import pyodbc
import subprocess
import socket
from DatabaseClient import DatabaseClient

# ******************************************** DATABASE *******************************************
try:
   subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)
   cnxn=pyodbc.connect('DSN=8001')
except subprocess.CalledProcessError:
   print 'ERROR OPENING DATABASE'
   
  # cnxn   = pyodbc.connect('DSN=8001')

# ******************************************* SERVER SOCKET ***************************************
HOST = '' # All available interfaces
PORT = 60000 # Arbitrary port

# Create a new socket and bind the socket to the PORT
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

# Listen for up to 5 socket clients.
server.listen(5)

# Always listen for a socket client.
while 1:
   client = DatabaseClient(server.accept(),cnxn) # start a new database client
   #client = DatabaseClient(server.accept()) # start a new database client
   client.start() # run the client on a thread
      
      
      
      
