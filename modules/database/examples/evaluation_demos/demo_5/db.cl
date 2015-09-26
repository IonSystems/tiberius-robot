------------------------------------------------------------------------------
-- Project:	Polyhedra
-- Copyright:	Copyright (C) 1994-2014 by Enea Software AB
--		All Rights Reserved
-- Date:	$Date: 2014/01/06 14:49:01 $
-- Revision:	$Id: db.cl,v 1.8 2014/01/06 14:49:01 andy Exp $
-- Author:	Dave Stow, Nigel Day
-- Description:	
------------------------------------------------------------------------------

-- CL Code for Demo 5
-- Version 1.0 - Dave Stow - December 2000
--               Initial version
-- Version 1.1 - Nigel Day - January 2001
--               validate limits, illustrating abort transaction 

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------


-- NB: -- flags that the rest of the line is a comment.
--     /* and */ can be used (as in C) for extended comments.


-- introduce the group of methods to be associated with the
-- tables called 'currency'; 'end script' terminates the group.


script currency

	-- set up a method to be triggered whenever the usdollar
	-- attribut is changed.
	
	on  set usdollar
		if usdollar < 0 then
			debug "US Dollar value cannot be negative"
			set usdollar to 0
		end if
	end set usdollar

end script


-- now the methods for the 'currency_limit' table - many more of these!


script currency_limits

	on  create
	
		-- code triggered whenever an object of this type
		-- is created, and run in the context of the object
		
		validate_limits ()
		
		if usdollar > high_limit then
			set status to 'HIGH'
			debug "Currency " & code & " is over high limit"
		else if usdollar < low_limit then
			set status to "LOW"
			debug "Currency " & code & " is under low limit"
		else
			set status to "OK"
		end if
		
	end  create

	on  set usdollar

		-- called whenever the attribute value changes for
		-- any reason (but not on creation, as 'initialisation'
		-- by the SQL INSERT statement (or whatever it was that
		-- created the record) does not count as a 'change' to
		-- the value).
  
		check_value ()
		
	end set usdollar
	
	on  check_value  

		-- a named method, callable by other CL-coded methods.
		-- such methods can take arguments, this one does not.
		-- functions, returning values, are also supported.
  
		if usdollar > high_limit and status<>'HIGH' then
			debug code & " is over high limit"
			set status to "HIGH"
		end if

		if usdollar < low_limit and status<> 'LOW' then
			debug code & " is under low limit"
			set status to "LOW"
		end if

		if usdollar >= low_limit and usdollar <= high_limit then
			debug code & " is within the limits"
			set status to "OK"
		end if

	end check_value
	
	on  set high_limit
	
		validate_limits ()
		check_value ()
  
	end set high_limit
	
	on  set low_limit
	
		validate_limits ()
		check_value ()

	end set low_limit
	
	on  validate_limits
		
		if low_limit < 0 then
			abort transaction "-ve low limit for" && code
		else if high_limit <= low_limit then
			abort transaction "invalid limits for" && code
		end if  
	
	end validate_limits

end script