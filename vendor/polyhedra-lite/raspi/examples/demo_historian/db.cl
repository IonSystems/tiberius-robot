------------------------------------------------------------------------------
-- Project:	Polyhedra
-- Copyright:	Copyright (C) 1994-2015 by Enea Software AB
--		All Rights Reserved
-- Author:	
-- Description:	
------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

script currency
	on activate
		local reference logcontrol ref
		locate logcontrol {id = 1} into ref
		set enable of ref to true
	end activate
end script

