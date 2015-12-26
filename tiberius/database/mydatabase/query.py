#!/usr/bin/python
import pyodbc
import subprocess

# Opening database
try:
    subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)
    cnxn = pyodbc.connect('DSN=8001')
    cursor = cnxn.cursor()   
    
except subprocess.CalledProcessError:
    print 'ERROR OPENING DATABASE'



#cursor.execute("update object_detect set VALUE=?",0.0)
#VALUE=1.0 for correspondent mode in currently in use
#cursor.execute("update object_detect set SIMILARITY=? where OBJECTS='HEXAGON'",0.89)
#cnxn.commit()
##Print Database 
#cursor.execute("select OBJECTS,SIMILARITY from object_detect")
#row = cursor.fetchall()
#print row


#FETCH THE STATUS AND SAVE IN A PARAMEMETER CALLED STATE
cursor.execute("select STATUS from tiberius_status where VALUE= ?", 1.0)
row=cursor.fetchone()
if row:
    STATE=row.status
    print 'Mode currently in use:',STATE
             








