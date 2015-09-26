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


insert into tiberius_status values ('AM','AUTONOMY_MODE' ,'FALSE');
insert into tiberius_status values ('IM','IDLE_MODE'     ,'TRUE');  
insert into tiberius_status values ('MM','MANUAL_MODE'   ,'FALSE');


--------------Insert initial data for object_similarity table----------------------

insert into object_similarity values('OBJ1','CUBE'	, 'NULL');
insert into object_similarity values('OBJ2','HEXAGON'   , 'NULL');
insert into object_similarity values('OBJ3','STAR'      , 'NULL');


--------------Insert initial data for mission_parameters table----------------------

insert into mission_parameters values('LONG'  ,  'LONGITUDE'        , '0.000000');
insert into mission_parameters values('LAT'   ,  'LATITUDE'         , '0.000000');
insert into mission_parameters values('SELOBJ',  'SELECTED_OBJECT'  , 'NONE');

--------------Insert initial data for mission_status table----------------------

insert into mission_status values('ST0','MISSION_START'        ,'FALSE','N/A');
insert into mission_status values('ST1','NAVIGATING'           ,'FALSE','N/A');
insert into mission_status values('ST2','DESTINATION_REACHED'  ,'FALSE','N/A');
insert into mission_status values('ST3','SCANNING_OBJECTS'     ,'FALSE','N/A');
insert into mission_status values('ST4','ANALYSING_IMAGE'      ,'FALSE','N/A');
insert into mission_status values('ST5','OBJECT_DETECTED'      ,'FALSE','N/A');
insert into mission_status values('ST6','MISSION_FINISHED'     ,'TRUE','N/A');
insert into mission_status values('ST7','MISSION_PAUSED'       ,'N/A','FALSE');
commit;

insert into LIDAR_data values('LD0','0');
insert into LIDAR_data values('LD1','0');
insert into LIDAR_data values('LD2','0');
insert into LIDAR_data values('LD3','0');
insert into LIDAR_data values('LD4','0');
insert into LIDAR_data values('LD5','0');
insert into LIDAR_data values('LD6','0');
insert into LIDAR_data values('LD7','0');
insert into LIDAR_data values('LD8','0');
insert into LIDAR_data values('LD9','0');
insert into LIDAR_data values('LD10','0');
insert into LIDAR_data values('LD11','0');
insert into LIDAR_data values('LD12','0');
insert into LIDAR_data values('LD13','0');
insert into LIDAR_data values('LD14','0');
insert into LIDAR_data values('LD15','0');
insert into LIDAR_data values('LD16','0');
insert into LIDAR_data values('LD17','0');
insert into LIDAR_data values('LD18','0');
insert into LIDAR_data values('LD19','0');
insert into LIDAR_data values('LD20','0');
insert into LIDAR_data values('LD21','0');
insert into LIDAR_data values('LD22','0');
insert into LIDAR_data values('LD23','0');
insert into LIDAR_data values('LD24','0');
insert into LIDAR_data values('LD25','0');








