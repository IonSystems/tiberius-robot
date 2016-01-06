-------------------------------------------------------------------------------
--                             P O L Y H E D R A
--                Copyright (C) 2006-2015 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : readme.txt
--    Description   : Polyhedra unixODBC installation guide.
--
--
-------------------------------------------------------------------------------

This installation kit contains the Polyhedra unixODBC driver and setup library.

Before the driver can be used, the driver and library must be registered.
The registration can be performed in the following way, assuming that unixODBC
has already been installed:

1. Copy the file libpolyod32.so from this kit to an appropriate directory,
   e.g. /usr/local/lib

2. Edit the Driver and Setup lines in the odbcinst.ini file to agree with
   step 1.

3. As root, execute "odbcinst -i -d -f odbcinst.ini"

You may then configure data sources to use the drivers using the ODBCConfig GUI
application supplied as part of unixODBC.

-------------------------------------------------------------------------------
--                                End of File
-------------------------------------------------------------------------------
