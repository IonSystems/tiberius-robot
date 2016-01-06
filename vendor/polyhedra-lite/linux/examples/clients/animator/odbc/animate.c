/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2001-2015 by Enea Software AB
//		All Rights Reserved
// Authors:	Nigel Day, Andy England
// Description:	aniamte example
//------------------------------------------------------------------------------
//
// Uses the ODBC API to periodically change the contents of the currency table
// in the database to which it is connected.
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

/* On Windows we need to include windows.h and define sleep() */
#if defined(WIN32)
#include <windows.h>
#include <sys/timeb.h>
#else
#include <unistd.h>
#include <string.h>
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
#define MAX_CURRENCIES 100

/* Percentage limit on sawtooth walk */
#define LIMIT           10

/* Number of deciseconds between updates */
#define UPDATE_PERIOD   20

/*------------------------------------------------------------------------------
// Global variables
//----------------------------------------------------------------------------*/

/* Number of rows actually in this array */
int			NumRows;

struct
{
    double		usdollar;
    double		change;
}			Rows[MAX_CURRENCIES];

/*------------------------------------------------------------------------------
// Print error function called after any ODBC function has failed
//----------------------------------------------------------------------------*/

void print_error(
    int			ret, 
    SQLSMALLINT		handleType,
    SQLHANDLE		handle,
    const char *	errorMsg)
{
    fprintf(stderr, "%s\n", errorMsg);

    if (handle != SQL_NULL_HANDLE)
    {
	SQLSMALLINT	recNumber = 1;
	SQLINTEGER	nativeError;
	SQLCHAR		sqlState[6];
	SQLCHAR		msg[MAX_DIAG_MSG];
	SQLSMALLINT	actualLen;

	sqlState[5] = '\0';

	/* Get the diagnostics for the error */
	while (SQLGetDiagRec(handleType, handle, recNumber++, &sqlState[0],
			     &nativeError, &msg[0], MAX_DIAG_MSG, &actualLen) == SQL_SUCCESS)
	{
	    fprintf(stderr, "ODBC error: %s: %s (%d)\n", sqlState, msg, (int)nativeError);
	}
    }
}

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
// Get the current time
//----------------------------------------------------------------------------*/

double get_time()
{
#if defined(WIN32)
    struct _timeb tb;
    _ftime(&tb);

    return tb.time + (tb.millitm / 1000.0);
#else
    struct timeval tv;

    gettimeofday(&tv, 0);

    return tv.tv_sec + (tv.tv_usec / 1000000000.0);
#endif
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
    int			i;
    SQLCHAR		code[4];
    SQLDOUBLE		usdollar;
    SQLLEN		indicators[2];
    SQLINTEGER		value;

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

    indicators[0] = sizeof(code);
    indicators[1] = sizeof(usdollar);

    /* Allocate an environment handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate environment handle");

    /* Set event timeout */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_POLY_EVENT_TIMEOUT, (SQLPOINTER)500, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to set event timeout");

#if !defined(ODBC_STD)
    /* Set the ODBC version used */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to set ODBC version");
#endif

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
				SQL_ATTR_POLY_FT_HEALTHCHECK_INTERVAL, 
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
    printf("Connection made successfully.\n");

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Use dynamic cursor */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to make dynamic cursor");

    /* A little trick - set maximum rows to MAX_CURRENCIES */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_MAX_ROWS, (SQLPOINTER)MAX_CURRENCIES, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set maximum rows");

    /* Bind columns */
    ret = SQLBindCol(hstmt, 1, SQL_C_CHAR, &code, sizeof(code), &indicators[0]);
    check_success (ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");

    ret = SQLBindCol(hstmt, 2, SQL_C_DOUBLE, &usdollar, sizeof(usdollar), &indicators[1]);
    check_success (ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usdollar column");

    /* Execute the query */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"select code,usdollar from currency", SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to execute statement");

    /* For equivalence with Callback API version. */
    printf("Delta Complete\n");

    /* Set manual commit mode on the connection */
    ret = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to set manual commit mode");

    for (;;) 
    {
	double t;

	/* Main loop: iterate over the result set and perform a
	// weighted drunkard's walk on each element.
	*/

	printf("Start update through active query\n");

	ret = SQLFetchScroll(hstmt, SQL_FETCH_FIRST, 0);
	i = 0;

	while (ret == SQL_SUCCESS)
	{
	    /* Work out the change we wish to apply */
	    i++;
	    if (i > NumRows)
	    {
		Rows[i].usdollar = usdollar;
		Rows[i].change = usdollar * 0.01;
		printf("%d %s %lf\n", i, code, Rows[i].usdollar);
	    }

	    if (Rows[i].change > 0)
	    {
		if (usdollar + Rows[i].change > Rows[i].usdollar * 1.1) 
		{
		    printf("Upper limit crossed\n");
		    Rows[i].change = -Rows[i].change;
		}
	    }
	    else
	    {
		if (usdollar + Rows[i].change <= Rows[i].usdollar * 0.9)
		{
		    printf("Lower limit crossed\n");
		    Rows[i].change = -Rows[i].change;
		}
	    }

	    usdollar += Rows[i].change;

	    printf("Change usdollar field of %s by %lf to %lf\n", code, Rows[i].change, usdollar);

	    /* Ask the library to record the local change we have
	    // just made (to be done as part of a later transaction
	    // as we have turned off auto-commit)
	    */
	    ret = SQLSetPos(hstmt, 1, SQL_UPDATE, SQL_LOCK_NO_CHANGE);
	    /*check_success(ret, SQL_HANDLE_STMT, hstmt, "Problem with SQLSetPos");*/

	    /* Move to the next record */
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_NEXT, 0);
	}

	/* Cope with failures of either of the calls of SQLFetchScroll, which
	// will 'legitimately' fail when encountering the end of the result set.
	*/
	if (ret == SQL_ERROR)
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Problem when fetching");
	NumRows = i;

	/* If the table is not empty, commit the changes we have just set up. */

	if (i != 0)
	{
	    ret = SQLEndTran(SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
	    if (ret == SQL_SUCCESS)
	    {
		printf("Transaction complete\n");
	    }
	    else
	    {
		print_error(ret, SQL_HANDLE_DBC, hdbc, "Commit failure");
	    }

	    /* For equivalence with Callback API version. */
	    printf("Delta Complete\n");
	}

	/* Wait 2 seconds */
	t = get_time();

	do
	{
	    ret = SQLHandleMsg(henv);
	    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to handle message");

	    ret = SQLGetConnectAttr(hdbc, SQL_ATTR_CONNECTION_DEAD, &value, sizeof(SQLINTEGER), 0);
	    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to get connection attribute");

	} while ((value == SQL_CD_FALSE) && (t + 2 > get_time()));

	if (value == SQL_CD_TRUE) break;
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

/*------------------------------------------------------------------------------
// End of file
//----------------------------------------------------------------------------*/
