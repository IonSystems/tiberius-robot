import time
import sys
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.sqlite_database import SqliteDatabase

poly = PolyhedraDatabase("poly_tibby")
sql = SqliteDatabase("sqlite_tibby")

def drop_tables():
    try:
        poly.drop("Test")
    except PolyhedraDatabase.OperationalError:
        print "Table already exists"
    except PolyhedraDatabase.NoSuchTableError:
        print "Table2 already exists"

    try:
        sql.drop("Test1")
    except SqliteDatabase.OperationalError:
        print "Table3 already exists"

def polycreate():
    try:
        poly.create("Test", {'id':'int primary key', 'col_int':'int', 'col_float':'float','col_text':'varchar(100)'})
    except PolyhedraDatabase.OperationalError:
        print "Table5 already exists"

def sqlitecreate():
    try:
        sql.create("Test1", {'id':'int primary key', 'testint':'int', 'testfloat':'float','testtext':'varchar(100)'})
    except SqliteDatabase.OperationalError:
        print "Table4 already exists"

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
