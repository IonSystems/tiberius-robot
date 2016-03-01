import pyodbc

cnxn = pyodbc.connect("DSN=8001")
cursor = cnxn.cursor()


cursor.execute("select * from test_table")
