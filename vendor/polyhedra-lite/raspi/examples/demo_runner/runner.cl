-------------------------------------------------------------------------------
--			P O L Y H E D R A   A P P L E T
--	 	     Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : replica.txt
--    Description   : automatic database runner.
--    Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


/*  the idea is that you embed something like the following lines in your
poly.cfg file...

runner:
type             = clc
root_class       = Monitor
cl_library       = ../poly/demos/bin/runner
monitor		 = 8001
checkdelay       = 300
clients          = *echo hello there,*echo goodbye
autoclients      = animate 8001,active 8001

...  and then when you issue the command 'clc runner' (when set to the 
root directory of your application/demo), an application runs that will 
start your database up, and restart it if it fails.  The database will be 
monitored, so that if it ever starts refusing connections the database 
process will be killed and restarted.  Whenever the database is restarted, 
the designated clients are also restarted.  

resources used:

monitor		the service address of the database to monitor.
		(viz: poly, 1234, nigel.polyhedra.com:5182)

path		when triggering off executables, a list of directories in which
		to look. If undefined, the environment variable PATH is used.
		The elements of the list can be separated by spaces, commas, 
		semi-colons or colons.

polypath	a list of directories, used when searching for executables 
		IN ADDITION to those in the path resource or PATH environment 
		variable. Please use same separator convention as is used in
		'path', see above (or the env variable PATH if 'path' undefined)            

dbname		Normally, the database is fired off using the poly.cfg entry
		point 'db'. The dbname resource allows you to give an alternate.

checkdelay	how long (in seconds) between consecutive connection attempts,
		when looking to see if a running database is still accepting 
		connections. Omitting this or giving the value of 0 means the
		default of 60 seconds is used.

clients		a comma-separated list of 'clients' - actually, the command
                lines used to set them off. Unless the client starts with an
		asterisk (which would be stripped off) the first word is looked
		up using the 'polypath' and 'path' settings to find out where
		the executable resides on file.

autoclients	similar to 'clients', but these commands are to be restarted if
		they stop whilst the database is (seemingly) still running. 
		
allowDbAtStart  do we stop if the database seems to be running at the time
                that the runner program starts, or do we carry on as best we
		can? (In the latter case, we cannot kill the database process
		if it seems locked up).

inline          are the initial clients done sequentially, or in parallel?
                in the former case, the autoclients will not be run until the
		initial clients have all terminated. By default, inline=no
		
assumptions made:

* poly.cfg has entry point <dbname> (defaulting to "db") to run the database

* the rtrdb (and clc) executable is READABLE as well as runnable;
  if not, this code cannot locate it for itself, which can give trouble if
  the shell path of spawned processes will not contain the right directory.

*/


-------------------------------------------------------------------------------
-- global constants.
-------------------------------------------------------------------------------


constant string  separators     = "; :,"

constant string  db_cmd         = GetPath ("rtrdb")
constant string  clc_cmd        = GetPath ("clc")

constant integer checkDelay     = GetIntDefault ("checkDelay",  60)
constant boolean allowDbAtStart = GetBoolDefault ("allowDbAtStart", true)
constant boolean runInline      = GetBoolDefault ("inline", true)


-------------------------------------------------------------------------------
--		c l - c o d e d   g l o b a l   f u n c t i o n s .
-------------------------------------------------------------------------------


-------------------------------------------------------------------------------
function Boolean GetBoolDefault (string res, Boolean def)
-------------------------------------------------------------------------------
-- look for a resource of a given name, and return TRUE if it holds a suitable
-- value; if the resurce cannot be found, return the supplied default value.
-------------------------------------------------------------------------------

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

------------------
end GetBoolDefault
------------------


-------------------------------------------------------------------------------
function integer GetIntDefault (string res, integer def)
-------------------------------------------------------------------------------
-- look for a resource of a given name, and (if found) return its value as an
-- integer. If it can't be found, return the supplied default.
-------------------------------------------------------------------------------

	local string s
	set s to GetResource (res)
	if s <> "" then
		return chartonum (s)
	else
		return def
	end if

-----------------
end GetIntDefault
-----------------


-------------------------------------------------------------------------------
function String GetDefault (String Resource, String TheDefault)
-------------------------------------------------------------------------------
-- Generic Handler for allowing the use of resources but ensuring the
-- definition of a default.
-------------------------------------------------------------------------------

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

--------------
end GetDefault
--------------


-------------------------------------------------------------------------------
function string GetPath (string exec)
-------------------------------------------------------------------------------
-- find the pathname for the given
-- executable.
-------------------------------------------------------------------------------

	local integer i
	local string  separator
	local string  path 	= GetResource ("path")

	if path = "" then set path to GetEnv ("PATH")

	-- assume now that 'path' contains a list of
	-- directory names... see which one contains <exec> or
	-- <exec>.exe
	-- (the constant 'separators' contains a list of expected
	-- separator charactors; arrange to 'lock in' to one of them
	-- (by trying each in order to find if it is used in 'path').

	repeat with i=1 to numberofchars (separators)
		set separator to char i of separators
		if separator in path then exit repeat
	end repeat

	-- now we know a separator, prepend the list a resource-
	-- supplied list, and then add in two other suggestions
	-- as to where things can be found (one suitable for UNIX
	-- and the other for Windows)...

	set path to GetResource ("PolyPath") & separator & \
			path                 & separator & \
			"/usr/local/bin"     & separator & \
			"c:/poly/bin"	     & separator

	return CheckPath (exec, path, separator)

-----------
end GetPath
-----------


-------------------------------------------------------------------------------
function string CheckPath (string exec, string path, string separator)
-------------------------------------------------------------------------------
-- find the pathname for the given executable, using supplied pathlist
-- and pathlist item separator.
-------------------------------------------------------------------------------

	local file    fileobj
	local boolean flag
	local integer i
	local integer j		= 1
	local string  name

	-- assume now that 'path' contains a list of
	-- directory names... see which one contains <exec> or
	-- <exec>.exe

	repeat with i = 1 to numberofchars (path)
		if char i of path = separator then
			if i > j then
				set name to \
					(char j to (i-1) of path) & "/" & exec
				set name of fileobj to name
				if Open () of fileobj then 
					set flag to Close () of fileobj
					return name
				end if
				set name to name & ".exe"
				set name of fileobj to name
				if Open () of fileobj then 
					set flag to Close () of fileobj
					return name 
				end if
			end if
			set j to i + 1
		end if
	end repeat

	debug "no path found for" && exec

	return ""

-------------
end CheckPath
-------------


-------------------------------------------------------------------------------
function boolean CheckFile (string name)
-------------------------------------------------------------------------------
-- find out whether a given file exists.
-------------------------------------------------------------------------------

	local file    fileobj
	local boolean flag
	
	set name of fileobj to name
	if Open () of fileobj then 
		set flag to Close () of fileobj
		return true
	end if

	return false

-------------
end CheckFile
-------------


-------------------------------------------------------------------------------
--	c l - e n c o d e d   c l a s s   d e f i n i t i o n s .
-------------------------------------------------------------------------------


---------------------
class task is program
---------------------

	-- a class that runs a program, optionally reports to
	-- its owner on completion. 
	-- fairly general-purpose code! Create with the (inherited)
	-- attribute 'command' set accordingly, and with the
	-- following attributes set as needed:

	export reference monitor owner
	export string            action    = ""
	export boolean		 inline    = false
	export boolean		 suicidal  = true
	export boolean           auto      = false
	integer                  startct   = 0
	integer                  dbstartct = 0

	on  create
		--
		if exists owner then set dbstartct to StartCount of owner
		if inline then
			execute ()
		else
			send execute () to me
		end if
	end create

	on  execute
		--
		add 1 to StartCt
		if auto then
			debug  now () & "\n\t about to run '" & command & \
			"' (iteration count =" && StartCt & ")\n"
		else
			debug  now () & "\n\t about to run '" & command & "'\n"
		end if

		run ()
		wait ()

		if status <> 0 then
			debug now () & "\n\t '" & command & \
			               "' failed with rc" && status && "\n"
		else
			debug  now () & "\n\t '" & command & "' completed\n"
		end if

		if exists owner and action <> "" then do action to owner
		if auto then
			sleep 5
			if IsOpen of owner                     \
			   and StartCount of owner = dbstartct \
                           and exists dbtask of owner          \
                        then
				send execute () to me
				exit
			end if
		end if			
		if suicidal and exists owner then
			send KillTask (me) to owner
		end if
	end execute

---------
end class
---------


----------------------------
class monitor is dataservice
----------------------------

	export reference task dbtask
	array of task         clients
	string                dbname         = GetResource ("dbname")
	boolean               ClientsStarted = false
	export integer        StartCount     = 0  
	boolean	              AdoptedDB      = false  

	on  create
		--
		-- fire off a separeate thread to do the actual work of
		-- this program, since it is not good form to have something
		-- than suspends an 'on create' handler. (calling open() on
		-- a dataservice suspends the thread.)
		send work () to me
	end create
	
	on work 
		--
		set name to GetResource ("Monitor")
		if name="" then
			debug "'monitor' resource not defined."
			quit
		end if
		if dbname="" then set dbname to "db"

		Open ()
		if IsOpen then
			if allowDbAtStart then
				debug "*** WARNING ***\n\tDB already running!"
				set AdoptedDB to true
				StartClients ()
			else
				debug "*** ERROR ***\n\tDB already running!"
				quit
			end if 
		else
			Check_dbtask ()
		end if
	end work

	on  dbDead
		--
		if exists dbtask then delete dbtask
		Check_dbtask ()
	end dbDead

	on  Check_dbtask
		--
		if exists dbTask then exit

		-- EITHER this is the first time through, OR
		-- a database has stopped/failed and its task
		-- has suicided.
		-- fire off a new attempt at starting the db

		set ClientsStarted to false
		add 1 to StartCount
		debug "-----------------------------------------------------"
		debug now () && "- Starting the db (count=" & StartCount & ")"
		debug "-----------------------------------------------------\n"

		If IsOpen then
			-- race condition: have not yet noticed that the
			-- connection has died. 
			sleep 1
			if IsOpen then Close ()
		end if

		create task ( command  = db_cmd && dbname \
		            , owner    = me               \
                            , action   = "dbdead"         \
		            , suicidal = false            \
		            ) into dbtask
		send OpenMe () to me
	end Check_dbtask

	on  StartClients
		--
		-- start off both the one-shot and the permanent clients.
		-- 
		debug now () & "\n\t (re)starting the clients.\n"
		StartClientsFromList (GetResource ("clients"),     false)
		StartClientsFromList (GetResource ("autoclients"), true)
	end StartClients

	on  StartClientsFromList (string commands, boolean auto)
		--
		local integer n        = NumberOfItems (commands)
		local integer i
		local string  s
		local string  c
		local integer m


		repeat with i = 1 to n
			set s to item i of commands

			-- patch word 1 of s to reflect the right path, unless
			-- the first character is an asterisk (in which case
			-- just strip the asterisk)
			
			set c to word 1 of s
			if c = "clc" then
				set c to clc_cmd
			else if char 1 of c = "*" then
				set c to char 2 to (NumberOfChars (c)) of c
			else
				set c to GetPath (c)
			end if
			set m to NumberOfWords (s)
			if c = "" then
				debug "(path problems with '" & s & "')"
			else if m = 1 then
				set s to c
			else
				set s to c && word 2 to m of s
			end if
			
			create task ( command  = s                      \
			            , suicidal = true                   \
			            , owner    = me                     \
			            , auto     = auto                   \
				    , inline   = runInline and not auto \
			            ) into clients
		end repeat

	end StartClientsFromList

	on  set IsOpen
		--
		if IsOpen and exists dbtask and not ClientsStarted then

			-- this is the very first time we have
			-- connected to this database task:
			-- start off the clients

			set ClientsStarted to true
			StartClients ()
			send CheckConnection () to me

		else if AdoptedDB and not IsOpen then
		
			-- the db was running at startup, but now seems 
			-- to have died. 
			
			set AdoptedDB to false
			send dbDead () to me 
			
		end if
	end set IsOpen

	on  OpenMe
		--
		-- keep trying to open a connection until it succeeds
		--
		local integer sc = StartCount

		if exists dbtask and not IsOpen then
			repeat until IsOpen or not exists dbtask
				-- wait 1/2 a second
				delay 500*1000
				if sc<>StartCount then exit
				Open () of me
			end repeat
		end if
	end OpenMe

	on  CheckConnection
		--
		-- every now and then close and re-open the connection,
		-- just to check the db is still accepting connections.
		--
		local integer sc

		set sc to StartCount

		repeat while IsOpen
			sleep CheckDelay
			if sc <> StartCount then exit
			if IsOpen then
				Close ()
				Open ()
				-- try again just to be sure...
				if not IsOpen then
					sleep 2
					Open ()
				end if
			end if
		end repeat

		-- we are fairly sure the db is dead!

		if sc=StartCount and exists dbtask and not IsOpen then
			debug now () & "\n\t cannot connect, so killing db!\n"
			kill () of dbtask
		end if
	end CheckConnection

	on  KillTask (task t)
		--
		delete t
	end KillTask

---------
end class
---------


-------------------------------------------------------------------------------
--                        E n d   o f   F i l e
-------------------------------------------------------------------------------
