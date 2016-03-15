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
        poly.create("Test", {'id':'int primary key', 'col_int':'int', 'col_float':'float','col_text':'varchar(100)'})
        print "created poly table"
    except PolyhedraDatabase.OperationalError:
        print "poly Table 'Test' already exists"

#Create a new test table with sqlite named Test1
def sqlitecreate():
    try:
        sql.create("Test1", {'id':'int primary key', 'testint':'int', 'testfloat':'float','testtext':'varchar(100)'})
        print "created sql table"
    except SqliteDatabase.OperationalError:
        print "sql Table4 already exists"

def insert():
    a = time.time()
    for i in range(0, 100):
        sql.insert("Test1", {'id':i, 'testint':i+3, 'testfloat':i*0.245,'testtext':"i is " + str(i)})
    b = time.time()
    for j in range(0, 100):
        poly.insert("Test", {'id':j, 'col_int':j+3, 'col_float':j*0.245,'col_text':"j is " + str(j)})
    c = time.time()

    print "Time to insert into sqlite database: " + str(b - a)
    print "Time to insert into polyhedra database: " + str(c - b)

def query():
    a = time.time()
    for i in range (0, 50):
        result = sql.query("Test1", "*")
    b = time.time()
    for i in range (0, 50):
        result2 = poly.query("Test", "*")
    c = time.time()

    print "Time for querying sqlite database: " + str(b - a)
    print "Time for querying polyhedra database: " + str(c - b)
    print result, result2

if __name__ == '__main__':
    drop_tables()
    polycreate()
    sqlitecreate()
    insert()
    query()
