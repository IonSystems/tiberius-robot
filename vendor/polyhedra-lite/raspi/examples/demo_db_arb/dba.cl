-------------------------------------------------------------------------------
--			P O L Y H E D R A   D E M O
--	 	   Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
--      Filename      : dba.cl
--      Description   : Arbitrator script
--      Author        : Andy England, Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product. 
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- how many heartbeats should one wait before closing down the standby because
-- it seems out of step with the master?

constant integer idle_limit = 5


-- set the following boolean to TRUE if wanting to test auto-stop of standby
-- when it seems as if its connection to the master is lost; if set, the code
-- will assume the connection always gives trouble once the standby has loaded
-- its snapshot.

constant boolean test_code_for_stopping_standby = FALSE


-- We use mydataconnection so that we can attach CL to dataconnection.
-- This mechanism (see dataconnection_class in poly.cfg) allows for the
-- CL to be saved in the database file and prevents a warning being displayed.

-----------------------
script mydataconnection
-----------------------

	-- used for debugging purposes only!

	on  create
		debug "(new connection)"
	end create
	
	on  delete
		debug "(connection lost/closed)"
	end delete

----------
end script
----------


-----------------
script jcpcontrol
-----------------

	on  create
		--
		-- (note - these records are typically created while the 
		-- database is NOT running under the control of CL)
		--
		if exists partner then set partner of partner to me
		Check_Heartbeat_Interval ()
		Activate ()
	end create

	on  delete
		if exists partner then set partner of partner to null
	end delete

	on  Activate
		--
		-- called when the arbitrator database restarts, and also when
		-- this object is created (if CL is running at that time).
		-- 
		-- TAKE CARE HERE - the databases may already be running, it
		-- might be the arbitrator that failed! In which case, leaving
		-- 'active' field as null will be the right action; the
		-- server will set it to the correct value.
		--
		set Watchdog_Running to false
		set HeartBeat to seconds (0) -- any prior value rubbish!
		Check_Heartbeat_Interval ()

		-- try and ensure the 'right' server is flagged active; if
		-- no partner, this is easy; if I have a partner, wait a bit
		-- (in case the servers are already running and can tell me
		-- their config) and then make the preferred one master.

		if not exists partner then
			set active to true
		else
			set active to null
			if preferredserver and not active of partner then 
				send SetPreferred () to me
			end if
		end if 
	end Activate

	-----------------------------------------------------------
	-- respond to changes in attributes: the 'on set' handlers.
	-----------------------------------------------------------
	 
	on  set Heartbeat_interval
		Check_Heartbeat_Interval ()
	end set HeartBeat_interval
	
	on  set Heartbeat 
	 
		local reference DataConnection d
		local string str = ""  
		
		-- remember the connection for this server.
		-- note we dont save a POINTER but just the
		-- id, otherwise the object can't be deleted
		-- when the connection is lost! As the 
		-- server can validly lose its connection
		-- and reconnect (using a different
		-- dataconnection object), we have to
		-- continually record this value (or note
		-- when the connection is lost and made
		-- again, at which time we do the check;
		-- however, it is easier though slightly
		-- less efficient to just record the id
		-- at every heartbeat).
		
		set d to GetConnection ()
		if exists d then set connection to id of d
		
		if not Watchdog_Running then 
		
			-- start the watchdog if we know what mode
			-- the server ought to be in (that is, when
			-- the active attribute is not null; test
			-- this using 'exists').
			
			if exists active and InContact () then StartWatchdog ()
			
		else
		
			-- watchdog is already running.
			
			if heartbeat_interval >= seconds(1) then
				report ("tick!")
			end if
			
			-- code to detect standby idle when its partner is not.
			-- This condition probably indicates that the standby
			-- has lost its connection to the master.

			if active or not exists partner then
				set idle_count to 0
			else if (transaction_no > -17 and transaction_no <= 0) then
				-- (standby, but still starting up)
				set idle_count to 0
			else if test_code_for_stopping_standby then
				add 1 to idle_count
				repeat for idle_count
					set str to str & "."
				end repeat 
				debug str
			else if transaction_no <> old transaction_no then
				-- some journal records have come through since
				-- last heartbeat)
				set idle_count to 0
			else if InContact () of Partner \
			     and transaction_no of partner <> transaction_no then
				-- the case we are worried about! no journal
				-- records coming through to standby, but 
				-- transactions seem to be ocurring in the master
				add 1 to idle_count       
			else
				-- standby not getting journal records, but
				-- it seems in step with the master (or
				-- my connection with master seems suspect, 
				-- which will be caught elsewhere
				set idle_count to 0 
			end if
			
		end if
	end set Heartbeat

	on  set Active
		--
		-- 'active' has been changed  - so take appropriate action.
		--
		if not exists active then
			-- active is set null during the startup phase to give
			-- already-running servers the chance to tell us the
			-- mode they are in.
		else if active then
			Report ("set as master")   
			if exists partner then set active of partner to false
		else
			Report ("set as standby")
			--set HeartBeat to seconds (0) -- DB will be stopping
			if exists partner then
				delay switchover_delay
				set active of partner to true
			end if
		end if
	end set Active
	
	on  set partner
		--
		abort transaction "cannot change partner attribute at present" 
	end set partner

	on  set preferredServer
		if exists partner then
			if exists preferredServer then
				set preferredServer of partner to \
						not preferredServer
			end if
		else
			set preferredServer to null
		end if
	end set preferredServer
	
	on  Check_Heartbeat_Interval
		--
		-- ensure heartbeat_interval is valid.
		--
		if not IsValidDateTime (Heartbeat_Interval) then
			set Heartbeat_Interval to seconds (30)
		end if
	end Check_Heartbeat_Interval
	
	on  set Transaction_no
		if old transaction_no = 0 then 
			report ("DB running")
		else if transaction_no = 0 then
			report ("DB starting?") 
		end if 
		/* testing: remove the 'if' once over. */
		if transaction_no < 0 then set idle_count to 0
	end set Transaction_no
	
	--------------------------------------
	-- procedures of use in other methods.
	--------------------------------------

	on  StartWatchdog
		--
		set Watchdog_Running to True
		send Watchdog () to me
	end StartWatchdog
	
	on  SetPreferred
		--
		-- called at startup to allow the preferred record to
		-- claim control after a while - but only if the
		-- active flag is still null, indicating that if any
		-- servers have connected, they did not know the state
		-- they were in. (Thus, we are not recovering from a
		-- failure of the arbitrator database, but starting up the
		-- FT service from scratch.)
		--
		sleep 30
		if not exists active then
			-- (NB, someone may have set 'preferred' in the
			-- interim).
			set active to preferredServer
		end if
	end SetPreferred
	
	on  Watchdog
		--
		-- watch for loss of contact with a running database
		-- (which may be active or standby)
		--
		local reference DataConnection d
		local datetime  rc = now () + seconds (5)
		local string    myname
		
		local integer dt = \
			round (to_microseconds(Heartbeat_Interval)) div 2
			
		Report ("watchdog started") 
		
		-- wait until the server seems to have got its initial
		-- snapshot image.
		
		repeat until transaction_no > 0 or transaction_no < -20
			delay dt
			if not InContact () then
				exit repeat
			end if
			if now () > rc then
				Report ("server still starting...")
				set rc to now () + seconds (5)
			end if 
		end repeat
		
		Report ("server seems ready")
		
		-- see if we ought to fail-over to the newly-started server
		   
		set rc to now () + recovery_time
		if preferredserver and exists partner and \
		   exists active and not active and       \
		   exists recovery_time and               \
		   recovery_time > milliseconds (100) then
	
			-- this is the preferred database, but it is currently
			-- not active. we wait for a bit (as defined by the
			-- recovery_time attribute) to confirm that this
			-- database remains active (both so that a machine
			-- that fails shortly after startup is detected, and
			-- so that the db has a chance to get up to date with
			-- the master db), and then switch over to it.
			--
			-- if contact is lost whilst waiting, then we should
			-- wait until service is resumed, and then wait again
			-- for the recovery time.

			Report ("(auto-switch to me?)")
			
			repeat until now () > rc
				delay dt
				if not InContact () then
					set rc to now () + recovery_time
				end if
			end repeat
			if Incontact () and not active then
				Report ("auto-switching!")
				set active of partner to false
			end if
		end if

		-- main loop.
		
		repeat forever

			delay dt

			if InContact () then
				if exists partner and not active then
					if not exists Watchdog_running of Partner then
						Report ("claiming from" && name of partner)
						set active to true
					else if idle_count > idle_limit then
						-- the standby seems to have lost
						-- connection with the master.
						
						report ("Standby seems to have lost contact with the master")
						
						-- If we drop its connection with
						-- us, it will stop when it's
						-- connection to the master seems idle:
					    
						--locate DataConnection (id=connection) into d
						--if exists d then delete d
						
						-- The above worked with 4.3.1 onwards,
						-- but the technique does not work if
					        -- what is wanted is to stop the standby
						-- even though the connection with the master
					        -- is working. The following code will do
						-- this, and will also mean that we can work
						-- with 4.3.0 onwards.
						
					        set myname to name
						set name to "-" && myname
						delay 1
						Report ("(restoring record name to" && myname & ")")
						set name to myname
						
						exit repeat
						  
					end if
				end if 
			else
				if active and exists partner then 
					if inContact () of partner then
						Report ("passing control to" && name of partner)
						set active to false
					else
						Report ("lost contact, but" && \
							name of partner && "inactive(?)")
					end if
				else     
					Report ("Lost contact")
				end if
				exit repeat
			end if

		end repeat

		set WatchDog_Running to False
	end Watchdog

	function boolean InContact
		--
		-- has our jcp been in contact recently?
		--
		if not IsValidDateTime (Heartbeat) then return false
		if Heartbeat=seconds(0) then return false
		return Now () < Heartbeat + Heartbeat_Interval+Heartbeat_Interval
	end InContact

	on  FailOver
		--
		-- a method that can be triggered by a client
		-- by means of the SQL 'send' command:
		--
		--    send 'Failover' to jcpcontrol'
		--
		-- the method will yield control, when applied to
		-- the record for the master database with a standby
		-- in the right state.
		--
		if active and exists partner then
			if InContact () of partner then
				delay 0
				debug "explicit failover from" && name
				set active to false
			end if
		end if
	end FailOver
	
	on  Report (string str)
		local string state
		if active then
			set state to "master "
		else if exists active then
			set state to "standby"
		else
			set state to "unknown"
		end if     
		debug httpNow() && name & "," && state & ", #" & \
		      transaction_no & ": " & str
	end Report

----------
end script
----------


--------------------------------------
function string httpDate (datetime d)
--------------------------------------
-- convert a datetime to the canonical
-- http format, for example...
--	Tue, 29 Apr 97 10:14:05 GMT
--------------------------------------
	return (item (1+The_weekday(d)) of "Sun,Mon,Tue,Wed,Thu,Fri,Sat") & \
		"," && get_DateTimef (d, "%02d %03M %04y %02h:%02i:%02s GMT")
------------
end httpDate
------------


----------------------------------------
function string httpNow
----------------------------------------
-- convert the datetime to the canonical
-- http format, for example...
--	Tue, 29 Apr 97 10:14:05 GMT
----------------------------------------
	return httpDate (now ())
-----------
end httpNow
-----------


----------------------------------------
function string ShowNow
----------------------------------------
-- convert the current time to an 
-- httpabbreviated format, for example...
--	Tue 10:14:05 GMT
----------------------------------------
	local datetime d = Now ()
	return (item (1+The_weekday(d)) of "Sun,Mon,Tue,Wed,Thu,Fri,Sat") & \
		"," && get_DateTimef (d, "%%02h:%02i:%02s GMT")
-----------
end ShowNow
-----------


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------
     
