-----------------------------------------------------------
-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : readme.txt
--    Description   : description of what's in the examples directory.
--    Author        : Nigel Day
--
--
--    Please note the important caveat incorporated at the end of this document
-------------------------------------------------------------------------------


As well as the demo directories referred to in the Polyhedra
Evaluation Guide (eg, demo_1, demo_2, ...  demo_5, demo_websocket)
this directory also contains (in the directory called clients) the
source code of the example client applications that are provided as
executables in the evaluation kits and in some of the release kits.
The client applications are coded to use the callback API, but the
source code of equivalent versions using the ODBC API (and in some
cases, the JDBC API) are also provided.  In most cases, it is expected
that customers will use the ODBC API for their C or C++ applications,
as it is usually faster if used correctly.

Further examples are occasionally added to this directory, each in its own 
directory and described in a text file within that directory.  In most 
cases, the example applications will build on that used in demo_1 to 
demo_5, to allow the standard client executables to be used to animate and 
monitor the additional examples.  At present, the extra examples (in 
alphabetical order) are as follows: 

* demo_db_arb shows how a third database can be used as an arbitrator for 
a fault-tolerant system.  Includes sample CL code for controlling the 
arbitrator database.  

* demo_db_db_queries provides sample table structures and associated
CL code whereby one database can connect to another database and set
up active quries on it.  The application contains more code than the
bare minimum needed to implement the specified functionality, as it is
fairly general-purpose; it can be used to launch queries on many
databases, and can readily be adapted to launch a number of different
queries on each database.

* demo_global_fn provides some useful CL-coded global functions, which can 
be used in any CL script attached to a database.  

* demo_historian shows how the Polyhedra historian submodule can be
set up to log 'samples' recording the past state of data points in the
database, and showing how sample data can be retrieved (for display on
a trend diagram, say).

* demo_replica contains a poly.cfg file that sets up read-only replicas of 
a fault-tolerant pair of servers.  

* demo_runner shows how a CL-coded application (run using the CLC bytecode 
engine) can be used on a Windows, Linux or Unix-based workstation or 
server to run and control a Polyhedra server and associated client 
applications.  (On an embedded platform such as OSE or VxWorks, the server 
is more typically invoked through a function interface rather than a 
command-line interface, so it is more common to control the application 
from a C or C++ application.) 

* demo_shrink_db gives sample code that can be used to 'shrink' the size 
of a saved database file when journalling means it has got too big.  

* demo_singleton shows how one can set up a table that will only ever have 
one record, and gives CL that not only enforces the contraint that there 
is just one record but also set up a CL global contant that points at the 
unique record in theis table, to allow ready access to the record from all 
other CL that may be attached to the database.  

* demo_subscription shows how the contents of a table can be subscribed
from one database into another such that changes are automatically
sent to the subscribing database. The example also shows how data can
be aggregated from multiple databases into one table in another
database.

See the readme files for each example for more details and instructions on 
running them.  Suggestions for further examples welcomed, as are 
contributions!  


-------------------------------------------------------------------------------


AN IMPORTANT CAVEAT: 

Examples provided in the various subdirectories are all ILLUSTRATIVE CODE, 
provided on an 'as is' basis to help demonstrate the use of Polyhedra.  
Permission is hereby granted for licensed users of Polyhedra to adapt the 
code and use it as needed in their Polyhedra-based applications, provided 
that Enea Software AB (and any other author mentioned in the readme files of 
the examples you use) is acknowledged in the source of your application, 
and that users are aware that neither Enea Software AB, its agents and 
distributors nor (in the case of submitted contributions) the original 
authors warrant this code in any way.  

Customers are encouraged to submit their own 'tips and tricks' for 
inclusion in this directory for the benefit of the Polyhedra user 
community.  Please indicate whether you want to be identified as the 
contributor, or whether you prefer to remain anonymous.  When submitting 
examples for inclusion in this directory, please confirm that you are 
transferring ownership to Enea and that you are happy for them to made 
available to other Polyhedra users under the terms and conditions outlined 
above.  We reserve the right to decide whether or not to publish such 
contributions, and the right to modify them as we see fit.  


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------
