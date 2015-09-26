-------------------------------------------------------------------------------
--                       P O L Y H E D R A    D E M O
--                   Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : query.cl
-- 	Description   : methods for tables that handle the donkey work of
--			establishing connections and active queries from the DB
-- 	Author        : Nigel Day
--
--      CVSID         : $Id: query.cl,v 1.8 2014/01/06 14:49:01 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------     


--------------
script auto_id
--------------

	on  create
		if id = 0 then
			add 1  to nextid
			set id to nextid
		end if
	end create

----------
end script
----------


--------------------
script auto_id_timer
--------------------

	on  create
		--
		-- give this object an ID that does not clas with any other
		-- object in this table (or its superclass)
		local reference timer t

		while id = 0
			add 1  to nextid
			locate timer (id=nextid) into t
			if not exists t then set id to nextid
		end while
	end create

----------
end script
----------


------------------------
script dataservice_timer
------------------------

	on  create
		Activate ()
	end create

	on  delete
		if exists Service then forget MyTimer of Service
	end delete

	on  set Counter
		if IsOpen of Service or Disable of Service then
			set Interval to 3
			--set Active   to false
		else
			if Interval < 60 then add 1 to Interval
			debug "trying to open connection to" && name of service
			Open () of Service
		end if
	end set Counter

	on  Activate
		--
		-- called on creation AND when the rtrdb restarts.
		--
		debug "timer for" && name of service && "restarted"
		set TickTime   to 1000000
		set Interval   to 1
		set Continuous to true
		set Active     to true
		Close () of service
	end Activate		

----------
end script
----------


--------------------
script MyDataservice
--------------------

	on  create
		create Dataservice_timer (id=0, service=me) into MyTimer
	end create

	on delete
		if exists MyTimer then delete MyTimer
	end delete

	on  set IsOpen
		--
		-- if true:
		-- go round finding the client query objects and prod
		-- them to re-establish themselves.
		--
		-- if false:
		-- in theory, we could take this opportunity to close
		-- the various queries that use this data service. In 
		-- practice, this has two problems... first, we have no
		-- way of closing a query other than by deleting the
		-- owner or closing the connection, and, secondly, IsOpen
		-- is set false AFTER the queries have been terminated!
		--
		local reference QueryObject q

		if IsOpen then
			debug "connection to" && name && "opened."
			if disable then
				Close ()
			else
				foreach q in Queries
					if not disable of q then emit "LinkMe" to q
				end foreach
			end if
		else
			debug "connection to" && name && "closed."
			if exists MyTimer and not disable then set active of MyTimer to true

			foreach q in Queries
				Closed () of q
			end foreach
			
		end if
	end set IsOpen

	on  set disable
		if exists MyTimer then set active of MyTimer to not disable
		if disable and IsOpen then Close ()
	end set disable

----------
end script
----------


------------------
script QueryObject
------------------

	on  create
		if exists Service then insert me into Queries of Service
		if exists service and not disable then
			if IsOpen of service then emit "LinkMe" to me
		end if
	end create

	on  delete
		if exists Service then remove me from Queries of Service
	end delete

	on  set Service
		if exists Old Service then remove me from Queries of Old Service
		if exists Service     then insert me into Queries of Service
	end set Service

	on  set disable
		if exists service then
			if IsOpen of service then 
				if disable then
					send UnlinkMe () to me
				else
					emit "LinkMe" to me
				end if
			end if
		end if
	end set disable

	on  LinkMe
		--
		-- redefine as needed in subclasses. assuming the derived class
		-- has, say, an array attribute called objects, the redefined
		-- version of this handler might simply consist of a single
		-- statement, 'link objects with sql"..."'
		--
	end LinkMe
	
	on  UnlinkMe
		--
		-- redefine as needed in subclasses. assuming the derived class
		-- has, say, an array attribute called objects, the redefined
		-- version of this handler might simply consist of a single
		-- statement, 'unlink objects'
		--
	end UnlinkMe	

	on  Closed
		--
		-- the link has closed: tidy up!
		--
		-- redefine as needed in subclasses. Often, nothing may need
		-- to be done.
		--
	end Closed

----------
end script
----------


-------------------------------------------------------------------------------
--			e n d   o f   f i l e
-------------------------------------------------------------------------------
