-------------------------------------------------------------------------------
--                             P O L Y H E D R A
--                Copyright (C) 2006-2013 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : readme.txt
--    Description   : Polyhedra unixODBC installation guide.
--    Author        : Don More
--
--    CVSID         : $Id: readme.txt,v 1.7 2013/01/04 10:26:06 andy Exp $
--
-------------------------------------------------------------------------------

This directory contains the Polyhedra unixODBC driver and setup library.

Before the driver can be used, the driver and library must be registered.
The registration can be performed in the following way, assuming that unixODBC
has already been installed:

1. Copy the .so file to an appropriate directory, e.g. /usr/local/lib

2. Edit the Driver and Setup lines in the odbcinst.ini file to agree with
   step 1.

3. As root, execute "odbcinst -i -d -f odbcinst.ini"

You may then configure data sources to use the drivers using the ODBCConfig GUI
application supplied as part of unixODBC.

-------------------------------------------------------------------------------
--                                End of File
-------------------------------------------------------------------------------
