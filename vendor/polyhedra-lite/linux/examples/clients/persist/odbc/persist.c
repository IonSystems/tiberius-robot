/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2002-2015 by Enea Software AB
//		All Rights Reserved
// Author:	Andy England
// Description:	persist example
//------------------------------------------------------------------------------
//
// Source code for the data persistence example
// This takes a single parameter, being the maximum size of the file.
// It launches an active query on journalcontrol - which holds the size of the
// load_file. When the load_file crosses the the size boundary, then a "save"
// is issued to create a new snapshot of the data in memory.
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

/* Longest diagnostic message we can handle */
#define MAX_DIAG_MSG		256

/*------------------------------------------------------------------------------
// Global variables
//----------------------------------------------------------------------------*/

/* Buffer for holding bookmark - know that 4 bytes is big enough */
SQLUINTEGER		Bookmark;

/* Array for holding row status */
SQLUSMALLINT		RowStatusArray[1];

/* Maximum size of load file */
long			MaxFileSize;
long			SizeAtSave = 0;

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
	    SQLSMALLINT recNumber = 1;
	    SQLINTEGER nativeError;
	    SQLCHAR sqlState[6];
	    SQLCHAR msg[MAX_DIAG_MSG];
	    SQLSMALLINT actualLen;

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
// Save database
//----------------------------------------------------------------------------*/

void save_database(
    SQLHDBC		hdbc,
    long                current_size)
{
    SQLRETURN		ret;
    SQLHSTMT		hstmt;

    /* The maximum allowable filesize has been exceeded.. Issue a save into. */
    printf("File size has reached %ld, so time to create new load_file.\n", current_size);
    
    SizeAtSave = current_size;

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Enable safe-commit mode */
    ret = SQLSetConnectAttr(hdbc, SQL_ATTR_POLY_FT_SAFE_COMMIT_ENABLE, (SQLPOINTER)SQL_POLY_FT_SAFE_COMMIT_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to enable safe-commit");

    /* Execute the statement */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"save", SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed execute statement");

    printf("Save into completed.\n");

    /* Free the statement handle */
    ret = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to free statement handle");
}

/*------------------------------------------------------------------------------
// Fetch and display all rows for a statement
//----------------------------------------------------------------------------*/

void fetch_all_data(
    SQLHDBC		hdbc,
    SQLHSTMT            hstmt)
{
    SQLRETURN		ret;
    SQLLEN		length;

    ret = SQLFetchScroll(hstmt, SQL_FETCH_FIRST, 0);

    while (ret != SQL_NO_DATA)
    {
	SQLINTEGER	file_size;

	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	ret = SQLGetData(hstmt, 2, SQL_C_LONG, &file_size, 0, &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of file_size column");

	if (length == SQL_NULL_DATA)
	{
	    printf("no FileSize??\n");
	}
	else
	{
	    /* SizeAtSave used to prevent false 'save into's issued */
	    /* as filesize fluctuates during save into operation. */
	    if (file_size < SizeAtSave)
	    {
		/* Okay to issue a 'save into' */
		SizeAtSave = 0;
	    }

	    if (file_size > MaxFileSize && SizeAtSave == 0)
	    {
		save_database(hdbc, file_size);
	    }
	}

	ret = SQLFetchScroll(hstmt, SQL_FETCH_NEXT, 0);
    }
}

/*------------------------------------------------------------------------------
// Fetch and display a single row for a statement
//----------------------------------------------------------------------------*/

void fetch_by_bookmark(
    SQLHDBC		hdbc,
    SQLHSTMT            hstmt)
{
    SQLRETURN		ret;
    SQLLEN		length;

    switch (RowStatusArray[0])
    {
    case SQL_ROW_ADDED:
    case SQL_ROW_UPDATED:
	{
	    SQLINTEGER	file_size;

	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	    ret = SQLGetData(hstmt, 2, SQL_C_LONG, &file_size, 0, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of file_size column");

	    if (length == SQL_NULL_DATA)
	    {
		printf("no FileSize??\n");
	    }
	    else
	    {
		/* SizeAtSave used to prevent false 'save into's issued */
		/* as filesize fluctuates during save into operation. */
		if (file_size < SizeAtSave)
		{
		    /* Okay to issue a 'save into' */
		    SizeAtSave = 0;
		}

		if (file_size > MaxFileSize && SizeAtSave == 0)
		{
		    save_database(hdbc, file_size);
		}
	    }
	}
	break;

    case SQL_ROW_DELETED:
	{
	    fprintf(stderr, "Journal control record removed!\n");
	    exit(1);
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
    SQLSMALLINT		columnCount;
    char *		service = "8001";
    int			ft = FALSE;

    /* Check we have the correct number of arguments */
    if (argc < 2 || argc > 3)
    {
	fprintf(stderr, "usage: %s <max size of load_file> [<data service>]\n", argv[0]);
	return 1;
    }

    MaxFileSize = atol(argv[1]);

    /* Check we have a service argument */
    if (argc > 2)
    {
	service = argv[2];
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

    printf("Connecting to database at %s...\n", service);

    /* Connect to the database */
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to connect to the database");

    printf("Connected, now launch active query on journal control...\n");
    printf("and monitor file_size for it reaching %ld\n", MaxFileSize);

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Use dynamic cursor */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, 0);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to set dynamic cursor");

    /* Enable async statement events */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to enable async events");

    /* Execute the query */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"select id,file_size from journalcontrol", SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed execute statement");

    /* Set the row status array */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_ROW_STATUS_PTR, RowStatusArray, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set row status ptr");

    /* Obtain the number of result columns */
    ret = SQLNumResultCols(hstmt, &columnCount);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed obtain number of columns in result set");

    /* Use bookmarks */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_USE_BOOKMARKS, (SQLPOINTER)SQL_UB_VARIABLE, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set variable-length bookmarks");

    /* Set fetch bookmark pointer */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_FETCH_BOOKMARK_PTR, &Bookmark, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set fetch bookmark ptr");

    /* Fetch and display initial result set */
    fetch_all_data(hdbc, hstmt);

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

	    case SQL_API_SQLEXECDIRECT:
	    case SQL_API_SQLFETCH:
		/* Data has changed - fetch and display modified result set */
		while (SQLGetAsyncStmtEvent(hstmt) == SQL_SUCCESS)
		{
		    fetch_by_bookmark(hdbc, hstmt);
		}
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
