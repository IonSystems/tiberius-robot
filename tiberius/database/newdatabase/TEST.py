#!/usr/bin/python
import pyodbc
import re
import subprocess

# Opening database
try:
    subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)
  
    
except subprocess.CalledProcessError:
    print 'ERROR OPENING DATABASE'




cnxn= pyodbc.connect('DSN=8001')
cursor=cnxn.cursor()

params_LD = [('NULL','LD0'),('NULL','LD1'),('NULL','LD2'),('NULL','LD3'),('NULL','LD4'),('NULL','LD5'),('NULL','LD6'),('NULL','LD7'),('NULL','LD8'),('NULL','LD9'),('NULL','LD10'),('NULL','LD11'),('NULL','LD12'),('NULL','LD13'),('NULL','LD14'),('NULL','LD15'),('NULL','LD16'),('NULL','LD17'),('NULL','LD18'),('NULL','LD19'),('NULL','LD20'),('NULL','LD21'),('NULL','LD22'),('NULL','LD23'),('NULL','LD24'),('NULL','LD25')]
cursor.executemany("update LIDAR_data set value=? where ID=?",params_LD)
cnxn.commit()

#message="WRITE.LIDAR,53.8531, 240.875, 53.8531, 240.875, 56.4312, 97.05, 56.4312, 97.05, 65.9, 68.275, 104.525, 102.6, 104.9938, 206.075, 107.9312, 198.65, 109.9781, 68.275, 111.9469, 68.275, 114.8688, 181.8, 192.884, 218.625, 195.588, 85.05, 197.541, 86.45, 198.759, 244.75, 206.588, 298.45, 208.119, 115.2, 211.181, 111.375, 212.088, 112.55, 212.088, 112.55, 213.322, 87.975, 221.072, 89.175, 221.603, 136.85, 237.697, 92.475, 238.728, 93.875, 247.228, 117.7, 248.712, 271.875, 250.697, 274.8, 251.9, 174.475, 252.822, 177.25, 253.603, 276.3, 259.494, 287.925, 263.338, 294.725, 277.009, 347.075, 279.916, 362.65, 280.9, 370.35, 281.978, 257.55, 281.978, 257.55, 282.853, 383.275, 283.822, 388.375, 285.759, 403.675, 285.759, 403.675, 288.681, 424.05, 291.603, 460.675, 294.541, 467.05, 294.541, 467.05, 296.494, 453.55, 297.494, 460.45, 308.853, 131.925, 309.916, 130.925, 310.838, 136.0, 330.588, 131.225, 331.525, 140.925, 331.525, 140.925, 332.056, 321.9, 332.056, 321.9, 333.572, 125.6, 335.4, 116.65, 336.4, 116.65, 347.134, 122.375, 348.572, 306.825, 349.541, 305.825, 350.494, 310.5, 356.338, 332.175, 357.338, 325.425, 3.181, 347.675, 4.166, 365.975, 5.119, 358.95, 6.119, 363.475, 9.041, 380.125, 10.9, 543.575, 11.884, 543.575, 14.822, 511.6, 16.791, 496.45, 19.728, 481.2, 21.884, 461.2, 22.884, 460.15, 23.884, 448.9, 29.869, 332.175, 32.822, 325.325, 34.806, 306.75, 34.806, 306.75, 35.759, 346.45, 35.759, 346.45, 37.759, 310.125, 38.744, 307.625, 39.744, 313.05, 40.728, 306.425, 45.666, 383.5, 47.666, 380.325, 48.634, 383.0, 50.619, 376.125, 51.806, 268.2, 52.806, 265.85."
#lidar=re.sub(r'.*,(\d+\.?\d*,?\s?(\d+\.?\d*,?\s?)+)\.$',r'\1',message)


#for x in xrange(0,int(len(lidar)/80)+1):
#    line =(lidar[x*80:x*80+79]) #lidar...
#    cursor.execute("update LIDAR_data set value=? where ID=?",str(line),'LD'+str(x))
#    cnxn.commit()

#row=''
#lidar=''
#NULL='NULL'
#for x in xrange(0,27): #rowcount
#    cursor.execute("select value from LIDAR_data where ID=?",'LD'+str(x))
#    row = cursor.fetchone()
#    if row:
#        val=row.value
        #val=str(y)

#        if(val!=NULL):
#            lidar+=val 
#        else:
#            break

#print lidar
   
cursor.execute("select * from RANGEFINDERS_data")
            row=cursor.fetchall()

            if row:
            
               live_FL=row.front_left
               live_FC=row.front_centre
               live_FR=row.front_right
               live_RL=row.rear_left
               live_RC=row.rear_centre
               live_RR=row.rear_right

               print  'LIVE RANGEFINDER READ \n:Front Left:',live_FL,' Front Centre:',live_FC,'Front Right:',live_FR,'Rear Left:',live_RL, 'Rear Centre:',live_RC,'Rear Right:',live_RR

               self.client.sendall(live_FL + "," + live_FC + "," + live_FR + "," + live_RL + ","+ live_RC + "," + live_RR +EOL)



#print check
#if (check==lidar):
#    print 'happy'
#    #  cursor= self.database.cursor()
#       now=datetime.datetime.time(datetime.datetime.now())
#       cursor.execute("update GPS_data set id=?,latitude=?,longtitude=?,instance=?",'GPS',str(LAT),str(LONG),str(now))
#       self.database.commit()
