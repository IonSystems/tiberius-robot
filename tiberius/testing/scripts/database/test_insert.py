import pyodbc

cnxn = pyodbc.connect("DSN=8001", autocommit=True)
cursor = cnxn.cursor()


cursor.execute("insert into test_table(id, column) values(33,22)")
