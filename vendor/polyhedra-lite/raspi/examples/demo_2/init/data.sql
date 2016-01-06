--
--	POLYHEDRA DEMO SUITE
--	Copyright (C) 2000-2015 by Enea Software AB
--
--	data.sql
--
--	Initial data for basic currency demo
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

insert into currency values ('GBP','UK','Pound',0.67);
insert into currency values ('EUR','Eurozone','Euro',0.81);
insert into currency values ('CHF','Switzerland','Franc',1.67);
commit;

insert into currency_limits values ('CAD','Canada','Dollar',1.49,1.4,1.6);
insert into currency_limits values ('AUD','Australia','Dollar',1.72,1.6,1.85);
insert into currency_limits values ('JPY','Japan','Yen',109.5,102,117);
commit;



