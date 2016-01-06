-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : db.cl
-- 	Description   : illustrate active queries from the DB (in conjunction
--                      with the CL code in query.cl)   
-- 	Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------     


---------------------
script currency_Query
---------------------

	on activate
	end activate
	
	on  LinkMe
		-- 
		-- this is called when a connection has been established by my
		-- 'service' object
		--
		
		debug "Setting up currency query" && id && "in" && \
			GetResource ("data_service")            && \
			"into" && name of Service
			
		-- ensure the array of currency objects is empty. This should
		-- already be the case, but a lttle paranoia doesn't hurt.
		  
		while exists object 1 of objs
			delete object 1 of objs
		end while
		
		-- now set up the active query
		
		link objs                                          \
			with  sql "select * from currency"        \
			from  service

		debug "Query 1 set up:" && getArraysize (objs) && "records retrieved."
	end LinkMe

	on  UnlinkMe
		--
		-- this is called when a query is disabled.
		--
		unlink objs
		debug "currency query" && id && "now unlinked."
	end UnlinkMe
----------
end script
----------


---------------
script currency
---------------

	on  create
		--
		local reference QueryObject    qo
		local reference Currency_Query cq
		
		if not exists getConnection () then exit
		
		-- the object appears to have been created by a 'user',
		-- not by the active query mechanism. We have a choice:
		--
		-- * we can cause a matching object to be created in the
		--   other database; 
		--
		-- * we can abort the transaction; or,
		--
		-- * we can leave the new currency record alone, in
		--   which case there will be no corresponding record in
		--   any of the queried database(s).
		--
		-- the first option is only meaningful and possible if
		-- we are only querying one remote database, and only 
		-- launching the one active query
		--
		-- to cause a corresponding object to be created in a
		-- remote database, we should add a pointer to this
		-- record into the array of objects managed by the
		-- active query on that database. We would have to 
		-- locate the right Currency_query object, and then
		-- issue a command such as
		--    insert me into objs of cq 
	        
		-- for the moment, take the easy way out:
		
		abort transaction "users are not allowed to insert records" && \
		                  "into the local currency table."  
	end create

----------
end script
----------


-------------------------------------------------------------------------------
--			e n d   o f   f i l e
-------------------------------------------------------------------------------

  
