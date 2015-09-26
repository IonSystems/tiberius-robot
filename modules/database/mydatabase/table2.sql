create schema

create table detect_object 
        (persistent,
	OBJECTS		large varchar primary key,
	SIMILARITY 	real)
;