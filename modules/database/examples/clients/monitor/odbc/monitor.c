/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2001-2014 by Enea Software AB
//		All Rights Reserved
// Date:	$Date: 2014/05/28 10:13:40 $
// Revision:	$Id: monitor.c,v 1.13 2014/05/28 10:13:40 alan Exp $
// Author:	Nigel Day, Andy England
// Description:	monitor example
//------------------------------------------------------------------------------
//
// Shows how active queries can be used to monitor changes in a table.
// A message is produced when a new currency_limit is set up, and when the
// current value moves into or outside the limits associated with the currency.
//
// In case of error, the 'exit' function is called; on embedded	platforms that
//  do not tidy up when tasks terminate, it would be more appropriate to alter 
// the logic of the program to leave cleanly via the main routine. As such coding 
// merely complicates the logic of the program without illustrating any new 
// features of the use of the Polyhedra ODBC library, the 'lazy' approach has 
// been adopted here.
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

/*------------------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------------*/

/* On Windows we need to include windows.h  */
#if defined(WIN32)
#include <windows.h>
#else
#include <unistd.h>
#endif

/* Include standard header files */
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

/* Include the ODBC header files */
#include <sql.h>
#if !defined(ODBC_STD)
#include <sqlext.h>
#include <sqlpoly.h>
#endif

/*------------------------------------------------------------------------------
// Useful macros
//----------------------------------------------------------------------------*/

#define FALSE 0
#define TRUE 1

/* Longest diagnostic message we can handle */
#define MAX_DIAG_MSG		256

/* Maximum number of currencies we want to deal with */
#define MAX_CURRENCIES	100

#define UNKNOWN_ALARM -1
#define NO_ALARM       0
#define LO_ALARM       1
#define HI_ALARM       2

/*------------------------------------------------------------------------------
// Global variables
//----------------------------------------------------------------------------*/

int			Rows[MAX_CURRENCIES];

/* Number of rows actually in this array */
int			NumRows;

/*------------------------------------------------------------------------------
// Error-check function called after any ODBC function to abort if it failed
//----------------------------------------------------------------------------*/

void check_success(
    int			ret, 
    SQLSMALLINT		handleType,
    SQLHANDLE		handle,
    const char *	errorMsg)
{
    if (ret != SQL_SUCCESS)
    {
	fprintf(stderr, "%s\n", errorMsg);

	if (handle != SQL_NULL_HANDLE)
	{
	    SQLSMALLINT	recNumber = 1;
	    SQLINTEGER	nativeError;
	    SQLCHAR	sqlState[6];
	    SQLCHAR	msg[MAX_DIAG_MSG];
	    SQLSMALLINT	actualLen;

	    sqlState[5] = '\0';

	    /* Get the diagnostics for the error */
	    while (SQLGetDiagRec(handleType, handle, recNumber++, &sqlState[0],
			         &nativeError, &msg[0], MAX_DIAG_MSG, &actualLen) == SQL_SUCCESS)
	    {
		fprintf(stderr, "ODBC error: %s: %s (%d)\n", sqlState, msg, (int)nativeError);
	    }
	}

	exit(1);
    }
}

/*------------------------------------------------------------------------------
// A function that only returns when the connection is broken or a delta has
// been received.
// Wait for an incoming event, returning the function ID - which will be enough
// for our purposes to determine what happened.
//----------------------------------------------------------------------------*/

SQLUSMALLINT WaitForIt(
    SQLHENV		henv)
{
    SQLUSMALLINT	functionId;
    SQLSMALLINT		handleType;
    SQLHANDLE		handle;

    for (;;) 
    {
	/* Get the next event */
	int ret = SQLGetAsyncEvent(henv, &functionId, &handleType, &handle);

	if (ret == SQL_NO_DATA)
	{
	    /* No event to handle; wait for a new message */

	    /* Generic function to wait for a Polyhedra message */
	    /* This can be replaced by OS specific main loop */
	    ret = SQLHandleMsg(henv);
	    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to handle message");
	}
	else
	{
	    return functionId;
	}
    }
}

/*------------------------------------------------------------------------------
// main function
//----------------------------------------------------------------------------*/

#if defined(EMBEDDED)
int poly_main(
#else
int main(
#endif
    int			argc,
    char *		argv[])
{
    SQLRETURN		ret;
    SQLHENV		henv;
    SQLHDBC		hdbc;
    SQLHSTMT		hstmt;
    char *		service = "8001";

    int			i;

    SQLCHAR		code[4];
    SQLDOUBLE		usdollar;
    SQLDOUBLE		low_limit;
    SQLDOUBLE		high_limit;

    /* Set indicator lengths */

    SQLLEN		indicators[4];


    /* Check we have the correct number of arguments */
    if (argc > 2)
    {
	fprintf(stderr, "usage: %s [<data service>]\n", argv[0]);
	return 1;
    }

    /* Check we have a service argument */
    if (argc > 1)
    {
	service = argv[1];
    }

    indicators[0] = sizeof(code);
    indicators[1] = sizeof(usdollar);
    indicators[2] = sizeof(low_limit);
    indicators[3] = sizeof(high_limit);

    /* Allocate an environment handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate environment handle");

#if !defined(ODBC_STD)
    /* Set the ODBC version used */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to set ODBC version");
#endif

    /* Enable async events */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to enable async events");

    /* Allocate a conection handle */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate connection handle");

    /* Connect to the database */
    printf ("connecting to database at %s...\n",service);
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to connect to the database");
    printf ("Connected, now launch active query...\n");

    /* Set manual commit mode on the connection */
    ret = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to set manual commit mode");

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Use dynamic cursor */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to make dynamic cursor");

    /* A little trick - set maximum rows to MAX_CURRENCIES */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_MAX_ROWS, (SQLPOINTER)MAX_CURRENCIES, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set maximum rows");

    /* Prepare the SQL query and bind the columns */
    ret = SQLPrepare(hstmt, 
		     (SQLCHAR*) "select code,usdollar,low_limit,high_limit from currency_limits",
		     SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Prepare failure");

    ret = SQLBindCol(hstmt, 1, SQL_CHAR,  &code, sizeof(code), &indicators[0]);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Bind failure (column 1 - id)");

    ret = SQLBindCol(hstmt, 2, SQL_DOUBLE, &usdollar, sizeof(usdollar), &indicators[1]);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Bind failure (column 2 - usdollar)");

    ret = SQLBindCol(hstmt, 3, SQL_DOUBLE, &low_limit, sizeof(low_limit), &indicators[2]);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Bind failure (column 3 - low_limit)");

    ret = SQLBindCol(hstmt, 4, SQL_DOUBLE, &high_limit, sizeof(high_limit), &indicators[3]);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Bind failure (column 4 - high_limit)");

    /* Execute the query */
    ret = SQLExecute(hstmt);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "SQLExecute failure");
    NumRows = 0;

    for (;;) 
    {
	/* 
	// main loop: report whenever it appears a value has gone outside
	// the alarm limits or come back within them..
	*/

	ret = SQLFetchScroll(hstmt, SQL_FETCH_FIRST, 0);
	i = 0;

	while (ret == SQL_SUCCESS)
	{ 
	    int oldalm, newalm;
	    oldalm = ((i >= NumRows) ? UNKNOWN_ALARM : Rows[i]);
	    newalm = ((usdollar > high_limit) ? HI_ALARM :
		          ((usdollar < low_limit) ? LO_ALARM : NO_ALARM));
	    if (newalm != oldalm) 
	    {
		if (oldalm == UNKNOWN_ALARM) 
		{
		    printf("Row Added - Code: %s, 1 Dollar buys: %0.2lf. Limits - Low: %0.2lf High: %0.2lf\n",
			   code, usdollar, low_limit, high_limit);
		}
		else if (newalm == HI_ALARM) 
		{
		    printf("*** ALARM *** : %s has risen above the high alarm limit %0.2lf at %0.2lf.\n",
			   code, high_limit, usdollar);
		}	  
		else if (newalm == LO_ALARM)
		{
		    printf("*** ALARM *** : %s has dropped below the low alarm limit %0.2lf at %0.2lf.\n",
			   code, low_limit, usdollar);
		}
		else if (oldalm == LO_ALARM)  
		{
		    printf("--- clear --- : %s has risen above the low alarm limit %0.2lf at %0.2lf.\n",
			   code, low_limit, usdollar);
		}
		else if (oldalm == HI_ALARM)  
		{
		    printf("--- clear --- : %s has dropped below the high alarm limit %0.2lf at %0.2lf.\n",
			   code, high_limit, usdollar);
		}
		else
		{  
		    printf("%s lies within limits (%0.2lf, %0.2lf) at %0.2lf.\n",
			   code, low_limit, high_limit, usdollar);
		}
		
		Rows[i] = newalm;
	    }
	    ++i;
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_NEXT, 0);
	}
	NumRows = i;

	/* Wait for something to happen - which in this case could either be 
	// a loss of connection or a delta coming through.
	*/

	if (WaitForIt(henv) == SQL_API_SQLDISCONNECT) break;
    }

    /* Free the statement handle */
    ret = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to free statement handle");

    /* Disconnect from database */
    ret = SQLDisconnect(hdbc);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to disconnect from the database");

    /* Free the connection handle */
    ret = SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to free connection handle");

    /* Free the environment handle */
    ret = SQLFreeHandle(SQL_HANDLE_ENV, henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to free environment handle");

    return 0;
}


/*------------------------------- End of File -------------------------------*/

