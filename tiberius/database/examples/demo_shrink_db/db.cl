-------------------------------------------------------------------------------
--			 P O L Y H E D R A    D E M O
--	 	     Copyright (C) 2005-2014 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : db.cl
-- 	Description   : code to shrink the database save file if it gets too big
-- 	Author        : Nigel Day
--
--      CVSID         : $Id: db.cl,v 1.8 2014/01/06 14:49:02 andy Exp $
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


----------------------------------------------------------
-- define a pointer to the unique snapshot_info object,
-- initialised whenever the database restarts.
----------------------------------------------------------

constant reference snapshot_info snapshot_info_object = Find_snapshot_info ()

function snapshot_info Find_snapshot_info
        --
	-- whilst of course this function can be invoked by any method
	-- attached to this database, it is intended ONLY for use in 
	-- initialising the above constant; other methods can simply 
	-- use the snapshot_info_object global function whenever they need
	-- to access an attribute or method of the snapshot_info object
	--
 	local reference snapshot_info obj
	locate snapshot_info (id=1) into obj
	if not exists obj then
                debug "APPLICATION ERROR:\n\tsnapshot_info not found"
                quit
        end if	
	return obj 
	
end Find_snapshot_info



-------------------------------
-- the scripts that do the work
-------------------------------


script journalcontrol

	-- set up a method to be triggered whenever the 
	-- file_size attribute is changed.
	
	on  set file_size
		--
		local integer size = file_size
		
		if disable then exit -- do nothing if not journalling
		
		-- some code to keep track of min/max file sizes,
		-- out of interest
		
		if size > max_size of snapshot_info_object then 
			set max_size of snapshot_info_object to file_size
		else if size > 0 and \
		            (size < min_size of snapshot_info_object \
			    or min_size of snapshot_info_object= null) then 
			set min_size of snapshot_info_object to size   
		end if
		
		-- do we need a new snapshot?
		
		if size > target_size of snapshot_info_object and \
				not saving of snapshot_info_object then
			send save () to me
		end if
		
		-- have we just completed a snapshot? if so, ensure the
		-- target is realistic.
		
		if old file_size = 0 or size< old file_size then
			if old file_size=0 then 
				debug "database file shrunk to" && file_size
			else
				debug "database file shrunk from" && \
					old file_size && "to" && file_size
			end if
			if size > target_size of snapshot_info_object then
				set target_size of snapshot_info_object to \
							(size*11) div 10
			end if 
		end if
	end set file_size 
	
	on  save
		--
		if saving of snapshot_info_object then exit
		set saving of snapshot_info_object to true
		sql "save"
		set saving of snapshot_info_object to false
	end save
	
end script

   
-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

