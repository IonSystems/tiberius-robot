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


insert into currency values ('GBP','UK','Pound',0.67);
insert into currency values ('EUR','Eurozone','Euro',0.81);
insert into currency values ('CHF','Switzerland','Franc',1.67);
insert into currency values ('CAD','Canada','Dollar',1.49);
insert into currency values ('AUD','Australia','Dollar',1.72);
insert into currency values ('JPY','Japan','Yen',109.5);
commit;

save into 'test.dat';

-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

