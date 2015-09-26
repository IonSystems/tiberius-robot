--
--	POLYHEDRA DEMO SUITE
--	Copyright (C) 2000-2014 by Enea Software AB
--
--	sensible.sql
--
--	Initial values of the usdollar column
--	for the persistence demo.
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

update trans_currency set usdollar = 0.67  where code = 'GBP';
update trans_currency set usdollar = 0.81  where code = 'EUR';
update trans_currency set usdollar = 1.67  where code = 'CHF';
update trans_currency set usdollar = 1.49  where code = 'CAD';
update trans_currency set usdollar = 1.72  where code = 'AUD';
update trans_currency set usdollar = 109.5 where code = 'JPY';
commit;
