#
# Sample pyodb script. Relies on a database "test1" existing with the table 
# "temp". The table schema looks like:
# 
# create table temp (t_one varchar(32), t_two varchar(32), t_three varchar(32))
#
from pyodb import *

# All the calls in pyodb can throw exceptions when an error occurs. 
# You can choose to catch these and handle the error, or allow the
# Python runtime catch them. The error message output with the exception
# will give a SQLSTATE which can be looked up in the ODBC API documentation.

# This creates a new connection object for the database test1. On
# error this will throw a ConnectError exception. When the object is
# destroyed at the end of the program the connection is closed. 
# You can open more than one connection at a time to different databases. 
# ie. c2 = Connect("test2"). You can explicitly close a connection to
# a database if it is no longer required using c1.disconnect(). No error
# is generated if you attempt to close an already closed connection.
c1 = Connect("test1", "root", "neil12")

# If you know the connection string for your ODBC database driver you can 
# specify this using the "conn" argument. For MySQL this might be:
# c1 = Connect(conn="DRIVER={MySQL ODBC 3.51 Driver}; SERVER=localhost; PORT=3306; DATABASE=mysql; UID=joe; PASSWORD=bloggs; OPTION=3;SOCKET=/var/run/mysqld/mysqld.sock;")

# There are 6 methods for the connect object: 
# execute(), fetch(), disconnect(), begin(), commit() and rollback().

# Raw SQL statements are run using the execute() method. This call will
# return the number of rows affected by the command. On error this will
# throw an ExecuteError.

try:
    c1.execute("drop table temp")
except ExecuteError:
    pass # ok if table does not exist

c1.execute("create table temp (c1 char(50), c2 char(50), c3 char(50))")
c1.execute("insert into temp values ('one','two','three')")
c1.execute("insert into temp values ('four','five','six')")
c1.execute("insert into temp values ('seven','eight','nine')")
c1.execute("select * from temp")

# The results of a select can be returned using the fetch() method.
# On error this will throw a FetchError.
rows = c1.fetch()

# The rows are returned as a list of rows (ie a list of lists)
print rows

# You can iterate over each row...
for row in rows:
	# ...and reference the data in each column
	print row[0] + ' ' + row[1] + ' ' + row[2]

# To start a transaction use the connections begin() method. The default
# mode is for all statements to be committed. It is an error to try to 
# start more than one transaction on a connection.
# 
# Of course the database must support transactions.
c1.begin()
c1.execute("insert into temp values ('some','new','data')")
c1.execute("insert into temp values ('some','more','data')")

# To commit or rollback a transaction use the connections commit()
# or rollback() methods. It is an error to commit or rollback on a
# connection that has not started a transaction.
c1.commit()

# Multiple connection objects can be created to different data sources.
# Each connection is independent, so that any action on a connection
# will not affect another connection.
# 
# c2 = Connect("test2")
# c3 = Connect("test3")
# ...
