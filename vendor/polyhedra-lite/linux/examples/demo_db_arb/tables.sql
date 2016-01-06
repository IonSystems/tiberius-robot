-------------------------------------------------------------------------------
--                      P O L Y H E D R A    D E M O
--                  Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : tables.sql
-- 	Description   : sql for setting up the database schema for the demo.
-- 	Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- use dba.sql to set up dba.dat as the arbitrator database,
-- tidying up afterwards.

include 'dba';


-------------------------------------------------------------------------------


-- pick up the 'standard' currency_limits table definitions.

include '../demo_5/init/tables';

save into 'test.dat';
shutdown;

  
-------------------------------------------------------------------------------
--                        E n d   o f   F i l e
-------------------------------------------------------------------------------

