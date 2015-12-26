#! usr/bin/env python

import socket
import re
import threading
import pyodbc

# COMMANDS THAT CAN BE RECEIVED
READ  = "READ"
WRITE = "WRITE"          

#WRITE AUTONOMY STATUS PARAMETERS
AUTONOMY_START  = "AUTONOMY_START"
AUTONOMY_PAUSE  = "AUTONOMY_PAUSE" 
AUTONOMY_STOP   = "AUTONOMY_STOP"
MANUAL_START   = "MANUAL_START"
MANUAL_STOP    = "MANUAL_STOP"
# used from the android side to continue the AUTONOMY after a pause - translated into AUTONOMY_START for the AUTONOMY status parameters
AUTONOMY_RESUME = "AUTONOMY_RESUME"

# READ AUTONOMY STATUS PAREMETER
TIBERIUS_STATUS = "TIBERIUS_STATUS"

# READ OBJECT TO BE DETECTED
OBJECT_DETECT = "OBJECT_DETECT"


# CREATE A THREAD FOR HANDLING THE CLIENTS
class DatabaseClient(threading.Thread):
   def __init__(self, (client, address),database):   #add database variable
      threading.Thread.__init__(self)
      self.client   = client
      self.address  = address
      self.database = database

   # Receive data from the socket and decode its message.  
   def run(self):      
      
      # while connected to this client.
      while 1: 
         message = self.client.recv(1024)
      
         print "Connected to address = {0}".format(self.address)
         
         print message
         
         # disconnect when the client closes the socket
         if not message: break  
                      
         # else decode the received message             
         else: self.decode(message) 
            
      self.client.close()
      print "Disconnected"
         
         
#******************************************** Decode the input message.*******************************#



      
   def decode(self, message):
      # ***************************** WRITE TO DATABASE ****************************
      if(WRITE in message):
         
         # AUTONOMY_START
         if(AUTONOMY_START in message):
            AUTONOMY_status = AUTONOMY_START
            # update the robot status in the database
            self.updateStatus(AUTONOMY_START)
            # Get the autonomy parameter settings
            latitude        = re.sub(r'.*LAT:(\d+\.?\d*),.*',r'\1',message)  
            longitude       = re.sub(r'.*LON:(\d+\.?\d*),.*',r'\1',message) 
            selected_object = re.sub(r'.*OBJ:(\w+)\.',r'\1',message)
            
            
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
            print "Latitude = {0}".format(latitude)
            print "Longitude = {0}".format(longitude)
            print "Object = {0}\n\n\n".format(selected_object)
            
                        
         # AUTONOMY_PAUSE
         if(AUTONOMY_PAUSE in message):
            AUTONOMY_status = AUTONOMY_PAUSE
            # update the robot status in the database
            self.updateStatus(AUTONOMY_PAUSE)
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)

         
         # AUTONOMY_RESUME
         if(AUTONOMY_RESUME in message):
            AUTONOMY_status = AUTONOMY_START
            # update the robot status in the database
            self.updateStatus(AUTONOMY_START)
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
                  
         # AUTONOMY_STOP
         if(AUTONOMY_STOP in message):
            AUTONOMY_status = AUTONOMY_STOP
            # update the robot status in the database
            self.updateStatus(AUTONOMY_STOP)
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
         
         # MANUAL_START  
         if(MANUAL_START in message):
            AUTONOMY_status = MANUAL_START
            # update the robot status in the database
            self.updateStatus(MANUAL_START)
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
                  
         # MANUAL_STOP 
         if(MANUAL_STOP in message):
            AUTONOMY_status = MANUAL_STOP
            self.updateStatus(MANUAL_STOP)
            print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
            
      # ***************************** READ FROM DATABASE ****************************
      elif(READ in message):
         cursor = self.database.cursor() #initiate the cursor
         #REQUEST FOR CURRENT TIBERIUS MODE IN USE

         if (TIBERIUS_STATUS in message):
            cursor.execute("select STATUS from tiberius_status where VALUE= ?", 1.0)
            row=cursor.fetchone()
            if row:
               STATE=row.status
               print 'Mode currently in use:',STATE
               self.client.sendall(STATE)    #SEND STATUS TO  CLIENT
         if (OBJECT_DETECT) in message:
            pass
        
             
       




    


   




      
                  
            
   # update the robot status in the database      
   def updateStatus(self, status):

      cursor = self.database.cursor() #initiate the cursor
      
      if   (status == AUTONOMY_START):
        
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=?",0.0)
         self.database.commit()

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='AUTONOMY_START'",1.0)

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
         print row 
        
         
      elif (status == AUTONOMY_PAUSE): 
       
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=?",0.0)
         self.database.commit()

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='AUTONOMY_PAUSE'",1.0)

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
         print row 
        
         
      elif (status == AUTONOMY_STOP): 
        
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=?",0.0)
         self.database.commit()

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='AUTONOMY_STOP'",1.0)

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
         print row 
         
      elif (status == MANUAL_START): 
        
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=?",0.0)
         self.database.commit()
         

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='MANUAL_START'",1.0)

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
         print row
         
      elif (status == MANUAL_STOP):
      
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=?",0.0)
         self.database.commit()

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='MANUAL_STOP'",1.0)

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
         print row
      
