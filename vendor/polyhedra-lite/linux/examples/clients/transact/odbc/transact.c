/*------------------------------------------------------------------------------
// Project:	Polyhedra Demo Suite
// Copyright:	Copyright (C) 2002-2015 by Enea Software AB
//		All Rights Reserved
// Author:	Andy England
// Description:	transact example
//------------------------------------------------------------------------------
//
// This program illustrates the use of simple transactions.
// It connects to the database and then fires off a piece of SQL,
// as specified by the program argument. 
//
// The supplied value can be a single SQL DDL statement
// (eg, create table, create schema, drop table), OR one or more SQL DML
// statements (insert, delete or update) separated by semicolons, but should
// not include any select statement. 
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

/* Include the ODBC header files */
#include <sql.h>
#if !defined(ODBC_STD)
#include "sqlext.h"
#include "sqlpoly.h"
#endif

/*------------------------------------------------------------------------------
// Useful macros
//----------------------------------------------------------------------------*/

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
    char *		sql;
    char *		service = "8001";

    /* Check we have the correct number of arguments */
    if (argc < 2 || argc > 3)
    {
	fprintf(stderr, "usage: %s <sql> [<data service>]\n", argv[0]);
	return 1;
    }

    sql = argv[1];

    /* Check we have a service argument */
    if (argc > 2)
    {
	service = argv[2];
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

    printf("Connecting to port %s...\n", service);

    /* Connect to the database */
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to connect to the database");

    printf("Connected successfully. Start the transaction:\n%s\n", sql);

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Execute the query */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)sql, SQL_NTS);
    check_success (ret, SQL_HANDLE_STMT, hstmt, "Failed execute statement");
    printf("Transaction completed successfully.\n");

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
