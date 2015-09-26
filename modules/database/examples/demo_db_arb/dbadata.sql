-------------------------------------------------------------------------------
--                         P O L Y H E D R A    D E M O
--	 	       Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : dbadata.sql
--    Description   : sql for populating jcpcontrol for the arbitrator db.
--    Author        : Nigel Day
--
--    CVSID         : $Id: dbadata.sql,v 1.8 2014/01/06 14:49:01 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


insert into jcpcontrol ( name, heartbeat_interval, switchover_delay
                       , active, preferredServer, recovery_time
		                 )
		values ( '9201', milliseconds (200), 100*1000, true, true, seconds (20));

insert into jcpcontrol ( name, heartbeat_interval, switchover_delay
                       , active, preferredServer, partner
                       )
      values ( '9202', milliseconds (200), 100*1000, false, false, '9201');

update jcpcontrol set partner='9202' where name='9201';

commit;


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

