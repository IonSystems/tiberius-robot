--
--	POLYHEDRA DEMO SUITE
--	Copyright (C) 2000-2014 by Enea Software AB
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

--------------Insert initial data for tiberius_status table----------------------

insert into tiberius_status values ('AU1',AUTONOMY_START' ,0);
insert into tiberius_status values ('AU2',AUTONOMY_STOP'  ,1);  
insert into tiberius_status values ('AU3',AUTONOMY_PAUSE' ,0);
insert into tiberius_status values ('MA1',MANUAL_START'   ,0);
insert into tiberius_status values ('MA2',MANUAL_STOP'    ,0);

insert into object_existence values('OBJ1','HEXAGON', 0)
insert into object_existence values('OBJ2','STAR'   , 0)
insert into object_existence values('OBJ3','CUBE'   , 0)
insert into object_existence values('OBJ4','NONE'   , 1)

commit;



commit;

