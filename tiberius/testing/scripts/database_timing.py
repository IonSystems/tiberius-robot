import time
import sys
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.sqlite_database import SqliteDatabase

#creating instance of class
poly = PolyhedraDatabase("poly_tibby")
sql = SqliteDatabase("sqlite_tibby")

#delete tables if they already exist
def drop_tables():
    try:
        poly.drop("Test")
        print "dropped poly table"
    except PolyhedraDatabase.OperationalError:
        print "poly Table does not exist"
    except PolyhedraDatabase.NoSuchTableError:
        print "poly Table does not exist"
    try:
        sql.drop("Test1")
        print "dropped sql table"
    except SqliteDatabase.OperationalError:
        print "sql Table does not exists"

#Create a new test table with polyhedra named 'Test'
def polycreate():
    try:
        a = time.time()
        poly.create("Test", {'id':'int primary key', 'col_int':'int', 'col_float':'float','col_text':'varchar(100)'})
        b = time.time()
        print "Time to create poly database: " + str(b - a)
    except PolyhedraDatabase.OperationalError:
        print "poly Table 'Test' already exists"

#Create a new test table with sqlite named Test1
def sqlitecreate():
    try:
        a = time.time()
        sql.create("Test1", {'id':'int primary key', 'testint':'int', 'testfloat':'float','testtext':'varchar(100)'})
        b = time.time()
        print "Time to create sql database: " + str(b - a)
    except SqliteDatabase.OperationalError:
        print "sql Table already exists"

#insert 1000 test data
def insert():
    a = time.time()
    for i in range(0, 1000):
        poly.insert("Test", {'id':i, 'col_int':i+3, 'col_float':i*0.245,'col_text':"i is " + str(i)})
    b = time.time()
    for j in range(0, 1000):
        sql.insert("Test1", {'id':j, 'testint':j+3, 'testfloat':j*0.245,'testtext':"j is " + str(j)})
    c = time.time()

    print "Time to insert into polyhedra database: " + str( (b - a) /1000 ) #divide by 1000 to take average
    print "Time to insert into sqlite database: " + str( (c - b) /1000 )

#update all the data stored
def update():
    a = time.time()
    for i in range (0, 1000):
        poly.update("Test",
                    {
                    'col_int': i+5,
                    'col_float': i*0.725,
                    'col_text' : "i is currently"  + str(i)
                    },
                    {'clause': 'WHERE',
                     'data': [
                         {
                             'column': 'id',
                             'assertion': '=',
                             'value': i
                         }
                     ]})
    b = time.time()
    for j in range (0, 1000):
        sql.update("Test1",
            {
                'testint': j+5,
                'testfloat': j*0.725,
                'testtext' : "j is currently"  + str(j)
            },
            {
                'clause':'WHERE',
                'data': [
                    {
                        'column' : 'id',
                        'assertion' : '=',
                        'value': j
                    }
                ]
            })
    c = time.time()
    print "Time to update into poly database: " + str((b - a) /1000)
    print "Time to update into sqlite database: " + str((c - b) /1000)

def query():
    a = time.time()
    for i in range (0, 1000):
        result = sql.query("Test1", "*")
    b = time.time()
    for i in range (0, 1000):
        result2 = poly.query("Test", "*")
    c = time.time()

    print "Time for querying sqlite database: " + str((b - a)/1000)
    print "Time for querying polyhedra database: " + str((c - b)/1000)
    #print result, result2

if __name__ == '__main__':
    drop_tables()
    polycreate()
    sqlitecreate()
    insert()
    update()
    query()
