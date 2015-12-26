/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2001-2014 by Enea Software AB
//		All Rights Reserved
// Date:	$Date: 2014/01/06 14:48:58 $
// Revision:	$Id: active.java,v 1.9 2014/01/06 14:48:58 andy Exp $
// Authors:	Nigel Day
// Description:	active example
//------------------------------------------------------------------------------
//
// Source code for Active Query example client
// Launch an active query on the database and display the changing data.
//
//----------------------------------------------------------------------------*/

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

import java.sql.* ;

public class active
{
  public static void main(String[] argv)
    throws SQLException, ClassNotFoundException, InstantiationException,
           IllegalAccessException, InterruptedException
  {
    // load Polyhedra JDBC Driver
    // automatically registers with JDBC Driver Manager

    // note: the newInstance() is required for Visual J++
    Class.forName("com.polyhedra.jdbc.JdbcDriver").newInstance() ;

    // perform connection

    // get url
    String url = "jdbc:polyhedra://:8001" ;
    if (argv.length > 0) // use 1st commandline arg if specified
      url = argv[0] ;
    // get properties
    java.util.Properties prop = new java.util.Properties() ;
    if (argv.length > 1) // use 2nd commandline arg for user name
      prop.put("user", argv[1]) ;
    // connect
    Connection conn = DriverManager.getConnection(url, prop) ;

    // get result set

    String sql = "select code,usdollar from currency" ;
    Statement statement = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE
					       , ResultSet.CONCUR_READ_ONLY) ;
    statement.setMaxRows(10000) ;
    ResultSet resultSet = statement.executeQuery(sql) ;

    // print result set
    System.out.println("Initial state:") ;
    for (int row = 0 ; resultSet.next() ; row++)
      System.out.println(resultSet.getString(1) + " -> " + resultSet.getString(2)) ;

    // cycle waiting for a change.
    for (;;)
    {
	java.lang.Thread.sleep (2000);

	if (conn.isClosed ()) 
        {
	    System.out.println("\n(connection terminated.)") ;
            break;
        }

	int ctsame = 0;
	int ctdiff = 0;
	resultSet.beforeFirst ();

	for (int row = 0 ; resultSet.next() ; row++)
	{
	    resultSet.refreshRow();

	    if (resultSet.rowDeleted())
	    {
		if (ctdiff++ == 0) System.out.println ("");
		System.out.println(resultSet.getString(1) + " now deleted") ;
	    }    
	    else if (resultSet.rowInserted())
	    {
		
		if (ctdiff++ == 0) System.out.println ("");
		System.out.println(resultSet.getString(1) + " -> " + resultSet.getString(2) + " (new row)" ) ;
	    }    
	    else if (resultSet.rowUpdated())
	    {  
		if (ctdiff++ == 0) System.out.println ("");
		System.out.println(resultSet.getString(1) + " -> " + resultSet.getString(2)) ;
	    }  
	    else
	    {
		ctsame++;
	    }
	}
	if (ctdiff > 0)
	{
	    System.out.println("(" + ctsame + " rows unaltered)") ;
	}
	else
	{
	    // no changes
	    System.out.print(".");
	}
    }

    // close jdbc objects
    resultSet.close() ;
    statement.close() ;
    conn.close() ;
  }
}

/*------------------------------------------------------------------------------
// End of file
//----------------------------------------------------------------------------*/
