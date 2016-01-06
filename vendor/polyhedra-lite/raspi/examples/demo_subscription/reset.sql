-------------------------------------------------------------------------------
--                      P O L Y H E D R A    D E M O
--                  Copyright (C) 2004-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : reset.sql
-- 	Description   : integrated sql for setting up the database schema for the demo.
-- 	Author        : Don More
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate the use of a database as the arbitrator in a fault-tolerant 
-- configuration. It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-------------------------------------------------------------------------------

-- pick up the 'standard' currency table definitions.
include '../demo_4/init/tables';
include '../demo_4/init/data';

-- save regional databases.
save into 'london.dat';
save into 'tokyo.dat';
save into 'shanghai.dat';

-- Now create a subscribing database.

-- Tables to control the subscriptions.
-- Note that column market_name an application-specific extra.
CREATE TABLE JournalSession
(
	Id				INTEGER PRIMARY KEY,
	Service				LARGE VARCHAR UNIQUE,
	Enable				BOOL DEFAULT FALSE NOT NULL,
	Status				INTEGER,
	Error_Text			LARGE VARCHAR,
	Current_Service			LARGE VARCHAR,
	Connect_Count			INTEGER,
	Connect_Interval		INTEGER,
	Connect_Timeout			INTEGER,
	Heartbeat_Interval		INTEGER,
	Heartbeat_Timeout		INTEGER,
	Load_File_Timestamp		DATETIME,
	Server_Timestamp		DATETIME,
	PERSISTENT
);

CREATE TABLE JournalSubscription
(
	Session				INTEGER,
	Source_Table_Name		LARGE VARCHAR NOT NULL,
	Destination_Table_Name		LARGE VARCHAR,
	Destination_Column_Names	LARGE VARCHAR,
	Id_Column_Name			LARGE VARCHAR,
	Source_Transaction_Number	INTEGER64,
	PRIMARY KEY (Session, Source_Table_Name),
	FOREIGN KEY (Session) REFERENCES JournalSession (Id),
	PERSISTENT
);

-- Ensure currency table is empty on startup.
delete from currency;
commit;

-- Data to define subscription. Since the table is persistent and
-- enable is set, the subscription will be activated on database
-- start.
insert into journalsession (id,service) values (1,'8011');
insert into journalsubscription (session,source_table_name) values (1,'currency');
update journalsession set enable = true where id = 1;
commit;

save into 'db1.dat';

-- Now create a central database to aggregate multiple subscriptions.
-- Table that will contain an aggregation of regional data.
drop table currency;
create table currency (transient,
	code		large varchar not null,
	market_id	integer not null,
	country	large varchar,
	name		large varchar,
	usdollar	real,
	primary key(code,market_id))
;

alter table journalsession add market_name LARGE VARCHAR;

-- Set up data so that the subscriptions will come up on start-up.
delete from journalsubscription;
delete from journalsession;
insert into journalsession(id,service,market_name) values(1,'8011','London');
insert into journalsession(id,service,market_name) values(2,'8012','Tokyo');
insert into journalsession(id,service,market_name) values(3,'8013','Shanghai');
insert into journalsubscription(session,source_table_name,id_column_name) values (1,'currency','market_id');
insert into journalsubscription(session,source_table_name,id_column_name) values (2,'currency','market_id');
insert into journalsubscription(session,source_table_name,id_column_name) values (3,'currency','market_id');
update journalsession set enable = true where id in (1,2,3);
commit;

save into 'db2.dat';

shutdown;

-------------------------------------------------------------------------------
--			e n d   o f   f i l e				     --
-------------------------------------------------------------------------------
