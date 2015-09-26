#!/usr/bin/python
import pyodbc
cnxn = pyodbc.connect('DSN=3283')
cursor = cnxn.cursor()
for row in cursor.execute("select code, usdollar from currency"):
        print('Currency Code',row.code, ' -1 US Dollar buys', row.usdollar)
