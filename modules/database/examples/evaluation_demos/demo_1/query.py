#!/usr/bin/python
import pyodbc
import subprocess

# Opening database
try:
    subprocess.Popen(['rtrdb','db'], stdout=subprocess.PIPE)

except subprocess.CalledProcessError:
    print 'ERROR OPENING DATABASE'

# Connecting to database
cnxn = pyodbc.connect('DSN=8001')
cursor = cnxn.cursor()

for row in cursor.execute("select usdollar from currency"):
        
        print(row)

for row in cursor.execute("select mission_status from tasos"):
        
        print(row)
