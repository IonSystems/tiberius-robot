/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2001-2015 by Enea Software AB
//		All Rights Reserved
// Authors:	Nigel Day, Andy England
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


/*------------------------------------------------------------------------------
// Includes
//----------------------------------------------------------------------------*/

/* On Windows we need to include windows.h */
#if defined(WIN32)
#include <windows.h>
#endif

/* Include standard header files */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/* Include the ODBC header files */
#include <sql.h>
#if !defined(ODBC_STD)
#include "sqlext.h"
#include "sqlpoly.h"
#endif

/*------------------------------------------------------------------------------
// Useful macros
//----------------------------------------------------------------------------*/

#define FALSE 0
#define TRUE 1

/* Longest column name we can handle */
#define MAX_COLUMN_NAME         256

/* Longest string value length we can handle */
#define MAX_STRING_LENGTH       256

/* Longest binary value length we can handle */
#define MAX_BINARY_LENGTH       256

/* Longest diagnostic message we can handle */
#define MAX_DIAG_MSG		256

/* Maximum number of currencies we want to deal with */
#define MAX_CURRENCIES		100

/*------------------------------------------------------------------------------
// Global variables
//----------------------------------------------------------------------------*/

/* Buffer for holding bookmark - know that 4 bytes is big enough */
SQLUINTEGER		Bookmark;

/* Array for holding row status */
SQLUSMALLINT		RowStatusArray[1];

/* Number of columns in the result set */
SQLSMALLINT		ColumnCount;

/* Array for holding column status */
SQLUSMALLINT		ColumnStatusArray[5];

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
// Fetch and display all rows for a statement
//----------------------------------------------------------------------------*/

void fetch_all_data(
    SQLHSTMT            hstmt)
{
    SQLRETURN		ret;
    SQLUINTEGER		bookmark;
    SQLCHAR		code[MAX_STRING_LENGTH];
    SQLCHAR		market[MAX_STRING_LENGTH];
    SQLDOUBLE		usd;
    SQLLEN		length;

    /* Go to the first row in the result set. */
    ret = SQLFetchScroll(hstmt, SQL_FETCH_FIRST, 0);

    while (ret != SQL_NO_DATA)
    {
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	/* If we wanted to store results in our own data structures, then we */
	/* could use the bookmarks as indexes on these structures, since when */
	/* deltas come through we can find the bookmarks of the rows that have */
	/* been added, deleted or altered. The following two lines show how we */
	/* can find the bookmark of the current row, if needed; in this demo,  */
	/* though, we do nothing with the value. */
	ret = SQLGetData(hstmt, 0, SQL_C_BOOKMARK, &bookmark, 0, &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of bookmark column");

	/* Retrieve the currency name and current value of the USD attribute, */
	/* and print them. If we had created out own data structures, we */
	/* could use the calls below to store the information directly into */
	/* the data structure for the current row. */
	ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");

	ret = SQLGetData(hstmt, 2, SQL_C_DOUBLE, &usd, 0, &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usd column");

	if (ColumnCount > 2)
	{
	    /* Retrieve the market name. */
	    ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &market, MAX_STRING_LENGTH, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of market column");

	    printf("Row Added - Market: %s, Code: %s, 1 Dollar buys: %lf.\n", market, code, usd);
	}
	else
	{
	    printf("Row Added - Code: %s, 1 Dollar buys: %lf.\n", code, usd);
	}

	/* Move onto the next undeleted row. If fetch_all_data is only called */
	/* after the active query is first set up, we will iterate through the */
	/* initial result set. If called at other times, we will iterate through */
	/* the current contents of the result set, skipping rows that hold a */
	/* representation of recently-deleted rows - such rows can only be visited */
	/* once, via their bookmark, and then the space is recovered. */
	ret = SQLFetchScroll(hstmt, SQL_FETCH_NEXT, 0);
    }
}

/*------------------------------------------------------------------------------
// Fetch and display a single row for a statement
//----------------------------------------------------------------------------*/

void fetch_by_bookmark(
    SQLHSTMT            hstmt)
{
    SQLRETURN		ret;  
    SQLCHAR		code[MAX_STRING_LENGTH];
    SQLCHAR		market[MAX_STRING_LENGTH];
    SQLDOUBLE		usd;
    SQLLEN		length;

    switch (RowStatusArray[0])
    {
    case SQL_ROW_ADDED:
	{
	    /* The row is a new one; retrieve the currency name and current USD value, */
	    /* and print them. */
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	    ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");

	    ret = SQLGetData(hstmt, 2, SQL_C_DOUBLE, &usd, 0, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usd column");

	    if (ColumnCount > 2)
	    {
		ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &market, MAX_STRING_LENGTH, &length);
		check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of market column");

		printf("Row Added - Market: %s, Code: %s, 1 Dollar buys: %lf.\n", market, code, usd);
	    }
	    else
	    {
		printf("Row Added - Code: %s, 1 Dollar buys: %lf.\n", code, usd);
	    }
	}
	break;

    case SQL_ROW_UPDATED:
	{
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	    if (ColumnStatusArray[2] == SQL_COLUMN_UPDATED)
	    {
		/* USD value changed - so report it. note that in a 'real' application, we */
		/* would have saved away previously-noted values in one of our own data */
		/* structures, indexed by the bookmark for quick access; here, though, we */
		/* can simply retrieve the currency name from the result set maintained by */
		/* the client library, and combine this with the new usd value to produce */
		/* the message we are going to print out. */
		ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
		check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");
		ret = SQLGetData(hstmt, 2, SQL_C_DOUBLE, &usd, 0, &length);
		check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usd column");

		if (ColumnCount > 2)
		{
		    ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &market, MAX_STRING_LENGTH, &length);
		    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of market column");

		    printf("Market: %s, Code: %s, 1 US Dollar now buys %lf.\n", market, code, usd);
		}
		else
		{
		    printf("Code: %s, 1 US Dollar now buys %lf.\n", code, usd);
		}
	    }
	}
	break;

    case SQL_ROW_DELETED:
	{
	    /* The row has been deleted - but the space used in the client-side copy */
	    /* of the result set is not recovered until we have had a chance to visit */
	    /* visit it and get back the previously-reported values. */
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");
	    ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column for deleted row");
	    ret = SQLGetData(hstmt, 2, SQL_C_DOUBLE, &usd, 0, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usd column");

	    if (ColumnCount > 2)
	    {
		ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &market, MAX_STRING_LENGTH, &length);
		check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of market column for deleted row");

		printf("Market: %s, currency %s removed from resultset\n", market, code);
	    }
	    else
	    {
		printf("Currency %s removed from resultset\n", code);
	    }
	}
	break;
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
    int			ft = FALSE;

    /* Check we have the correct number of arguments */
    if (argc > 3)
    {
	fprintf(stderr, "usage: %s [<data service> [FT]]\n", argv[0]);
	return 1;
    }

    /* Check we have a service argument */
    if (argc > 1)
    {
	service = argv[1];
    }

    /* Check we have FT option */
    if (argc > 2)
    {
	if (strcmp(argv[2], "FT") == 0) ft = TRUE;
    }

    /* Allocate an environment handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate environment handle");

#if !defined(ODBC_STD)
    /* Set the ODBC version used */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    check_success (ret, SQL_HANDLE_ENV, henv, "Failed to set ODBC version");
#endif

    /* Enable async events */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to enable async events");

    /* Allocate a conection handle */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate connection handle");

    if (ft)
    {
	printf("Connecting to %s Fault Tolerant...\n", service);

	/* Enable FT */
	ret = SQLSetConnectAttr(hdbc, SQL_ATTR_POLY_FT_ENABLE, (SQLPOINTER)SQL_POLY_FT_ENABLE_ON, 0);
	check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to enable FT");

	/* Set FT attributes */
	ret = SQLSetConnectAttr(hdbc, 
				SQL_ATTR_POLY_FT_HEALTHCHECK_INTERVAL, 
				(SQLPOINTER)1000, 
				0); 
	ret = SQLSetConnectAttr(hdbc,
				SQL_ATTR_POLY_FT_HEALTHCHECK_TIMEOUT, 
				(SQLPOINTER)1000, 
				0) && ret;
	ret = SQLSetConnectAttr(hdbc,
				SQL_ATTR_POLY_FT_RECONNECTION_TIMEOUT, 
				(SQLPOINTER)1000, 
				0) && ret;
	ret = SQLSetConnectAttr(hdbc, 
				SQL_ATTR_POLY_FT_RECONNECTION_INTERVAL, 
				(SQLPOINTER)1000, 
				0) && ret;
	ret = SQLSetConnectAttr(hdbc, 
				SQL_ATTR_POLY_FT_RECONNECTION_RETRIES, 
				(SQLPOINTER)1000, 
				0) && ret;
	check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to set FT options");
    }
    else
	printf("Connecting to %s...\n", service);

    /* Connect to the database */
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to connect to the database");

    printf("Connected, now launch active query...\n");

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Use dynamic cursor */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set dynamic cursor");

    /* Enable async statement events */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to enable async events");

    /* A little trick - set maximum rows to MAX_CURRENCIES */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_MAX_ROWS, (SQLPOINTER)MAX_CURRENCIES, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set maximum rows");

    /* Execute the query */
    /* First try the aggregate case */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"select code,usdollar,market_name,id from currency,journalsession where id = market_id", SQL_NTS);
    if (ret != SQL_SUCCESS)
    {
	/* Try the standard currency table */
	ret = SQLExecDirect(hstmt, (SQLCHAR *)"select code,usdollar from currency", SQL_NTS);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to execute statement");
    }

    /* Number of result columns */
    ret = SQLNumResultCols(hstmt, &ColumnCount);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get number of result columns");

    /* Set the row status array */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_ROW_STATUS_PTR, RowStatusArray, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set row status ptr");

    /* Set the column status array */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_POLY_COLUMN_STATUS_PTR, ColumnStatusArray, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set column status ptr");

    /* Use bookmarks */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_USE_BOOKMARKS, (SQLPOINTER)SQL_UB_VARIABLE, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set variable-length bookmarks");

    /* Set fetch bookmark pointer */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_FETCH_BOOKMARK_PTR, &Bookmark, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set fetch bookmark ptr");

    /* Fetch and display initial result set */
    fetch_all_data(hstmt);
    printf("Delta complete - success.\n\n");

    /* Loop handling events */
    for (;;)
    {
	SQLUSMALLINT	functionId;
	SQLSMALLINT	handleType;
	SQLHANDLE	handle;

	/* Get the next event */
	while (SQLGetAsyncEvent(henv, &functionId, &handleType, &handle) == SQL_SUCCESS)
	{
	    switch (functionId)
	    {
	    case SQL_API_SQLDISCONNECT:
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

	    case SQL_API_SQLFETCH:
		/* Data has changed - fetch and display modified result set */
		while (SQLGetAsyncStmtEvent(hstmt) == SQL_SUCCESS)
		{
		    fetch_by_bookmark(hstmt);
		}

		printf("Delta complete - success.\n\n");
		break;

	    case SQL_API_SQLGETCONNECTATTR:
		/* Connection attribute has changed */
		{
		    SQLCHAR name[256];
		    SQLUINTEGER mode;

		    /* Get the service name being used */
		    ret = SQLGetConnectAttr(hdbc, SQL_ATTR_POLY_CONNECTION_NAME, (SQLPOINTER)name, sizeof(name), 0);
		    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get connection name");


		    /* If name is blank, connection is reconnecting */
		    if (name[0] == '\0')
		    {
			printf("Reconnecting\n");
			break;
		    }

		    /* Get the FT mode */
		    ret = SQLGetConnectAttr(hdbc, SQL_ATTR_POLY_FT_MODE, &mode, 0, 0);
		    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get FT mode");

		    printf("Connection: %s, mode: %d\n", name, (int)mode);
		}
		break;

	    default:
		fprintf(stderr, "Event %d not handled\n", functionId);
		break;
	    }
	}

	/* Generic function to wait for a Polyhedra message */
	/* This can be replaced by OS specific main loop */
	ret = SQLHandleMsg(henv);
	check_success(ret, SQL_HANDLE_ENV, henv, "Failed to handle message");
    }

    return 0;
}

/*------------------------------------------------------------------------------
// End of file
//----------------------------------------------------------------------------*/
