-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : query.sql
-- 	Description   : define basic query tables for use in many demos.
-- 	Author        : Nigel Day
--
--      CVSID         : $Id: query.sql,v 1.8 2014/01/06 14:49:01 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------     


-------------------------------------------------------------------------------
--	The auto_id table can be used as a base for any tables requiring an 
--	automatically assigned primary key
-------------------------------------------------------------------------------

create table auto_id
(  persistent
,  id		integer not null primary key
,  nextid		integer shared hidden
);

-------------------------------------------------------------------------------
--	The auto-id_timer table is used as a base for any timers requiring an 
--	automatically assigned primary key
-------------------------------------------------------------------------------

create table auto_id_timer

(  persistent
,  derived from	timer
,  nextid		integer		shared hidden
);

-------------------------------------------------------------------------------
-- set up MyDataservice and QueryObject, one to handle connections and the
-- other to handle establishment and re-establishment of queries depending
-- primarily on the health of the connection.
-- QueryObject is abstract; derive your own, useful(?) classes from it.
-------------------------------------------------------------------------------

create schema

create table dataservice_timer

(  persistent
,  derived from auto_id_timer
,  Service		large varchar		references MyDataService
)

create table MyDataservice

(  persistent
,  derived FROM Dataservice
,  mytimer INTEGER              references dataservice_timer
,  Queries ARRAY OF QueryObject 
,  Disable BOOL                 
)

create table QueryObject

(  persistent
,  derived from	auto_id
,  Service	   LARGE VARCHAR not null references MyDataservice
,  Disable      BOOL
);


-------------------------------------------------------------------------------
--                           E n d   o f   F i l e
-------------------------------------------------------------------------------
