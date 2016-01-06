-------------------------------------------------------------------------------
--                      P O L Y H E D R A   D E M O
--                 Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : tables.sql
-- 	Description   : sql to initialise the client database for the demo.
-- 	Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- include some useful tables that will assist in applications
-- that may be launching multiple active queries onto
-- multiple databases.

INCLUDE 'query.sql';

-- define a currency table, essentially the same as in the
-- demo_1 database except that it will be TRANSIENT and LOCAL

create table currency

(  transient, local

,  code     LARGE VARCHAR primary key
,  country  LARGE VARCHAR
,  name	   LARGE VARCHAR
,  usdollar REAL
);

-- define the table that will specify that we will be populating
-- our local currency table by means of a query on the remote
-- currency table.

create table Currency_Query

( 	derived from QueryObject
,	objs         array of currency transient local
);

-- define a table that will allow us to track whether a currency
-- object is being created by a user transaction or by a
-- transaction set off by the system to record the results of 
-- an active query. (the existence of a table called dataconnection,
-- with the appropriate attribute definitions


create table dataConnection

(  local
,  transient
,  id          INTEGER primary key
,  machine     INTEGER 
,  client_Type	LARGE VARCHAR 
,  env	      LARGE VARCHAR 

-- (if we are using the user-based security feature of Polyhedra,
--  then the dataconnection table can point at the relevant record
--  in the 'users' table for the current user. Not relevant in 
--  this particular app.)
--, username   large varchar references users
);


-------------------------------------------------------------------------------
--	                        E n d   o f   F i l e
-------------------------------------------------------------------------------

