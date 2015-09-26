-------------------------------------------------------------------------------
--                      P O L Y H E D R A    D E M O
--                  Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : tables.sql
-- 	Description   : sql for setting up the database schema for the demo.
-- 	Author        : Nigel Day
--
--    CVSID         : $Id: tables.sql,v 1.8 2014/01/06 14:49:02 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

  

create table singleton

-- there should be precisely one of these objects - thats the point of the
-- demo!

(	persistent
,	id integer primary key

-- add an attribute which we will use when illustrating how the singleton 
-- can be used

,  nextid integer default 0

);

-- create the object NOW, whilst no CL is running.

insert into singleton (id) values (1); commit;


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

