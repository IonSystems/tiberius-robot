-------------------------------------------------------------------------------
--			 P O L Y H E D R A    D E M O
--	 	     Copyright (C) 2005-2015 by Enea Software AB
-------------------------------------------------------------------------------
-- 	Filename      : globals.cl
-- 	Description   : some useful global functions, for use in RTRDB, CLC
-- 	Author        : Nigel Day
--
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


----------------------------------------------------------------------
function boolean GetBoolDefault (string resname, boolean defaultvalue)
----------------------------------------------------------------------
-- look up a resource in poly.cfg, and return a boolean indicating its
-- value; if the resource is undefined, return the supplied default
-- value.
----------------------------------------------------------------------
	local string resvalue = uppercase (GetResource (resname))
	local string res      = char 1 of resvalue

	--if resvalue = "" then return defaultvalue

	if defaultvalue then
		-- return true unless resname looks like it is set false
		if res = "N" or res = "F" then return false
	else
		-- return false unless resname looks like it is set true
		if res = "Y" or res = "T" then return true
	end if

	return defaultvalue

------------------
end GetBoolDefault
------------------


-------------------------------------------------------
function integer GetIntDefault(string res, integer def)
-------------------------------------------------------
-- look for a resource of a given name, and (if found)
-- return its value as an integer. If it can't be found,
-- return the supplied default.
--------------------------------------------------------
	local string s
	set s to GetResource(res)
	if s <> "" then
		return chartonum(s)
	else
		return def
	end if
-----------------
end GetIntDefault
-----------------


------------------------------------------------
function string HowLong (datetime dt, integer n)
------------------------------------------------
-- return a string indicating how long ago was
-- the supplied datetime; if n is non-zero, the
-- result also indicates how many operations per
-- second were done if n is the number of ops.
-- useful in code doing timing tests!
------------------------------------------------
	local real   secs = to_microseconds (now()-dt) / 1000000
	local string str  = Decimals (secs, 3) && "seconds"

	if n > 0 then
		set str to str && \
			"(" & truncate (n / secs) && "ops per sec," && \
			Decimals (secs / n, 6) && "secs per op)"
	end if
	return str
-----------
end HowLong
-----------


--------------------------------------------
function string Decimals (real r, integer n)
--------------------------------------------
-- return a string representing the given
-- real to n decimal places.
--------------------------------------------
	local integer whole
	local integer scale
	local integer fraction
	local string  zeros    = "0000000000" -- ten zeros, initially
	local string  trailing = ""

	-- cope with -ve numbers!
	if r < 0 then return "-" & Decimals (-r, n)

	-- cope with unexpected values for n
	if n <=0 then

		return round (r)

	else if n >10 then

		-- we are going via an integer to deal with the fractional
		-- part, so ensure that we dont try to store something too
		-- big in it; reduce n to be at most 10, and put the right
		-- number of zeros in 'trailing' to right-pad the number.

		set trailing to zeros
		-- keep doubling up until it is at least long enough...
		while NumberOfChars (trailing) < n-10
			set trailing to trailing & trailing
		end while
		-- ... and then throw away the surplus.
		set trailing to char 1 to (n-10) of trailing
		set n to 10

	end if

	set whole    to truncate (r)
	set scale    to 10^n
	set fraction to round ((r - whole) * scale)

	if fraction >= scale then

		-- once rounded to n digits, the fraction might overflow;
		-- for example, we want to represent Decimals (1.999, 2) by
		-- the string "2.00", not "1.00" or "1.100"!

		add 1 to whole
		set fraction to 0

	end if

	set zeros to char 1 to (n - NumberOfChars(fraction)) of zeros
	return whole & "." & zeros & fraction & trailing
------------
end Decimals
------------


----------------------------------------------------
function string RightJustify (string str, integer n)
----------------------------------------------------
-- return a string left-padded with spaces to ensure
-- its length is at least n characters.
----------------------------------------------------
	local string  spaces = "                   "
	local integer len    = NumberOfChars (str)

	subtract len from n
	if n <= 0 then return str

	while NumberOfChars (spaces) < n
		set spaces to spaces & spaces
	end while
	return (char 1 to n of spaces) & str 
----------------
end RightJustify
----------------


-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------

