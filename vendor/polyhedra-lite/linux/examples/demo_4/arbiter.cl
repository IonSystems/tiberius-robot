------------------------------------------------------------------------------
-- Project:	Polyhedra
-- Copyright:	Copyright (C) 1994-2015 by Enea Software AB
--		All Rights Reserved
-- Author:	Nigel Day/Dave Stow
-- Description:	
------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

--
--	Arbiter.cl
--
--	CL coded arbiter, using CLC to provide
--	very simplistic arbitration mechanism
--
------------------------------------------------
--
--	v1.0	Nigel Day/Dave Stow - 28 December
--		Nigel Day's DM arbiter with all 
--		graphical code stripped out by
--		Dave Stow.
--
--	v1.1	Dave Stow - code updated to provide
--		better debugs and copes with slow 
--		starting databases. New resource setting
--		"heartbeat_debugs" set to true will show
--		debugs for all the heartbeats.
--
--              Now under CVS control
--

--------------------
-- Global functions.
--------------------

function Boolean GetBoolDefault (string res, Boolean def)
	-- Look for a resource of a given name, and return 
	-- TRUE if it holds a suitable value; if the resource
	-- cannot be found, return the supplied default value.

	local string s
	set s to GetResource (res)
	if s <> "" then
		set s to uppercase (s)
		if s = "YES" or s = "Y" or s = "TRUE" or s = "ON" then 
			return true
		else
			return false
		end if
	else
		return def
	end if

end GetBoolDefault

function integer GetIntDefault (string res, integer def)
	-- look for a resource of a given name, and (if found)
	-- return its value as an integer. If it can't be found,
	-- return the supplied default.

	local string s
	set s to GetResource (res)
	if s <> "" then
		return chartonum (s)
	else
		return def
	end if

end GetIntDefault

function String GetDefault (String Resource, String TheDefault)
	-- Generic Handler for allowing the use of resources but
	-- ensuring the definition of a default.

	Local String Temp = ""

	if Resource = "" then
		if TheDefault <> "" then
			return TheDefault
		else
			debug "Resource and Default Null"
			return ""
		end if
	else
		Set Temp to GetResource (Resource)
		if Temp <> "" then
			return Temp
		else
			return TheDefault
		end if
	end if

end GetDefault

function string NumberToDottedIPAddress (string s)
	-- given a string holding a number, convert
	-- it to the equivalent IP dotted address

	local integer n  = CharToNum (s)
	local string  res

	set res to 	bitAnd (255, bitShiftRight (n, 24)) & "." & \
			bitAnd (255, bitShiftRight (n, 16)) & "." & \
			bitAnd (255, bitShiftRight (n,  8)) & "." & \
			bitAnd (255, n)
	--debug "NumberToDottedIPAddress (" & s & ") =" && res
	return res

end NumberToDottedIPAddress

function integer DottedIPAddressToNumber (string s)
	-- given a string holding a IP dotted address,
	-- convert it to the equivalent number.
	-- NB. this code is very lazy, has NO error checking 
	-- other than for too many dots.

	local string  c
	local string  d   = ""
	local integer i	  = 1
	local integer j   = 0
	local integer n   = 0
	local integer res = 0

	set s to s & "." -- allow lazy coding

	repeat with i=1 to NumberOfChars (s)
		set c to char i of s
		if c = "." then
			set res to BitOr (res, BitShiftLeft (n, 24-j*8))
			add 1 to j
			if j=4 then exit repeat
			set n to 0
		else
			set n to n * 10 + CharToNum (c)
		end if
	end repeat

	return res

end DottedIPAddressToNumber



-------------------
-- Global constants
-------------------

constant integer maxrequestbuffersize =  1000
constant integer responsebuffersize   =  4

constant boolean heartbeat_debugs = GetBoolDefault("heartbeat_debugs",false)

-- heartbeat interval is gained from the poly.cfg file. If not specified there
-- then it defaults to 5000000us - 5 seconds.
constant integer heartbeat_interval   = GetIntDefault ("heartbeat_interval",5000000)

-- The maxgap is the time allowed for a heartbeat before it times out
constant datetime maxgap              = Microseconds (heartbeat_interval * 2)

-- the max_db_startup_time is the maximum length of time a database is allowed to 
-- spend starting up - here it is 30 seconds.
constant datetime max_db_startup_time = Microseconds (30000000)


----------------------------------------------
-- Classes to handle the arbitration mechanism
----------------------------------------------

class ArbitratorPort is tcpServer
	-- Code for a tcp port that receives messages
	-- from the RTRDBsthis code implements a VERY
	-- simple strategy for deciding which is the
	-- active database: of those connected, it is
	-- the one that has been longest connected (with
	-- auto-disconnection occuring if no heartbeat
	-- signal seen for a while). 

	export array of rtrdbConnection	rtrdbs
	export reference object		Owner
	string				name = GetResource ("arbitrator_service")

	on  create
		local integer p

		-- if there is a colon in the port name,
		-- strip off everything up to and including the colon.
		-- We are only doing this once, so we can do it the
		-- lazy way!

		while ":" in name
			set name to char 2 to 999 of name
		end while

		set p to CharToNum (name)
		if p=0 then
			debug "arbitrator - bad port number given (must be numeric)"
			quit
		else if not QueueOpen (p) then
			debug "arbitrator system error - QueueOpen (" & p & \
							") returned false"
			quit
		end if

	end create

	on  OpenDone
		--
		local string str = GetlastError ()

		if str = "" then
			debug "Arbitrator server ready on port" && name
		else
			debug "arbitrator - open on port" && name && \
							"failed:" && str
			quit
		end if
	end OpenDone

	on ConnectionRequest (integer address)
		--
		-- override the default, since we want to create
		-- a rtrdbConnection object.
		--
		local reference rtrdbConnection obj

		create rtrdbConnection	( owner   = me			\
						, address = address		\
						) into obj

		if exists obj then
			if not QueueAccept (obj) then
				debug "arbitrator - QueueAccept failed"
				delete obj
			end if
		end if

	end ConnectionRequest

	on  AcceptDone (integer result)
		--
		-- a QueueAccept is processed - but we cannot tell which
		-- object.
		--
		if result<>0 then
			debug "arbitrator - connection not set up, code" && result
			-- NB: the connection object is now in limbo?
		end if
	end AcceptDone

	on  Register (rtrdbConnection jc)
		--
		-- a rtrdb has connected.
		--
		local reference rtrdbConnection jc1 = object 1 of rtrdbs

		if exists object 2 of rtrdbs then

			debug "too many RTRDB connections!"
			delete jc

		else if exists jc1 then

			-- there is one other rtrdb (presumably active);
			-- insert the jc object in the appropriate place
			-- in the rtrdbs array

			if name of jc < name of jc1 then
				insert jc into rtrdbs at 1
			else if name of jc > name of jc1 then
				insert jc into rtrdbs
			else if address of jc < address of jc1 then
				insert jc into rtrdbs at 1
			else
				insert jc into rtrdbs
			end if

		else

			-- no other rtrdb, so mark this one as active
			-- and store a pointer to it in the rtrdbs array.

			set active of jc to true
			insert jc into rtrdbs

		end if

		debug "RTRDB connected from " & \
			NumberToDottedIPAddress(address of jc) & ":" & name of jc

	end Register

	on  Deregister (rtrdbConnection jc)
		-- connection with a RTRDB has been lost or aborted.
		-- If it was the active, failover to the standby

		remove jc from rtrdbs
		
		if active of jc then
			debug "Active RTRDB" & \
				NumberToDottedIPAddress(address of jc) & \
				":" & name of jc & " has disconnected."
		else
			debug "Standby RTRDB" & \
				NumberToDottedIPAddress(address of jc) & \
				":" & name of jc & " has disconnected."
		end if

		-- if this was the active rtrdb, try to give control to the
		-- standby.

		if active of jc then
			if exists object 1 of rtrdbs then
				set active of object 1 of rtrdbs to true
				debug "Send " & \
					NumberToDottedIPAddress(address of object 1 of rtrdbs) & \
					":" & name of object 1 of rtrdbs & " active."
			end if
		end if

	end Deregister

end class

class rtrdbConnection is tcpConnection
	-- rtrdbConnection class handles each tcp connection
	-- to the arbitrator. This is the class that receives
	-- incoming heartbeats from the rtrdb, and responds to
	-- them. It also has the 'watchdog' function to 
	-- test for the heartbeat timing out.

	export reference ArbitratorPort	owner
	export integer				address -- IP address

	export string	name
	export integer	transaction_no	= 0
	export boolean	active		= false
	export boolean	alive			= true

	datetime		ExpireTime
	boolean		registered	= false

	boolean		firstheartbeat = false

	on create
		set firstheartbeat to true
	end create

	on  delete
		--
		-- the connection has been dropped for some reason, by one end
		-- or the other.
		--
		if registered then DeregisterMe ()
	end delete

	on  set active
		--
		-- this is set true when
		--
		-- (a)	this is the first rtrdb to register (in which case
		--	registered is just about to be set true, inside 
		--	ReadDone)
		-- (b)	the connection to the rtrdb that was active is dropped
		--	and I am the first remaining object in rtrdbs of owner.
		-- (c)	manual switchover has been triggered (somehow).
		--
		if registered then ReportStatus ()
	end set active

	on  Suicide
		--
		local reference object obj = me
		delete obj
	end Suicide

	on  DeregisterMe
		--
		set registered to false
		set alive      to false
		Deregister (me) of owner
	end DeregisterMe

	on  OpenDone (integer result)
		--
		if result <> 0 then
			debug "Open failed, result code" && result
		else
			-- set off a read.

			ReadMessage ()

			-- start heartbeat watchdog
			set ExpireTime to now () + maxgap
			send Watchdog () to me		-- new thread to watch for timeout
		end if
	end OpenDone

	on  ConnectionLost (integer reason)
		--
		Suicide ()
	end ConnectionLost

	on  CloseDone (integer reason)
		--
		debug "arbitrator - connection closed" && reason
		Suicide ()
	end CloseDone

	on  TryToClose
		--
		DeregisterMe ()
		if IsOpen () then
			if not QueueClose (maxgap) then
				debug "arbitrator - QueueClose failed"
				Suicide ()
			end if
		end if
	end TryToClose

	on  ReadMessage
		--
		-- trigger the system to read the next message.
		--
		if not QueueRead (-maxrequestbuffersize, seconds(0), 0) then
			debug "arbitrator - QueueRead failed"
			TryToClose ()
		end if
	end ReadMessage

	on  ReadDone (integer id, binary value, integer result)
		-- cope with messages from the rtrdb, by analysing them,
		-- storing the information, and then telling the other
		-- end what mode it should be operating in.
		--
		-- The format of messages from RTRDB to arbitrator is:
		--
		--	J	1 byte
		--	<mode>	4 byte		
		--	<trans>	4 byte
		--	<name>	C-style string, including null byte
		--
		-- The mode values are:
		--	
		--	0	Unknown
		--	1	Master
		--	2	Standby
		--
		-- The protocol is documented in the section on fault
		-- tolerance in the RTRDB reference manual.
		--
		local integer i = 0
		local integer n = NumberOfBytes (value)
		local binary  b
		local integer mode

		if result <> 0 then

			debug "arbitrator - ReadDone called with result code" && result
			if IsOpen () then
				if not QueueClose (maxgap) then
					debug "arbitrator - QueueClose failed"
				end if
			end if
		end if

		--debug "arbitrator - read" && n && "bytes from" && \
		--		NumberToDottedIPAddress (address)

		-- cope with an empty message, such as can be generated when
		-- we close a stream with an open read request.

		if n=0 then exit

		if n < 11 or GetStrInBinary (value, 0, 1) <> "J" then
			debug "arbitrator - bad message '" & \
				BinaryToHexString (value) & "' from" && \
				NumberToDottedIPAddress (address)
			TryToClose ()
			exit
		end if

		set mode           to GetIntInBinary (value, -1) -- bytes 1-4
		set transaction_no to GetIntInBinary (value, -5) -- bytes 5-8
		set name           to GetStrInBinary (value,  9, n-10)

		-- Set the time when the arbitrator will expire and failover
		if firstheartbeat then
			debug "First heartbeat"
			set firstheartbeat to false
			set ExpireTime to now() + max_db_startup_time
		else
			set ExpireTime to now() + maxgap
		end if

		-- Print a debug regarding this heartbeat if they are turned on
		if heartbeat_debugs then 
			debug get_datetimef(localtime(now()),"%02h:%02i:%02s") & \
				": Heartbeat from " & NumberToDottedIPAddress(address) & ":" & name

		end if

		if not Registered and alive then
			-- ensure my owner knows about me, and can set
			-- my active attribute appropriately.
			Register (me) of owner
			set registered to true
		end if

		ReportStatus ()
		ReadMessage ()

	end ReadDone

	on  ReportStatus
		--
		-- send a message to the RTRDB telling it what state I think
		-- it is/should be in.
		--
		-- the form of messages from arbitrator to RTRDB is:
		-- 
		--	A		1 byte
		--	<mode>		4 byte
		--	<trans>		4 byte (as reported to us by the RTRDB)
		--	<interval>	4 byte (micro-seconds)
		--
		-- The valid mode values to send are:
		--	
		--	1	Master
		--	2	Standby
		--
		-- see readme.txt for more details
		--
		local binary b -- used to build & hold the message

		-- build the message

		set b to SetStrInBinary (b, 0, "A", false)	-- "A"

		if not alive then						-- "Master/Standby"
			TryToClose ()
			exit
		else if active and alive then
			set b to SetIntInBinary (b, -1, 1)
		else
			set b to SetIntInBinary (b, -1, 2)
		end if

		-- reflect transaction number and heartbeat interval
		set b to SetIntInBinary (b, -5, transaction_no)
		set b to SetIntInBinary (b, -9, heartbeat_interval)

		-- send the message
		if not QueueWrite (b, maxgap, 0) then
			debug "arbitrator - QueueWrite failed to" && name
			TryToClose ()
		end if
	end ReportStatus

	on  Watchdog
		--
		-- watch for loss of contact with a running database
		-- (which may be active or standby)
		--
		local integer dt = Heartbeat_Interval div 2

		repeat forever

			delay dt

			if Now () > ExpireTime then
				debug "No message from RTRDB" && \
					name && "for too long - failover"
				TryToClose ()
				exit 
			end if

		end repeat
	end Watchdog

end class


---------------------------------------
-- Main class - this is the entry point
---------------------------------------

class main

	export ArbitratorPort ap = { owner=me }

	on  create
		debug "The time is: " & localtime(now())
		debug "Arbitrator started."
		debug "Heartbeat interval is " & heartbeat_interval & " microseconds."
	end create

end class
