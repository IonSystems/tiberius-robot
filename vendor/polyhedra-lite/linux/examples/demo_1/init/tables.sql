--
--	POLYHEDRA DEMO SUITE
--	Copyright (C) 2000-2015 by Enea Software AB
--
--	tables.sql
--
--	Definition of schema for demo 1
--	basic currency table
--
------------------------------------------
--
--	v1.0	Dave Stow
--

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

create schema

create table currency (persistent,
	code		large varchar primary key,
	country	large varchar,
	name		large varchar,
	usdollar	real)

;
