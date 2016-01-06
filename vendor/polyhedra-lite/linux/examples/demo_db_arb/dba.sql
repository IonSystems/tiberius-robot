-------------------------------------------------------------------------------
--                         P O L Y H E D R A   D E M O
--                    Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : dba.sql
--    Description   : sql for setting up a jcpcontrol table.
--
--			this includes 'dbadata.sql' to populate jcpcontrol,
--			saves the database in dba.dat and then drops tables; 
--			consequently, it can be used with the 'standard' init 
--			sequences by including this file from within the 
--			application's tables.sql file.
--
--    Author        : Nigel Day
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

-- set up dba.dat as the arbitrator database, tidying up afterwards.

create table dataConnection
(	local
,       transient
,	id          integer primary key
,	machine	   integer
,	client_Type	large varchar
,	env         large varchar
);

-- We use this derivation of dataconnection to avoid a warning regarding
-- saving CL in the database file.
create table mydataconnection(derived from dataconnection);

create table jcpcontrol
(	persistent

   -- required attributes, on which the FT databases will
   -- be launching an active query

,	name                    large varchar    primary key

,	active                  bool     transient
,	heartbeat_interval      datetime
,	heartbeat               datetime transient
,	transaction_no          integer  transient

	-- extra attributes, not used by the FT databases, just by the
	-- CL running in the arbitrator.

,	partner                 large varchar references jcpcontrol
,	preferredserver         bool	         -- treat this server as preferred?
,	recovery_time           datetime       -- flip to preferred after this time
,	switchover_delay        integer        -- settle time on switch-over

,	watchdog_running        bool transient -- for CL use only
,  idle_count              int transient  -- ditto
,  connection              int transient  -- ditto
);


-- populate the table with an entry for each jcp.

include 'dbadata';

save into 'dba.dat';


-- tidy up... the jcpcontrol table is not used by the other databases for which
-- we may be about to construct the schema.

update jcpcontrol set partner = null; commit;
drop table jcpcontrol;
drop table mydataconnection;
drop table dataconnection;


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

