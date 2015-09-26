-------------------------------------------------------------------------------
--			 P O L Y H E D R A    D E M O
--	 	     Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : db.cl
-- 	Description   : scripts to animate the database
-- 	Author        : Nigel Day
--
--	CVSID         : $Id: db.cl,v 1.8 2014/01/06 14:49:02 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


---------------------------------------------------
-- define a pointer to the unique singleton object,
-- initialised whenever the database restarts.
---------------------------------------------------

constant reference Singleton Singleton_object = Find_Singleton ()

function Singleton Find_Singleton
        --
	-- whilst of course this function can be invoked by any method
	-- attached to this database, it is intended ONLY for use in 
	-- initialising the above constant; other methods can simply 
	-- use the singleton_object global function whenever they need
	-- to access an attribute or method of the singleton object
	--
 	local reference Singleton obj
	locate singleton (id=1) into obj
	if not exists obj then
                debug "APPLICATION ERROR:\n\tSingleton not found"
                quit
        end if	
	return obj 
	
end Find_Singleton


----------------
script singleton
----------------

	-- let use enforce the singleton nature of this class

	on  create
		abort transaction "you should have only one object in singleton."
	end create

	on  delete
		abort transaction "you must not delete the singleton object."
	end delete

	on  activate
		--
		-- put code here that is to run EVERY TIME the database
		-- starts up!
		--
	end activate
	
	-- add a sample method:
	-- methods on other tables will be able to use
	--
	--           next_integer () of singleton_object
	--
	-- to obtain a unique value (well, unique until wrap-round
	-- occurs, after 2**32 calls of the function!
	
	function integer next_integer 
		--
		add 1 to nextid
		return nextid
	end next_integer 

----------
end script
----------


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------
