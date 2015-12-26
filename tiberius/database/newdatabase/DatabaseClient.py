#! usr/bin/env python

import socket
import re
import threading
import pyodbc
import time
import datetime

# COMMANDS THAT CAN BE RECEIVED
READ  = "READ"
WRITE = "WRITE"          

#WRITE AUTONOMY STATUS PARAMETERS
AUTONOMY_MODE = "AUTONOMY_MODE"
IDLE_MODE     = "IDLE_MODE"
MANUAL_MODE   = "MANUAL_MODE"

#READ AUTONOMY STATUS PAREMETER
TIBERIUS_STATUS = "TIBERIUS_STATUS"

#READ OBJECT TO BE DETECTED
OBJECT_SIMILARITY = "OBJECT_SIMILARITY"

#READ GPS VALUE
MISSION_GPS = "MISSION_GPS"

#MISSION_OBJECT
MISSION_OBJECT = "MISSION_OBJECT"

#MISSION_STATUS
MISSION_STATUS= "MISSION_STATUS"
NAVIGATING="NAVIGATING"
DESTINATION_REACHED="DESTINATION_REACHED"
SCANNING_OBJECTS="SCANNING_OBJECTS"
ANALYSING_IMAGE="ANALYSING_IMAGE"
OBJECT_DETECTED="OBJECT_DETECTED"
MISSION_FINISHED="MISSION_FINISHED"

#MISSION_PAUSED
MISSION_START = "MISSION_START"
MISSION_PAUSED="MISSION_PAUSED"
MISSION_RESUMED="MISSION_RESUMED"

#COMPASS DATA
COMPASS="COMPASS"
#GPS DATA
GPS="GPS"
#RANGEFINDERS
RANGEFINDERS="RANGEFINDERS"
#LIDAR
LIDAR="LIDAR"

#NEW LINE REQUIRED FOR DECODING OF MESSAGES BY CLIENTS
EOL = "\n"
#READ LIDAR
NULL='NULL'
params_LD = [('NULL','LD0'),('NULL','LD1'),('NULL','LD2'),('NULL','LD3'),('NULL','LD4'),('NULL','LD5'),('NULL','LD6'),('NULL','LD7'),('NULL','LD8'),('NULL','LD9'),('NULL','LD10'),('NULL','LD11'),('NULL','LD12'),('NULL','LD13'),('NULL','LD14'),('NULL','LD15'),('NULL','LD16'),('NULL','LD17'),('NULL','LD18'),('NULL','LD19'),('NULL','LD20'),('NULL','LD21'),('NULL','LD22'),('NULL','LD23'),('NULL','LD24'),('NULL','LD25')]





# CREATE A THREAD FOR HANDLING THE CLIENTS
class DatabaseClient(threading.Thread):
   def __init__(self,(client,address),database):   #add database variable
      threading.Thread.__init__(self)
      self.client   = client
      self.address  = address
      self.database = database
      self.cnt = 0
      self.running = True
   

   # Receive data from the socket and decode its message.  
   def run(self):      

      # while connected to this client.
      while (self.running): 

         message = self.client.recv(2048)
      #   print message
         self.cnt+=1
     #    print "Connected to address = {0}".format(self.address)
         
     #    print message
         
         # disconnect when the client closes the socket
         if not message: break  
                      
         # else decode the received message             
         else: self.decode(message) 
            
      self.client.close()
     
    #  print "Disconnected"


   def count(self):
      return self.cnt
         
         
#********************************************DECODE THE INPUT MESSAGE*********************************************************************#



      
   def decode(self, message):

      
     
#*****************************IF A WRITE TO THE DATABASE IS REQUESTED FROM A CLIENT**********************************#
      if(WRITE in message):
         
         if(AUTONOMY_MODE in message):

            AUTONOMY_status = AUTONOMY_MODE
        
            self.updateTiberiusStatus(AUTONOMY_MODE)  # UPDATE THE TIBERIUS_STATUS TABLE


# GET MISSION_PARAMETERS TABLE
            latitude        = re.sub(r'.*LAT:(\d+\.?\d*),.*',r'\1',message)  
            longitude       = re.sub(r'.*LON:(\d+\.?\d*),.*',r'\1',message) 
            selected_object = re.sub(r'.*OBJ:(\w+)\.',r'\1',message)


# UPDATE THE MISSION_PARAMETERS TABLE
          

            self.updateParameters(latitude,longitude,selected_object)   

      #      print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)
      #      print "Latitude = {0}".format(latitude)
      #       print "Longitude = {0}".format(longitude)
      #       print "Object = {0}\n\n\n".format(selected_object)
                     

#TIBERIUS_STATUS=IDLE MODE   

         elif(IDLE_MODE in message):

            AUTONOMY_status = IDLE_MODE
            # update the robot status in the database
            self.updateTiberiusStatus(IDLE_MODE)
     #       print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)

         
           
#TIBERIUS_STATUS=MANUAL MODE

         elif(MANUAL_MODE in message):
            AUTONOMY_status = MANUAL_MODE
            # update the robot status in the database
            self.updateTiberiusStatus(MANUAL_MODE)
     #       print "\n\n\nAUTONOMY_status = {0}".format(AUTONOMY_status)


#OBJECT SIMILARITY WRITE

         elif(OBJECT_SIMILARITY in message):


           #acquire similarity values
           cube=re.sub(r'.*CUBE:(\d+\.?\d*),.*',r'\1',message)
           hexagon=re.sub(r'.*HEX:(\d+\.?\d*),.*',r'\1',message)
           star=re.sub(r'.*STAR:(\d+\.?\d*).*',r'\1',message)

           self.UpdateObjectSim(cube,hexagon,star)  

   #        print "Similarity to CUBE is = {0}".format(cube)
   #        print "Similarity to HEXAGON is = {0}".format(hexagon)
   #        print "Similarity to STAR is = {0}\n\n\n".format(star)

        
#MISSION STATUS WRITE

         elif(MISSION_STATUS in message):

            self.UpdateMissionStatus(message)

      
#WRITE LIVE COMPASS DATA TO THE DATABASE

         elif(COMPASS in message):

           
           heading=re.sub(r'.*,(\d+\.?\d*).*',r'\1',message)   #Regular expression used to obtain the heading value from the message

   #        print "The compass value is = {0}".format(heading)

           self.InsertCompassData(heading)      #Pass the heading and the index the WRITE FUNCTION

          
   
#WRITE LIVE GPS DATA TO THE DATABASE

         elif(GPS in message):
            
            live_latitude=re.sub(r'.*LAT:(\d+\.?\d*),.*',r'\1',message)  
            live_longtitude=re.sub(r'.*LON:(\d+\.?\d*).*',r'\1',message)

    #        print "LIVE_Latitude = {0}".format(live_latitude)
    #        print "LIVE_Longitude = {0}".format(live_longtitude)

            self.InsertGPSData(live_latitude,live_longtitude)

         elif(RANGEFINDERS in message):

            live_FL=re.sub(r'.*FL:(\d+\.?\d*),.*',r'\1',message)
            live_FC=re.sub(r'.*FC:(\d+\.?\d*),.*',r'\1',message)
            live_FR=re.sub(r'.*FR:(\d+\.?\d*),.*',r'\1',message)
            live_RL=re.sub(r'.*RL:(\d+\.?\d*),.*',r'\1',message)
            live_RC=re.sub(r'.*RC:(\d+\.?\d*),.*',r'\1',message)
            live_RR=re.sub(r'.*RR:(\d+\.?\d*).',r'\1',message)

   #         print "live_FL = {0}".format(live_FL)
   #         print "live_FC = {0}".format(live_FC)
   #         print "live_FR = {0}".format(live_FR)
   #         print "live_RL = {0}".format(live_RL)
   #         print "live_RC = {0}".format(live_RC)
   #         print "live_RR = {0}".format(live_RR)
            

            self.InsertRangeFinderData(live_FL,live_FC,live_FR,live_RL,live_RC,live_RR)

         elif(LIDAR in message):
            
            live_LIDAR=re.sub(r'.*,(\d+\.?\d*,?\s?(\d+\.?\d*,?\s?)+)\.$',r'\1',message)
            self.InsertLidarData(live_LIDAR)

              
#*****************************************************************READ FROM DATABASE *************************************************************#
      #IF A READ FROM THE DATABASE IS REQUESTED FROM A CLIENT
      elif(READ in message):
         cursor = self.database.cursor() #initiate the cursor

        
         #READ TIBERIUS STATUS(AUTONOMY,IDLE,MANUAL)
         if (TIBERIUS_STATUS in message):
            cursor.execute("select STATUS from tiberius_status where VALUE=?",'TRUE')
            row=cursor.fetchone()

            if row:

               STATE=row.status
     #         print 'Mode currently in use:',STATE
               self.client.sendall(STATE + EOL)    #SEND TIBERIUS STATUS TO  CLIENT
               

           
         #READ OBJECT_SIMILARITY TABLE  
         elif (OBJECT_SIMILARITY) in message:
            cursor.execute("select similarity from object_similarity")
            row = cursor.fetchall()

            if row:
  
                cube=str(row[0].similarity)
                hexagon=str(row[1].similarity)
                star=str(row[2].similarity)
       #        print '\n Cube similarity percentage:',cube,'\n Hexagon similarity percentage:',hexagon ,'\n Star similarity percentage:', star 
                self.client.sendall(cube + "," + hexagon + "," + star + EOL)

       
         #SEND GPS DATA TO CLIENT
         elif (MISSION_GPS) in message:
            cursor.execute("select longtitude,latitude from mission_parameters")
            row = cursor.fetchall()

            if row:

               longtitude=str(row[0].value)
               latitude=str(row[1].value)
        #      print 'GPS latitude:',latitude,'GPS longtitude:',longtitude
               self.client.sendall(latitude + "," + longtitude + ","  +EOL)


         
         #SEND MISSION OBJECT INFO TO CLIENT     
         elif (MISSION_OBJECT) in message:           
             cursor.execute("select value from mission_parameters")
             row=cursor.fetchall()

             if row:

                mission_obj=row[2].value
        #       print 'The mission object is:',mission_obj
                self.client.sendall(mission_obj +EOL)

       
         #SEND MISSION STATUS TO CLIENT 
         elif (MISSION_STATUS) in message:
            cursor.execute("select STATUS from mission_status where VALUE=?",'TRUE')
            row=cursor.fetchone()

            if row:

               mission_stat=row.status
      #        print 'The mission status is:',mission_stat
               self.client.sendall(mission_stat +EOL)

      
         #SEND MISSION PAUSE INFO TO CLIENT 
         elif (MISSION_PAUSED) in message:
            cursor.execute("select pause_value from mission_status where status=?",'MISSION_PAUSED')
            row=cursor.fetchone()

            if row:

               mission_pause=row.pause_value
       #        print 'The mission is:',mission_pause
               self.client.sendall(mission_pause +EOL)


         # SEND COMPASS_DATA
         elif (COMPASS) in message:
           cursor.execute("select value from compass_data where ID=?",'CP')  #ID_COMPASS
           row=cursor.fetchone()

           if row:

               compass_value=row.value
          #     print 'The latest compass data:',compass_value
               self.client.sendall(compass_value +EOL)



      #SEND GPS DATA
         elif (GPS) in message:

              cursor.execute("select latitude,longtitude from GPS_data where ID=?",'GPS') #ID_GPS
              row = cursor.fetchone()

              if row:
               
                 live_long=row.longtitude
                 live_lat=row.latitude

             #    print 'LIVE GPS latitude:',live_long,' LIVE GPS longtitude:',live_lat
                 self.client.sendall(live_lat + ","+live_long +EOL)

      #SEND RANGEFINDER DATA

         elif(RANGEFINDERS) in message:

            cursor.execute("select front_left,front_centre,front_right,rear_left,rear_centre,rear_right from RANGEFINDERS_data")
            row=cursor.fetchone()

            if row:
            
               live_FL=row.front_left
               live_FC=row.front_centre
               live_FR=row.front_right
               live_RL=row.rear_left
               live_RC=row.rear_centre
               live_RR=row.rear_right

           #    print  'LIVE RANGEFINDER READ \n:Front Left:',live_FL,' Front Centre:',live_FC,'Front Right:',live_FR,'Rear Left:',live_RL, 'Rear Centre:',live_RC,'Rear Right:',live_RR

               self.client.sendall(live_FL + "," + live_FC + "," + live_FR + "," + live_RL + ","+ live_RC + "," + live_RR +EOL)


    #SEND LIDAR DATA
         elif(LIDAR) in message:
            live_LD=''
           
            for x in xrange(0,27): #rowcount
               cursor.execute("select value from LIDAR_data where ID=?",'LD'+str(x))
               row = cursor.fetchone()

               if row:
                 val=row.value
                
                 if(val!= NULL):
                     live_LD+=val 
                     
                 else:
                     break
            print "READ FROM DATABASE = {0}".format(live_LD)
            self.client.sendall(live_LD +EOL)
            
            

#*********************************WRITE/INSERT FUNCTIONS****************************************************************************
           

           
#INSERT LIDAR DATA


   def InsertLidarData(self,LIDAR):
     cursor= self.database.cursor()
     params_LD = [('NULL','LD0'),('NULL','LD1'),('NULL','LD2'),('NULL','LD3'),('NULL','LD4'),('NULL','LD5'),('NULL','LD6'),('NULL','LD7'),('NULL','LD8'),('NULL','LD9'),('NULL','LD10'),('NULL','LD11'),('NULL','LD12'),('NULL','LD13'),('NULL','LD14'),('NULL','LD15'),('NULL','LD16'),('NULL','LD17'),('NULL','LD18'),('NULL','LD19'),('NULL','LD20'),('NULL','LD21'),('NULL','LD22'),('NULL','LD23'),('NULL','LD24'),('NULL','LD25')]
     cursor.executemany("update LIDAR_data set value=? where ID=?",params_LD)
     self.database.commit()

     for x in xrange(0,int(len(LIDAR)/80)+1):
     #  cursor= self.database.cursor()
       line =(LIDAR[x*80:x*80+80]) #lidar...
      
       cursor.execute("update LIDAR_data set value=? where ID=?",str(line),'LD'+str(x))
       self.database.commit()
      

#INSERT RANGEFINDER DATA

   def InsertRangeFinderData(self,FL,FC,FR,RL,RC,RR):
       
       cursor= self.database.cursor()
       now=datetime.datetime.time(datetime.datetime.now())
      
       cursor.execute("update RANGEFINDERS_data set id=?,front_left=?,front_centre=?,front_right=?,rear_left=?,rear_centre=?,rear_right=?,instance=?",'RF',str(FL),str(FC),str(FR),str(RL),str(RC),str(RR),str(now))
       self.database.commit()


       # cursor.execute("insert into RANGEFINDERS_data values(?,?,?,?,?,?,?,?)",'RF'+ID_R,live_FL,live_FC,live_FR,live_RL,live_RC,live_RR,now)
       #  self.database.commit()
         
#INSERT COMPASS DATA

   def InsertCompassData(self,heading):

       cursor= self.database.cursor()
       now=datetime.datetime.time(datetime.datetime.now())

       cursor.execute("update compass_data set ID=?,value=?,instance=?",'CP',str(heading),str(now))
       self.database.commit()

      # cursor.execute("insert into compass_data values(?,?,?)",str(row_new),str(now),str(heading))
      # self.database.commit()
      
       

#INSERT GPS DATA

   def InsertGPSData(self,LAT,LONG):

       cursor= self.database.cursor()
       now=datetime.datetime.time(datetime.datetime.now())

       cursor.execute("update GPS_data set id=?,latitude=?,longtitude=?,instance=?",'GPS',str(LAT),str(LONG),str(now))
       self.database.commit()


     #  cursor.execute("insert into GPS_data values(?,?,?,?)",'GPS'+ID_GPS,str(LAT),str(LONG),now)
     #  self.database.commit()


       
               
#UPDATE THE MISSION PARAMETERS IN THE MISSION_PARAMETER TABLE
       
   def updateParameters(self,LAT,LONG,OBJ):

      cursor= self.database.cursor()

      #UPDATE LATITUDE IN DATABASE
      cursor.execute("update mission_parameters set VALUE= ? where ID=?",LAT,'LAT') 
      self.database.commit()
      #UPDATE LONGTITUDE IN DATABASE
      cursor.execute("update mission_parameters set VALUE= ? where ID=?",LONG,'LONG')
      self.database.commit()
      #UPDATE TARGET OBJECT IN DATABASE
      cursor.execute("update mission_parameters set VALUE= ? where ID=?",OBJ,'SELOBJ')
      self.database.commit()


              
#UPDATE THE TIBERIUS STATUS IN THE TIBERIUS_STATUS TABLE

      
   def updateTiberiusStatus(self, status):

      cursor = self.database.cursor() #initiate the cursor
      
      if   (status == AUTONOMY_MODE):
        
         #VALUE=0.0 for all STATUS entries
         cursor.execute("update tiberius_status set VALUE=? where VALUE=?",'FALSE','TRUE')
         self.database.commit()

         #VALUE=1.0 for correspondent mode in currently in use
         cursor.execute("update tiberius_status set VALUE=? where STATUS='AUTONOMY_MODE'",'TRUE')

         #Commit changes done to the database
         self.database.commit()
         
         #Print Database Result 
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
       #  print row 
        
         
      elif (status == IDLE_MODE): 
       
      
         cursor.execute("update tiberius_status set VALUE=? where VALUE=?",'FALSE','TRUE')
         self.database.commit()

        
         cursor.execute("update tiberius_status set VALUE=? where STATUS='IDLE_MODE'",'TRUE')
         self.database.commit()

         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
      #   print row 
        
         
      elif (status == MANUAL_MODE): 
        
        
         cursor.execute("update tiberius_status set VALUE=? where VALUE=?",'FALSE','TRUE')
         self.database.commit()
         
         cursor.execute("update tiberius_status set VALUE=? where STATUS='MANUAL_MODE'",'TRUE')
         self.database.commit()
         
        
         cursor.execute("select STATUS,VALUE from tiberius_status")
         row = cursor.fetchall()
      #   print row

#UPDATE THE OBJECT SIMILARITY IN THE OBJECT SIMILARITY TABLE
   def UpdateObjectSim(self,cube,hexagon,star):
        cursor = self.database.cursor() 

        cursor.execute("update object_similarity set SIMILARITY=? where id=?",cube,'OBJ1')
        cursor.execute("update object_similarity set SIMILARITY=? where id=?",hexagon,'OBJ2')
        cursor.execute("update object_similarity set SIMILARITY=? where id=?",star,'OBJ3')
        self.database.commit()


#UPDATE THE MISSION STATUS IN THE MISSION_STATUS TABLE
   
   def UpdateMissionStatus(self,message):
      cursor = self.database.cursor() 
      cursor.execute("update mission_status set VALUE=? where VALUE=?",'FALSE','TRUE')
      self.database.commit()
      
      if (MISSION_START in message):
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST0')
         self.database.commit()

  
      if(NAVIGATING in message):
        
       
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST1')
         self.database.commit()
      

      elif(DESTINATION_REACHED in message):
        
        
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST2')
         self.database.commit()
         

      elif(SCANNING_OBJECTS in message):
         
        
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST3')
         self.database.commit()

      elif(ANALYSING_IMAGE in message):
   
         
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST4')
         self.database.commit()

      elif(OBJECT_DETECTED in message):
      
        
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST5')
         self.database.commit()

      elif(MISSION_FINISHED in message):
      
         
         cursor.execute("update mission_status set VALUE=? where id=?",'TRUE','ST6')
         self.database.commit()

      elif(MISSION_PAUSED in message):
     
         cursor.execute("update mission_status set PAUSE_VALUE=? where id=?",'TRUE','ST7')     
         self.database.commit()

      elif(MISSION_RESUMED in message):
    
         cursor.execute("update mission_status set PAUSE_VALUE=? where id=?",'FALSE','ST7')
         self.database.commit()


   





























   
      
