-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : setup.sql
-- 	Description   : data to set up the historian to log
--                    changes to the basic currency table
-- 	Author        : Nigel Day
--
--      CVSID         : $Id: setup.sql,v 1.9 2014/01/06 14:49:02 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------     


-- sample the currency table every 5 seconds, using the
-- code field to identify the samples; we are not specifying
-- an enable column or a time stamp column, so all records
-- will be monitored and timestamps automatically generated.
-- The enable attribute is set to FALSE to prevent any data collection at
-- initialisation stage; collection starts when the database is 
-- restarted in the parent directory

insert into logcontrol (id, source,     namecolumn, enable, rate)
		values           (1,  'currency', 'code',     false,   5);

-- which columns to monitor? in this case, just the usdollar.

insert into logcolumn (type, control, name,       sourcecolumn)
		          values (0,   1,       'usdollar', 'usdollar');

-- when creating time-compressed samples, record the min, max
-- and average values for each time period. The 'type' value
-- determines what kind of tim-compression is to be done to
-- generate the relevant value for the sample. The order of 
-- inserts below affects the order of columns when
-- time-compressed data is retrieved with a 'select *' query.

insert into logcolumn (control, name,  type, sourcecolumn)
               values (1,       'min', 7,    'usdollar');
insert into logcolumn (control, name,  type, sourcecolumn)
	            values (1,       'avg', 8,    'usdollar');
insert into logcolumn (control, name,  type, sourcecolumn)
               values (1,       'max', 6,    'usdollar');

-- log 'raw' samples using using a file divided into
-- 10 buckets of 1K bytes (so the file will be 10K long,
-- plus a bit of room for indexing information). In
-- practice, one would choose a much larger buffer size,
-- but we want to be able to demonstrate that they are
-- being used circularly, without having to wait for too
-- long!

insert into logdata(rate,fedfromrate,control,buffercount,buffersize,directory)
		values ('0s', NULL, 1, 10, 1000, '.');

-- a further 10K is to be used for time-compressed samples
-- with 1-minute intervals, and another 40K for 5-minute
-- samples; the 5-minute samples are to be generated from
-- the 1-minute samples rather than from the raw samples.

insert into logdata(rate,   control, buffersize, buffercount)
	         values ( '60s', 1,       2000,        5);
insert into logdata(rate,   control, buffersize, buffercount, fedfromrate)
            values ('300s', 1,       2000,       20,          '60s');

-- (with these figures and 6 records in the currency table,
-- there is room for about 700 (approx 12 minutes) of raw
-- samples, about an hour of 1-minute samples, and about a
-- day of 5-minute samples. If the raw data rate has been
-- left unspecified when creating the logcontrol record,
-- all logging would have been 'on change', and so the
-- timespan covered by the raw log file would depend on
-- the average rate of data change.) 

commit;

-- set up a pseudo-table called 'sample' that can be used
-- to retrieve the raw samples, and another called csample
-- that can be used to retrieve time-compressed samples; 
-- when retrieving from the latter, one will have to 
-- specify the granularity with a clause such as 'where 
-- granularity='60s'.

update logcontrol set raw='sample',compressed='csample' where id=1;
commit;


-------------------------------------------------------------------------------
--                        E n d   o f   F i l e
-------------------------------------------------------------------------------

