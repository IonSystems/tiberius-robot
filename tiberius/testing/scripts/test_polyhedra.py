import pyodbc
cnxn = pyodbc.connect('DSN=8001')
cursor = cnxn.cursor()

cursor.execute("CREATE TABLE currency (code int, usdollar int)")

for row in cursor.execute("select code, usdollar from currency"):
    print ('Currency code', row.code, '- 1 US Dollar buys', row.usdollar)
