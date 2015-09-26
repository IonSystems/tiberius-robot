-------------------------------------------------------------------------------
--                      P O L Y H E D R A   D E M O
--                 Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : tables.sql
-- 	Description   : sql for setting up the database schema for the demo.
-- 	Author        : Nigel Day
--
--    CVSID         : $Id: tables.sql,v 1.9 2014/01/06 14:49:02 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

-- add the 'standard' table used in many examples,
-- so that the animator, etc can make lots of changes

CREATE TABLE currency 
   ( persistent
	, code	  LARGE VARCHAR primary key
	, country  LARGE VARCHAR
	, name	  LARGE VARCHAR
	, usdollar REAL
   );

-- create a table to hold info re snapshot state

CREATE TABLE snapshot_info
   ( persistent
   , id          INTEGER primary key
   , target_size INTEGER
   , saving      BOOL    transient
   , max_size    INTEGER transient
   , min_size    INTEGER transient
   );

INSERT INTO snapshot_info 
      (id, target_size) VALUES (1, 10000);
COMMIT;


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

