-------------------------------------------------------------------------------
--                        P O L Y H E D R A    D E M O
--                    Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : data.sql
-- 	Description   : sql to create the initial records for the demo.
-- 	Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- let us try deleting the singleton: this should fail!

delete from singleton; commit;

-- now try creating another one... this should also fail.

insert into singleton (id) values (2); commit;


-------------------------------------------------------------------------------
--                           e n d   o f   f i l e
-------------------------------------------------------------------------------

