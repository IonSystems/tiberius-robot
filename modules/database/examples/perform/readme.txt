-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : readme.txt
--    Description   : Description of the performance demonstration clients
--    Author        : Don More
--
--    CVSID         : $Id: readme.txt,v 1.13 2014/02/19 16:27:02 chrism Exp $
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


INTRODUCTION

The perform client illustrates the performance of Polyhedra. 
The client uses one of the client Application Programming Interfaces supported by Polyhedra:

a C++ program using the ODBC API can be built in the directory examples/clients/perform/odbc 
a C++ program using the Callback API can be built in the directory examples/clients/perform/callback
a java program using the JDBC API is provided in directory examples/clients/perform/jdbc

All of these programs run the same timed tests, an explanation of which can be found in perform.htm


BUILDING THE CLIENTS

The ODBC API version of the client is already built.

The JDBC API client should be compiled and run with respect to the
polyclasses.jar file.

To rebuild the C++ clients, go to the callback or odbc directory in
examples/clients/perform and follow the appropriate client linking instructions
(linking-odbc-client.txt or linking-callback-client.txt) in the platform doc
directory.

With Microsoft Visual Studio on Windows:

for the ODBC API version:
cl /O2 /nologo -DWIN32 -I .. -I..\..\..\..\include perform.cxx /link -subsystem:console -out:perform.exe /libpath:..\..\..\..\win32\i386\msvc\lib polyod32.lib pat.lib patmem.lib ws2_32.lib

and for the Callback API version:
cl /O2 /nologo -DWIN32 -I .. -I..\..\..\..\include perform.cxx /link -subsystem:console -out:perform.exe /libpath:..\..\..\..\win32\i386\msvc\lib patapp.lib pat.lib patmem.lib ws2_32.lib

RUNNING THE DEMONSTRATIONS

The clients connect to an already-running database, and assume by
default they are to use one running on the same machine as the client,
via port 8001. The client create and drop tables as needed, so you can
either just start, say, the demo_1 database, or you can fire off an
empty database from this directory, using the command
 
   rtrdb empty &
 
... if running on a Linux or Unix platform, or
 
   start rtrdb empty
 
... if running on Windows.

The ODBC and Callback API versions of the client are run thus:

perform [<dsn>] [<opcount>] [<inter-test_delay>]

<dsn> - the service to connect to (default 8001)
<opcount> - number of operations - larger will make test longer (default 1000)
<inter-test delay> - seconds to delay the start of the test sequence
seconds, to allow the db to stabilise if it has just been started up,
say; and, put a delay of 1 second between tests, to ensure database
has settled down from previous activity.

The JDBC API version is run thus:

jdbcapi -classpath .;polyclasses.jar jdbcapi [<port>] [<username>] [<password>]

<port> - service on which database runs on (default 8001)
<user> - username if required to access service.
<password> - password if required to access service.

------ FILES: ------ 

poly.cfg - config file for the supporting database
perform.htm - description of the tests performed

-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------
