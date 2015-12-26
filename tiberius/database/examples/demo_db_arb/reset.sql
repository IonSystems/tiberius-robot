-------------------------------------------------------------------------------
--                      P O L Y H E D R A    D E M O
--                  Copyright (C) 2004-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : reset.sql
-- 	Description   : integrated sql for setting up the database schema for the demo.
-- 	Author        : Don More
--
--    CVSID         : $Id: reset.sql,v 1.8 2014/01/06 14:49:01 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate the use of a database as the arbitrator in a fault-tolerant 
-- configuration. It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- use dba.sql to set up dba.dat as the arbitrator database,
-- tidying up afterwards.

include 'dba';

-------------------------------------------------------------------------------

-- pick up the 'standard' currency_limits table definitions.
include '../demo_5/init/tables';
save into 'test.dat';

include '../demo_5/init/data';

save into 'logdir1/test.dat';
save into 'logdir2/test.dat';
shutdown;


-------------------------------------------------------------------------------
--			e n d   o f   f i l e				     --
-------------------------------------------------------------------------------

