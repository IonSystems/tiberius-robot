create schema

	create table tiberius_status 
    	 (persistent,
		ID		large varchar primary key,
		STATUS          large varchar, 
                VALUE 	        large varchar)
	

	create table object_similarity
        (persistent,
		ID              large varchar primary key,
                OBJECTS         large varchar,
                SIMILARITY      large varchar)

	
	create table mission_parameters
       (persistent,
		ID               large varchar primary key,
                INFO             large varchar,
                VALUE    	 large varchar)     
	      


	create table mission_status
	(persistent,
		ID			large varchar primary key,
		STATUS		        large varchar,
		VALUE             	large varchar,
		PAUSE_VALUE		large varchar)
		
	create table compass_data
	(transient,
		ID 	 		large varchar primary key,			
	 			     
		INSTANCE	 	large varchar,	
		VALUE			large varchar)
		

		
	create table GPS_data
	(transient,	
		ID			large varchar primary key,
		LATITUDE		large varchar,
		LONGTITUDE		large varchar,	
		INSTANCE	 	large varchar)

        create table RANGEFINDERS_data
	(transient,	
		ID			large varchar primary key,
		FRONT_LEFT		large varchar,
		FRONT_CENTRE		large varchar,	
		FRONT_RIGHT	 	large varchar,
		REAR_LEFT		large varchar,	
		REAR_CENTRE		large varchar,
		REAR_RIGHT		large varchar,
		INSTANCE		large varchar)

	create table LIDAR_data
	(persistent,
		ID 	 		large varchar primary key,			
	 	VALUE			large varchar)



;	