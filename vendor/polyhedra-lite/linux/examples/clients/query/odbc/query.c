/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2001-2015 by Enea Software AB
//		All Rights Reserved
// Authors:	Nigel Day, Andy England
// Description:	query example
//------------------------------------------------------------------------------
//
// This program illustrates how a static query may be launched using the 
// Polyhedra ODBC API.
//
// When run, the program connects to the indicated database or to the database 
// "8001" if no argument is given. The query "select * from currency" is then 
// run, and the results displayed.
//
// In case of error, the 'exit' function is called; on embedded platforms that 
// do not tidy up when tasks terminate, it would be more appropriate to alter 
// the logic of the program to leave cleanly via the main routine. As such 
// coding merely complicates the logic of the program without illustrating any 
// new features of the use of the Polyhedra ODBC library, the 'lazy' approach 
// has been adopted here.
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
#endif

/* Include standard header files */
#include <stdlib.h>
#include <stdio.h>

/* Include the ODBC header files */
#include <sql.h>
#if !defined(ODBC_STD)
#include <sqlext.h>
#include <sqlpoly.h>
#endif

/*------------------------------------------------------------------------------
// Useful macros
//----------------------------------------------------------------------------*/

/* Longest column name we can handle */
#define MAX_COLUMN_NAME		256

/* Longest string value length we can handle */
#define MAX_STRING_LENGTH	256

/* Longest diagnostic message we can handle */
#define MAX_DIAG_MSG		256

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

    /* Check we have a service argument */
    if (argc == 2)
    {
	service = argv[1];
    }
    else if (argc > 2)
    {
	fprintf(stderr, "usage: %s [<data service>]\n", argv[0]);
	return 1;
    }

    /* Allocate an environment handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate environment handle");

#if !defined(ODBC_STD)
    /* Set the ODBC version used */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to set ODBC version");
#endif

    /* Allocate a conection handle */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate connection handle");

    printf("Connecting to database at %s...\n", service);

    /* Connect to the database */
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to connect to the database");

    printf("Connected, now launch query...\n");

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Execute the query  */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"select * from currency", SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed execute statement");

    /* Display the result set by fetching a row at a time */
    while ((ret = SQLFetch(hstmt)) == SQL_SUCCESS)
    {
	char		code[4];
	char		country[100];
	char		name[100];
	double		usdollar;
	SQLLEN		length;

	ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, sizeof(code), &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");

	ret = SQLGetData(hstmt, 2, SQL_C_CHAR, &country, sizeof(country), &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of country column");

	ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &name, sizeof(name), &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of name column");

	ret = SQLGetData(hstmt, 4, SQL_C_DOUBLE, &usdollar, sizeof(double), &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usdollar column");

	printf("Currency code: %s: 1 US Dollar buys %0.2lf %s %s.\n", code, usdollar, country, name);
    }

    printf("All rows returned.\n");

    /* Close the cursor */
    ret = SQLCloseCursor(hstmt);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Faied to close cursor");

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
