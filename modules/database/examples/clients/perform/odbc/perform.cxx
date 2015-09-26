/*-+-----------------------------------------------------------------------+-//
//									     //
//             P O L Y H E D R A    T E S T    L I B R A R Y		     //
//									     //
//                Copyright (C) 1999-2014 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------//
//	 
//-+ Filename	 : perform.cxx
//-+ Description : performance test application - ODBC version
//
//-+ CVSID	 : $Id: perform.cxx,v 1.13 2014/05/28 10:13:41 alan Exp $
//
//-+-----------------------------------------------------------------------+-*/

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

#define RAW
#define STANDARD
//#define EXTRA


#include "common.hxx"


#define INSERT_INTO_TEST1_PARAM_SQL (SQLCHAR*) \
    "INSERT INTO test1 (id, col2, col3, col4, col5) VALUES (?, ?, ?, ?, ?)"


#define INSERT_INTO_TEST2_PARAM_SQL       \
    (SQLCHAR*)                            \
    "INSERT INTO test2"                   \
    "( id,    col2,  col3,  col4,  col5"  \
    ", col6,  col7,  col8,  col9,  col10" \
    ", col11, col12, col13, col14, col15" \
    ", col16, col17, col18, col19, col20" \
    ", col21, col22, col23, col24, col25" \
    ", col26, col27, col28, col29, col30" \
    ", col31, col32, col33, col34, col35" \
    ", col36, col37, col38, col39, col40" \
    ", col41, col42, col43, col44, col45" \
    ", col46, col47, col48, col49, col50" \
    ") VALUES"                            \
    "( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      \
    ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      \
    ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      \
    ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      \
    ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      \
    ")"


#define SELECT_FROM_TEST1_SQL \
    (SQLCHAR*)                \
    "SELECT id,col2,col3,col4,col5 FROM test1"


#define SELECT_FROM_TEST1_PARAM_SQL \
    (SQLCHAR*)                      \
    "SELECT id,col2,col3,col4,col5 FROM test1 WHERE id=?"


#define SELECT_FROM_TEST2_PARAM_SQL \
    (SQLCHAR*)                      \
    "SELECT * FROM test2 WHERE id=?"


#define UPDATE_TEST1_PARAM_SQL \
    (SQLCHAR*)                 \
    "UPDATE test1 set col2=?, col3=?, col4=?, col5=? WHERE id=?"


#define UPDATE_TEST2_PARAM_SQL                          \
    (SQLCHAR*)                                           \
    "UPDATE test2 set col2=?,  col3=?,  col4=?,  col5=?" \
    "     ,  col6=?,  col7=?,  col8=?,  col9=?, col10=?" \
    "     , col11=?, col12=?, col13=?, col14=?, col15=?" \
    "     , col16=?, col17=?, col18=?, col19=?, col20=?" \
    "     , col21=?, col22=?, col23=?, col24=?, col25=?" \
    "     , col26=?, col27=?, col28=?, col29=?, col30=?" \
    "     , col31=?, col32=?, col33=?, col34=?, col35=?" \
    "     , col36=?, col37=?, col38=?, col39=?, col40=?" \
    "     , col41=?, col42=?, col43=?, col44=?, col45=?" \
    "     , col46=?, col47=?, col48=?, col49=?, col50=?" \
    " WHERE id=?"



#define DELETE_FROM_TEST1_PARAM_SQL \
    (SQLCHAR*)                      \
    "DELETE FROM test1 WHERE id=?"

#define DELETE_FROM_TEST2_PARAM_SQL \
    (SQLCHAR*)                      \
    "DELETE FROM test2 WHERE id=?"


#define DELETE_FROM_TEST1_SQL \
    (SQLCHAR*)                \
    "DELETE FROM test1"

#define DELETE_FROM_TEST2_SQL \
    (SQLCHAR*)                \
    "DELETE FROM test2"


#define DROP_TABLE_TEST1_SQL \
    (SQLCHAR*)               \
    "DROP TABLE test1"

#define DROP_TABLE_TEST2_SQL \
    (SQLCHAR*)               \
    "DROP TABLE test2"


// ----------------------------------------------------------------------------
// pick up more headers
// ----------------------------------------------------------------------------


#include <sql.h>
#include <sqlext.h>
//#include <sqlpoly.h>


// ----------------------------------------------------------------------------
// more useful macros, constants and functions
// ----------------------------------------------------------------------------

/* Check an SQL return code 
*/

#define check_success(r, t, h)	\
        check_return_line (SQL_SUCCESS, (r), (t), (h), 0, __FILE__, __LINE__)
#define check_error(r, t, h, s)	\
	check_return_line (SQL_ERROR, (r), (t), (h), (s), __FILE__, __LINE__)
#define check_success_with_info(r, t, h, s) \
	check_return_line (SQL_SUCCESS_WITH_INFO, (r), (t), (h), (s), __FILE__, __LINE__)

void check_return_line ( SQLRETURN    expectedRet,
                         SQLRETURN    ret,
                         SQLSMALLINT  handleType,
                         SQLHANDLE    handle,
                         const char * state,
                         const char * filename,
                         int          lineno
                       )
{
    if (ret != expectedRet)
    {
        printf ( "%s: Function did not return expected return code "
                 "(%d, not %d)\n", 
                 CurrentTest, ret, expectedRet
               );
        if (ret == SQL_ERROR && handle != SQL_NULL_HANDLE)
        {
            SQLCHAR     msg[256];
            SQLCHAR     sqlState[6];
            SQLINTEGER  nativeError;
            SQLSMALLINT actualLen;

            SQLGetDiagRec ( handleType, handle, 1, &sqlState[0], &nativeError, 
                            &msg[0], 256, &actualLen
                          );
            sqlState[5] = '\0';
            printf ( "%s: %s: %s (%d)\n", CurrentTest, sqlState, 
                     msg, (int)nativeError
                   );
        }
        fail (filename, lineno);
    }
    else if (state != 0)
    {
        SQLCHAR     msg[256];
        SQLCHAR     sqlState[6];
        SQLINTEGER  nativeError;
        SQLSMALLINT actualLen;

        SQLGetDiagRec ( handleType, handle, 1, &sqlState[0], &nativeError, 
                        &msg[0], 256, &actualLen
                      );
        sqlState[5] = '\0';
        if (strcmp ((char *)sqlState, state))
        {
            printf ( "%s: %s: %s (%d)\n", CurrentTest, sqlState, 
                     msg, (int)nativeError
                   );
            fail (filename, lineno);
        }
    }
}

void alloc_env(SQLHANDLE* phenv)
{
    SQLRETURN ret;

    /* Allocate an env handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, phenv);
    check_success(ret, SQL_HANDLE_ENV, *phenv);
    assert(*phenv != SQL_NULL_HANDLE);

    /* Set ODBC version to be used */
    /* We have to do this before we can allocate a dbc handle */
    ret = SQLSetEnvAttr ( *phenv, SQL_ATTR_ODBC_VERSION,
                          (SQLPOINTER)SQL_OV_ODBC3, SQL_IS_INTEGER
                        );
    check_success (ret, SQL_HANDLE_ENV, phenv);
}

/* Allocate a connection 
*/
void alloc_connect ( SQLHANDLE   henv,
                     SQLHANDLE * phdbc
                   )
{
    SQLRETURN ret;

    /* Allocate a dbc handle 
    */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, phdbc);
    check_success (ret, SQL_HANDLE_ENV, henv);
    assert (*phdbc != SQL_NULL_HANDLE);
}

/* Allocate a statement handle 
*/
void alloc_stmt ( SQLHANDLE   hdbc,
                  SQLHANDLE * phstmt
                )
{
    SQLRETURN ret;

    ret = SQLAllocHandle (SQL_HANDLE_STMT, hdbc, phstmt);
    check_success (ret, SQL_HANDLE_DBC, hdbc);
    assert (*phstmt != SQL_NULL_HANDLE);
}

/* Allocate a descriptor handle 
*/
void alloc_desc ( SQLHANDLE  hdbc,
                  SQLHANDLE * phdesc
                )
{
    SQLRETURN ret;

    ret = SQLAllocHandle ( SQL_HANDLE_DESC, hdbc, phdesc);
    check_success (ret, SQL_HANDLE_DBC, hdbc);
    assert (*phdesc != SQL_NULL_HANDLE);
}

/* Free a statement handle 
*/
void free_stmt (SQLHANDLE hstmt)
{
    SQLRETURN ret;

    ret = SQLFreeHandle (SQL_HANDLE_STMT, hstmt);
    check_success (ret, SQL_HANDLE_STMT, hstmt);
}

/* Free a descriptor handle 
*/
void free_desc (SQLHANDLE hdesc)
{
    SQLRETURN ret;

    ret = SQLFreeHandle (SQL_HANDLE_DESC, hdesc);
    check_success (ret, SQL_HANDLE_DESC, hdesc);
}


/* Connect to the DB:
   We have to do this before we can allocate
   either a stmt or desc handle 
*/
void do_connect ( SQLHANDLE   henv,
                  SQLHANDLE * phdbc,
		  SQLCHAR   * dsn
                )
{
    SQLRETURN ret;

    alloc_connect (henv, phdbc);

    ret = SQLConnect (*phdbc, dsn, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);

    if (ret!=SQL_SUCCESS)
    {
        printf ("\tThe database must be already running.\n");
        printf ("\tStart the database using the command, rtrdb empty\n\n");
    }
}


/* Free a connection 
*/
void free_connect ( SQLHANDLE henv,
		    SQLHANDLE hdbc
                  )
{
    if (hdbc != SQL_NULL_HANDLE)
        SQLFreeHandle (SQL_HANDLE_DBC, hdbc);

    if (henv != SQL_NULL_HANDLE)
        SQLFreeHandle (SQL_HANDLE_ENV, henv);
}


/* Disconnect a connection 
*/
void do_disconnect ( SQLHANDLE hdbc
                   )
{
    SQLRETURN ret = SQLDisconnect (hdbc);
    check_success (ret, SQL_HANDLE_DBC, hdbc);
    free_connect (SQL_NULL_HANDLE, hdbc);
}


/* Create the test tables, or find out how big they are
*/
SQLINTEGER create_table (SQLHANDLE hdbc, 
                         const char* tablename,
                         const char* createstring1, 
                         const char* createstring2,
                         const char* teststring,
                         int         strict)
{
    SQLRETURN  ret;
    SQLHANDLE  hstmt = SQL_NULL_HANDLE;
    SQLINTEGER rowct = 0;

    alloc_stmt (hdbc, &hstmt);
    ret = SQLExecDirect (hstmt, (SQLCHAR*)createstring1, SQL_NTS);

    if (ret != SQL_SUCCESS)
    {
        // the table may already exist - or it may be a non-polyhedra
        // server, and thus won't accept extensions such as 'persistent'.
        // try the alternate syntax.

        if (createstring2 != 0)
        {
            free_stmt (hstmt);
            alloc_stmt (hdbc, &hstmt);

            ret = SQLExecDirect (hstmt, (SQLCHAR*)createstring2, SQL_NTS);
        }

        if (strict == TRUE)
        {
            check_success (ret, SQL_HANDLE_STMT, hstmt);
        }
        else if (ret != SQL_SUCCESS)
        {
            // the table probably already exists - how many records?

            SQLLEN length;

            free_stmt (hstmt);
            alloc_stmt (hdbc, &hstmt);
            ret = SQLExecDirect ( hstmt,(SQLCHAR*)teststring, SQL_NTS);
            check_success (ret, SQL_HANDLE_STMT, hstmt);
            ret = SQLFetch (hstmt);
            check_success (ret, SQL_HANDLE_STMT, hstmt);
            ret = SQLGetData (hstmt, 1, SQL_C_SLONG, &rowct, sizeof(rowct), &length);
            check_success (ret, SQL_HANDLE_STMT, hstmt);
        }
    }
    free_stmt (hstmt); 
    //fprintf (stderr, "(table %s holds %d records)\n", tablename, rowct);
    return rowct;
}

SQLINTEGER create_table_test1 (SQLHANDLE hdbc, int strict = FALSE)
{
    return create_table (hdbc, "test1", 
                         CREATE_TABLE_TEST1_SQL, 
                         CREATE_TABLE_TEST1_STANDARD_SQL, 
                         "SELECT COUNT(*) FROM test1", 
                         strict
                        );
}

int create_table_test2 (SQLHANDLE hdbc, int strict = FALSE)
{
    return create_table (hdbc, "test2",
                         CREATE_TABLE_TEST2_SQL, 
                         CREATE_TABLE_TEST2_STANDARD_SQL, 
                         "SELECT COUNT(*) FROM test2",
                         strict
                        );
}


/* Drop the test tables, without checking return codes as they
   may not have been created!
*/
void drop_test_tables (SQLHANDLE hdbc)
{
    SQLRETURN ret;
    SQLHANDLE hstmt = SQL_NULL_HANDLE;

    alloc_stmt (hdbc, &hstmt);
    ret = SQLExecDirect (hstmt, DELETE_FROM_TEST1_SQL, SQL_NTS);
    free_stmt (hstmt);

    alloc_stmt (hdbc, &hstmt);
    ret = SQLExecDirect (hstmt, DELETE_FROM_TEST2_SQL, SQL_NTS);
    free_stmt (hstmt);

    alloc_stmt (hdbc, &hstmt);
    ret = SQLExecDirect (hstmt, DROP_TABLE_TEST1_SQL, SQL_NTS);
    free_stmt (hstmt);

    alloc_stmt (hdbc, &hstmt);
    ret = SQLExecDirect (hstmt, DROP_TABLE_TEST2_SQL, SQL_NTS);
    free_stmt (hstmt);
}


// ----------------------------------------------------------------------------
// driver and database version info
// ----------------------------------------------------------------------------


/* Whether using Driver Manager 
*/
int UsingDM = 0;


/* Driver/library version information 
*/
int ODBC_major_number = 0;
int ODBC_minor_number = 0;
int ODBC_build_number = 0;


void set_using_dm (SQLHANDLE henv)
    /* 
       find out if we are talking directly to the Polyhedra library, or using the
       Windows ODBC driver manager (in which case, performance will be affected).
    */    
{
    SQLRETURN ret;
    SQLHANDLE hdbc = SQL_NULL_HANDLE;
    char stringVal[MAX_STRING_BUFFER_LENGTH];
    SQLSMALLINT length;

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    /* If we are using the Driver Manager we will get a valid version number */
    ret = SQLGetInfo ( hdbc, SQL_DM_VER, 
                       stringVal, MAX_STRING_BUFFER_LENGTH, 
                       &length
                     );
    check_success (ret, SQL_HANDLE_DBC, hdbc);
    assert ((unsigned int)length == strlen("##.##.####.####"));
    UsingDM = (strcmp (stringVal, "??.??.????.????") != 0);

    do_disconnect (hdbc);
}


void display_version (SQLHANDLE henv)
{
    SQLRETURN ret;
    SQLHANDLE hdbc = SQL_NULL_HANDLE;
    char stringVal[MAX_STRING_BUFFER_LENGTH];
    SQLSMALLINT length;

    set_test ("software versions");

    printf ("\tapplication version: $Revision: 1.13 $\n");

    set_using_dm (henv);
    printf ("\tusing driver manager? %s.\n", (UsingDM ? "yes" : "no"));

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    // find out the version number of the ODBC library we are using.

    ret = SQLGetInfo (hdbc, SQL_DRIVER_VER, 
                      stringVal, MAX_STRING_BUFFER_LENGTH, &length);
    //check_success (ret, SQL_HANDLE_DBC, hdbc);
    if (ret==SQL_SUCCESS)
    {

        printf ("\tODBC version: %s\n", stringVal);

        // check the version info is of the expected form, and copy
        // out the major, minor and build number.

        if ((unsigned int)length == strlen("##.##.####") ||
            (unsigned int)length == strlen("##.##.##") ||
	    (unsigned int)length == strlen("##.##.##.##"))
        {
            ODBC_major_number = atoi(&stringVal[0]);
            ODBC_minor_number = atoi(&stringVal[3]);
            ODBC_build_number = atoi(&stringVal[6]);
        }
    }
    else
        printf("\t(could not find out version of the ODBC driver.)\n");

    // find out the version number of the DATABASE to which we are
    // connected; it is quite legitimate for this to differ from
    // the version of the library.

    ret = SQLGetInfo (hdbc, SQL_DBMS_VER, 
                      stringVal, MAX_STRING_BUFFER_LENGTH, &length);
    //check_success (ret, SQL_HANDLE_DBC, hdbc);
    if (ret==SQL_SUCCESS)
    {
        printf ("\tDBMS version: %s\n", stringVal);

        // check the version info is of the expected form, and copy
        // out the major, minor and build number; compare with the 
        // ODBC versions. NB - other DBs return different formats
        // and the ODBC driver number may differ greatly from the
        // DB version number, so we should not assert that we know
        // the form, or insist the numbers match.

        if ((unsigned int)length == strlen("##.##.####") ||
	    (unsigned int)length == strlen("##.##.##.##"))
        {
            Poly_major_number = atoi(&stringVal[0]);
            Poly_minor_number = atoi(&stringVal[3]);
            Poly_build_number = atoi(&stringVal[6]);

            if ((ODBC_major_number != Poly_major_number) ||
                (ODBC_minor_number != Poly_minor_number) || 
                (ODBC_build_number != Poly_build_number) )
            {
                printf ("\n\t\aWarning: ODBC and DBMS versions differ, "
                        "\n\twhich may invalidate timing test\n");
            }
        }
    }
    else
        printf("\t(could not find out database version.)\n");

    do_disconnect (hdbc);
}

// ----------------------------------------------------------------------------
// check we can create tables
// ----------------------------------------------------------------------------

/*
    drop, create and drop again the tables we need so that we can be sure 
    the creation worked. (most of the times, the creation will be 'soft',
    allowing for them to already exist; by creating them with the 'strict'
    flag, we have a chance to see the error messages if there any problems).
*/

void check_table_creation (SQLHANDLE henv)
{
    SQLHANDLE  hdbc  = SQL_NULL_HANDLE;

    set_test ("table creation",
              "can we create the tables we will be needing?"
             );

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    drop_test_tables (hdbc);
    create_table_test1 (hdbc, TRUE);
    create_table_test2 (hdbc, TRUE);
    drop_test_tables (hdbc);

    do_disconnect (hdbc);
    printf("\ttables successfully created and dropped.\n");
}


// ----------------------------------------------------------------------------
// insert tests
// ----------------------------------------------------------------------------

/* insert_records

   This is the function that will be used directly or indirectly to do all
   the record inserts needed in the performance tests. The parameters are:
   
   rowcount   the number of rows to insert in all
   
   batch    the number of inserts per transaction. A value <= 1 means
              that each insert is done in its own transaction.

   big        if TRUE, all attributes of the record are defined in the 
              insert statement; if false, then only the first 5 attribute
              values are defined.
              
   cleanup    if true, a timing test is performed and reported, and then
              the test table emptied and dropped. If false, it is assumed
              that the function has been called to set up the table ready
              for another timing test; the time taken is not reported,
              and the table is left with the new records in it.
              
   The function will create the test table if not present, and the
   records it adds will be numbered from one upwards; if the table were
   already present, the function finds out how many records were in it,
   and the records it adds will be numbered consecutively starting at
   <recordcount>+1.
   
   The function returns the number of records
   
   The current implementation of this function uses the SQLPrepare 
   library call to get an sql statement analysed, uses SQLBindParameter
   to tell the library where to find parameter values when needed, and
   then calls SQLExecute repeatedly to perform the inserts. If batching
   the inserts into larger transactions, auto-commit mode is turned off,
   and explicit calls are made to SQLEndTran to signal the ends of a
   batch; once the inserts are done, auto-commit mode is turned back
   on again.
*/
int insert_records ( SQLHANDLE hdbc, int rowcount, int batch, int big, 
                     int cleanup, const char* testname
                   )
{
    SQLRETURN   ret;
    SQLHANDLE   hstmt    = SQL_NULL_HANDLE;
    int         i;
    SQLINTEGER  id       = 0;
    SQLDOUBLE   col2     = 2.0, col3  = 3.0;
    SQLINTEGER  cols[MaxColumnCount];
    SQLLEN  indicators[MaxColumnCount];
    SQLSMALLINT paramct;
    double      start;

    // make sure the right table exists, and find out how many records in
    // it if does already exist.

    if (big == FALSE)
        id = create_table_test1 (hdbc);
    else
        id = create_table_test2 (hdbc);

    alloc_stmt (hdbc, &hstmt);
    ret = SQLPrepare ( hstmt
                       , (big 
                          ? INSERT_INTO_TEST2_PARAM_SQL
                          : INSERT_INTO_TEST1_PARAM_SQL)
                       , SQL_NTS
                     );
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    SQLNumParams (hstmt, &paramct);
    if (cleanup)
    {
        // report what this subtest is about to do, but not if the function
        // had been called to set up test data for another test.
        //
        // NB: we are reporting 'late', to allow us to time to find out
        // how many parameters were in the SQL string we used; this makes
        // it easier to vary the maximum number of columns in the table!
        // in other subtests, we normally do the initial message before
        // doing anything much - before the call of create_test_table, say.

        printf ( "\t%s insert %d records" 
                 " (%d per transaction, %d attributes each)\n", 
                 (testname == NULL ? "" : testname), 
                 rowcount, batch, paramct
               );
        if (id>0)
        {
            printf ("\t(test table initially had %d records)\n", (int)id);
        }
    }

    indicators[0] = 0;
    ret = SQLBindParameter ( hstmt, 1, SQL_PARAM_INPUT, 
                             SQL_C_SLONG, SQL_INTEGER, 
                             0, 0, &id, sizeof(SQLINTEGER), &indicators[0]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    indicators[1] = 0;
    ret = SQLBindParameter ( hstmt, 2, SQL_PARAM_INPUT, 
                             SQL_C_DOUBLE, SQL_DOUBLE, 
                             0, 0, &col2, sizeof(SQLDOUBLE), &indicators[1]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    indicators[2] = 0;
    ret = SQLBindParameter ( hstmt, 3, SQL_PARAM_INPUT, 
                             SQL_C_DOUBLE, SQL_DOUBLE, 
                             0, 0, &col3, sizeof(SQLDOUBLE), &indicators[2]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    // the remaining parameters are all integers, so can be done by a loop
    for (i=4; i<=paramct; i++)
    {
        cols[i-1] = 0;
        indicators[i-1] = 0;
        ret = SQLBindParameter ( hstmt, i, SQL_PARAM_INPUT, 
                                 SQL_C_SLONG, SQL_INTEGER, 
                                 0, 0, &cols[i-1], sizeof(SQLINTEGER),
                                 &indicators[i-1]
                               );
        check_success (ret, SQL_HANDLE_STMT, hstmt);
    }

    if (batch > 1)
    {
        /* Set manual commit */
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT, 
                                  (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0
                                );
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    start = the_tick ();

    for (i = 1; i <= rowcount; i++)
    {
        ++id;
        ret = SQLExecute (hstmt);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
        if ((batch > 1) && (i % batch == 0))
        {
            ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
            check_success (ret, SQL_HANDLE_DBC, hdbc);
        }
    }

    if (((batch > 1) && (rowcount % batch != 0)))
    {
        ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    if (cleanup)
    {
        double rate = HowFast (start, "insert", rowcount);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
    }
    free_stmt (hstmt);

    /* TIDY-UP */
    if (batch > 1)
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT,
                                  (SQLPOINTER)SQL_AUTOCOMMIT_ON, 0
                                );
    check_success (ret, SQL_HANDLE_DBC, hstmt);
    if (cleanup) drop_test_tables (hdbc);

    // return the number of records now in the table
    // (or that would have been there, if it hadnt
    // been cleaned up).

    return id;
}


/* insert_individually

   insert a number of records, one per transaction;
   report on the time taken and clear up afterwards.
*/
void insert_individually (SQLHANDLE hdbc, int rowcount, const char* testname)
{
    insert_records (hdbc, rowcount, 1, FALSE, TRUE, testname);
}

/* insert

   this function performs the insert-related timing tests. It opens
   the connection, calls insert_records or insert_individually to 
   perform the individual tests,and then drops the connection. At
   the end of the tests, the database will be left empty.
*/
void insert (SQLHANDLE henv, 
	     int rowcount)
{
    SQLHANDLE  hdbc  = SQL_NULL_HANDLE;

    set_test ("inserts",
              "how fast can we insert records?"
              "\n\thow much slower are inserts if there are many attributes?"
              "\n\thow much does batching up the inserts improve performance?"
              "\n\thow much does the size of the table affect insert speed?"
             );

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    // (individual record inserts)
    insert_individually (hdbc, rowcount, "I5 ");

    // (individual record inserts, big records)
    insert_records (hdbc, rowcount, 1, TRUE, TRUE, "I50");

    // (affect of batching)
    insert_records (hdbc, rowcount, 100, FALSE, TRUE, "I5B");

    // (check insert into pre-populated table)
    insert_records (hdbc, rowcount*10, 100, FALSE, FALSE, NULL);
    insert_individually (hdbc, rowcount, "I5P");

    // (no need to drop test table here, each subtest does that for itself)
    do_disconnect (hdbc);
}


// ----------------------------------------------------------------------------
// queries
// ----------------------------------------------------------------------------


/* scan_results

   scan a result set but do nothing with the results other than put the
   attributes in a buffer temporarily - just to prove the results have
   all been received by the client. (Polyhedra uses client-side cursors
   whereas some other systems use server-side cursors - for these, it
   is only if the cursor moves over the full result set that the true
   cost of the query is found.)
   A columnCount of zero instructs the code to find out how many columns
   were returned by the query.
   Return the number of records in the result set.
*/
int scan_results (SQLHANDLE hstmt, SQLSMALLINT columnCount)
{
    int         i = 0;
    SQLRETURN   ret;
    SQLSMALLINT columnNumber;
    SQLCHAR     value[MAX_COLUMN_BUFFER_LENGTH];
    SQLLEN  length;

    if (columnCount == 0)
    {
        ret = SQLNumResultCols (hstmt, &columnCount);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
    }

    /* scan the result set by fetching a row at a time */
    while ((ret = SQLFetch (hstmt)) == SQL_SUCCESS)
    {
        i++;
        for (columnNumber = 1; columnNumber <= columnCount; columnNumber++)
        {
            ret = SQLGetData ( hstmt, columnNumber, SQL_C_CHAR, 
                               &value, MAX_COLUMN_BUFFER_LENGTH, &length
                             );
            check_success (ret, SQL_HANDLE_STMT, hstmt);
        }
    }

    ret = SQLCloseCursor (hstmt);
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    return i;
}


/* do_query

   this function does <querycount> queries, using the supplied SQL in 
   each case. If useparam is true, a local variable is bound to 
   parameter one of the query, and the parameter value will be varied
   between 1 and <rowcount>.
*/
double do_query ( SQLHANDLE  hdbc, int rowcount, int queryct, SQLCHAR* sql, 
                  int useparam, const char* testname
                )
{
    SQLRETURN   ret;
    SQLHANDLE   hstmt     = SQL_NULL_HANDLE;
    int         i;
    int         ct        = 0;
    SQLINTEGER  value     = 1;
    SQLLEN  indicator = 0;
    SQLSMALLINT columnCount;
    double      start;

    alloc_stmt (hdbc, &hstmt);

    ret = SQLPrepare (hstmt, sql, SQL_NTS);
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    ret = SQLNumResultCols (hstmt, &columnCount);
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    printf ( "\t%s %d %s queries (%d attributes)\n", 
             (testname == NULL ? "" : testname),
             queryct, (useparam ? "individual record" : "table"), columnCount
           );

    if (useparam)
    {
        ret = SQLBindParameter ( hstmt, 1, SQL_PARAM_INPUT, SQL_C_SLONG, 
                                 SQL_INTEGER, 0, 0, 
                                 &value, sizeof(SQLINTEGER), &indicator
                               );
        check_success (ret, SQL_HANDLE_STMT, hstmt);
    }

    // (we are not bothering to bind the result set at this stage; the
    // columns are being retrieved, but not stored anywhere.)

    start = the_tick ();

    for (i = 0; i < queryct; i++)
    {
        ret = SQLExecute (hstmt);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
        ct += scan_results (hstmt, columnCount);
        value = (value % rowcount) + 1;
    }

    if (ct>queryct)
    {
        printf ("\t%d records returned per query.\n", ct / queryct);
    }
    double rate = HowFast (start, "query", ct);
    if (testname != NULL)
    {
        Recorder->Record (testname, rate);
    }
    free_stmt (hstmt);
    return rate;

}

/* do_batched_query

   this function does a number of queries to retrieve a total of queryct 
   rows in batches of the indicated size, using the supplied SQL coupled 
   with a 'where id in (...)' clause. Note that at present we are not 
   using SQLPrepare, so it is not quite as fast as it could be; however,
   using SQLExecDirect means that coding is very much simplified in this
   example, and the SQL parsing overhead is only once per batch of
   records retrieved, and so does not significantly affect performance.
*/
double do_batched_query ( SQLHANDLE  hdbc, int rowcount, int queryct, 
                          SQLCHAR* sql, int batch, const char* testname
                        )
{
    SQLRETURN   ret;
    SQLHANDLE   hstmt = SQL_NULL_HANDLE;
    int         i;
    int         ct = 0;
    double      start;
    int         id = 1;
    char        buffer[BUFFERSIZE];
    int         posn;
    int         bufflimit = BUFFERSIZE - 10;

    if (batch > MAXBATCHSIZE)
        batch = MAXBATCHSIZE;
    if (batch > rowcount)
        batch = rowcount;

    printf ( "\t%s retrieve %d records (%d per batch)\n", 
             (testname == NULL ? "" : testname),
             queryct, batch
           );

    start = the_tick ();
    posn  = 0;

    for (i = 1; i <= queryct; i++)
    {
        if (batch < 2)
        {
            // we shall retrieve records one at a time.

            sprintf (&buffer[0], "%s where id=%d", sql, id);

            // perform the query, retrieve the results
            alloc_stmt (hdbc, &hstmt);
            ret = SQLExecDirect (hstmt, (SQLCHAR*)buffer, SQL_NTS);
            check_success (ret, SQL_HANDLE_STMT, hstmt);
            ct += scan_results (hstmt, 0);
            free_stmt (hstmt);
        }
        else
        {
            if (posn == 0)
            {
                // first record of the batch; put the SELECT
                // statement into the buffer, with an 'IN' 
                // clause; not that we will overwrite the
                // closing parenthesis if we will be fetching
                // more than one record in this batch.

                posn = sprintf (&buffer[0], 
                                "%s WHERE id IN (%d)", sql, id);
            }
            else
            {
                // extend the SELECT statement we have been
                // building, writing over the parenthesis left
                // by the last call of sprintf)

                posn --;
                posn += sprintf (&buffer[posn], ",%d)", id);
            }
            if ((i % batch == 0) || posn > bufflimit)
            {
                // perform the query, retrieve the results

                alloc_stmt (hdbc, &hstmt);
                ret = SQLExecDirect (hstmt, (SQLCHAR*)buffer, SQL_NTS);
                check_success (ret, SQL_HANDLE_STMT, hstmt);
                ct += scan_results (hstmt, 0);
                free_stmt (hstmt);
                posn = 0;
            }
        }
        id = (id % rowcount) + 1;
    }

    if (posn > 0)
    {
        // perform the final query, retrieve the results
        alloc_stmt (hdbc, &hstmt);
        ret = SQLExecDirect (hstmt, (SQLCHAR*)buffer, SQL_NTS);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
        ct += scan_results (hstmt, 0);
        free_stmt (hstmt);
    }
    if (ct != queryct)
    {
        printf ("\t%d records returned in total, where we expected %d.\n", 
                ct, queryct);
    }
    double rate = HowFast (start, "query", ct);
    if (testname != NULL)
    {
        Recorder->Record (testname, rate);
    }
    return rate;
}

double query5 (int rowcount, int queryct, SQLHANDLE  hdbc, const char* testname)
{
    return do_query (hdbc, rowcount, queryct, SELECT_FROM_TEST1_PARAM_SQL, TRUE, 
                     testname);
}


double query50 (int rowcount, int queryct, SQLHANDLE  hdbc, const char* testname)
{
    return do_query (hdbc, rowcount, queryct, SELECT_FROM_TEST2_PARAM_SQL, TRUE,
                     testname);
}


double query_all (int rowcount, int queryct, SQLHANDLE  hdbc, const char* testname)
{
    return do_query (hdbc, rowcount, queryct, SELECT_FROM_TEST1_SQL, FALSE, 
                     testname);
}



/* query

   this function is called to perform the individual query performance
   tests. It first opens the tests, uses insert_records to create some
   records, and then does some tests. The record count is then gradually
   increased and certain tests repeated to see how they are affected by
   table size. At the end, the table is emptied and dropped, and the
   connection closed.
*/
void query (SQLHANDLE henv,
	    int rowcount)
{
    SQLHANDLE  hdbc      = SQL_NULL_HANDLE;
    int        tablesize = (rowcount < 1000 ? rowcount : 1000);
    int        ct1       = 0;
    int        ct2       = 0;

    set_test ("Query",
              "how fast can we retrieve individual records when we know the PK?"
              "\n\thow is retrieval time affected by the number of attributes?"
              "\n\thow is retrieval time affected by the size of table?");

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    // create and populate both test tables.

    ct1 = insert_records (hdbc, tablesize, INSERTBATCHSIZE, FALSE, FALSE, NULL);
    ct2 = insert_records (hdbc, tablesize, INSERTBATCHSIZE, TRUE , FALSE, NULL);

    if (ct1 == ct2)
        printf ("  *\ttest tables each have %d records\n\n", ct1);
    else
        printf ("  *\ttest1 table has %d records, test2 %d\n\n", ct1, ct2);

    // do the tests

    query5    (ct1, rowcount,     hdbc, "Q5 " );
    query50   (ct2, rowcount,     hdbc, "Q50");
    //query_all (ct1, rowcount/100, hdbc, "Q5A" );
    do_batched_query  (hdbc, ct1, rowcount, SELECT_FROM_TEST1_SQL, 50, "Q5B");

    // now test again with 10 times more records in table test1

    ct1 = insert_records (hdbc, tablesize*9, INSERTBATCHSIZE, FALSE, FALSE, NULL);

    printf ("  *\ttest1 table has %d records\n\n", ct1);
    query5    (ct1, rowcount,     hdbc, "Q5P");

    drop_test_tables (hdbc);
    do_disconnect (hdbc);
}


// ----------------------------------------------------------------------------


void update_records (SQLHANDLE hdbc, int rowcount, int opct, int batch, int big, 
                     const char* testname = NULL)
{
    SQLRETURN   ret;
    SQLHANDLE   hstmt    = SQL_NULL_HANDLE;
    int         i, j;
    SQLINTEGER  id       = 0;
    SQLDOUBLE   col2     = 2.0, col3  = 3.0;
    SQLINTEGER  cols[50];
    SQLLEN  indicators[50];
    SQLSMALLINT paramct;
    double     start;
    static int call_count = 0; // Call 8414
    call_count++;
    
    printf ( "\t%s update %d records (%d per transaction, %d attributes each)\n", 
             (testname == NULL ? "" : testname), 
             opct, batch, ((big==TRUE) ? 50 : 5)
           );

    alloc_stmt (hdbc, &hstmt);

    ret = SQLPrepare ( hstmt
                       , (big 
                          ? UPDATE_TEST2_PARAM_SQL
                          : UPDATE_TEST1_PARAM_SQL)
                       , SQL_NTS
                     );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    SQLNumParams (hstmt, &paramct);
    //fprintf (stderr, "(%d parameters)\n", paramct);

    indicators[0] = 0;
    ret = SQLBindParameter ( hstmt, 1, SQL_PARAM_INPUT, 
                             SQL_C_DOUBLE, SQL_DOUBLE, 
                             0, 0, &col2, sizeof(SQLDOUBLE), &indicators[0]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    col2 = call_count;
    indicators[1] = 0;
    ret = SQLBindParameter ( hstmt, 2, SQL_PARAM_INPUT, 
                             SQL_C_DOUBLE, SQL_DOUBLE, 
                             0, 0, &col3, sizeof(SQLDOUBLE), &indicators[1]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    col3 = call_count;
    // the remaining parameters are all integers, so can be done by a loop
    for (i=3; i<=paramct-1; i++)
    {
        cols[i-1] = call_count;
        indicators[i-1] = 0;
        ret = SQLBindParameter ( hstmt, i, SQL_PARAM_INPUT,
                                 SQL_C_SLONG, SQL_INTEGER, 
                                 0, 0, &cols[i-1], sizeof(SQLINTEGER), 
                                 &indicators[i-1]
                               );
        check_success (ret, SQL_HANDLE_STMT, hstmt);
    }

    // the 'id' column is the LAST parameter value, as the 'where' clause
    // follows the 'set' clause of an update statement.

    indicators[paramct-1] = 0;
    ret = SQLBindParameter ( hstmt, paramct, SQL_PARAM_INPUT,
                             SQL_C_SLONG, SQL_INTEGER, 
                             0, 0, &id, sizeof(SQLINTEGER),
                             &indicators[paramct-1]
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    if (batch > 1)
    {
        /* Set manual commit */
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT, 
                                  (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0
                                );
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    start = the_tick ();

    for (i = 1; i <= opct; i++)
    {
        id = (id % rowcount) + 1;
        ++col2;
        ++col3;  
        for (j=4; j<=paramct; j++)
        {
            ++cols[j-1]; 
        }

        ret = SQLExecute (hstmt);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
        if ((batch > 1) && (i % batch == 0))
        {
            ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
            check_success (ret, SQL_HANDLE_DBC, hdbc);
        }
    }

    if (((batch > 1) && (opct % batch != 0)))
    {
        ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    double rate = HowFast (start, "update", opct);
    if (testname != NULL)
    {
        Recorder->Record (testname, rate);
    }

    free_stmt (hstmt);

    /* TIDY-UP */
    if (batch > 1)
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT, 
                                  (SQLPOINTER)SQL_AUTOCOMMIT_ON, 0
                                );
    check_success (ret, SQL_HANDLE_DBC, hstmt);
}


void update (SQLHANDLE henv,
	     int rowcount)
{
    SQLHANDLE  hdbc  = SQL_NULL_HANDLE;
    int        tablesize = (rowcount < 1000 ? rowcount : 1000);
    int        ct1, ct2;

    set_test("Update",
             "how fast can one update individual records?"
             "\n\thow much slower if many attributes updated per record?"
             "\n\thow much does batching the updates speeed things up?"
             "\n\thow much does table size affect the update rate?"
            );

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    // create and populate both test tables.

    ct1 = insert_records (hdbc, tablesize,  INSERTBATCHSIZE, FALSE, FALSE, NULL);
    ct2 = insert_records (hdbc, tablesize,  INSERTBATCHSIZE, TRUE , FALSE, NULL);

    if (ct1 == ct2)
        printf ("  *\ttest tables each have %d records\n\n", ct1);
    else
        printf ("  *\ttest1 table has %d records, test2 %d\n\n", ct1, ct2);


    // do the main tests

    update_records (hdbc, ct1, rowcount,   1, FALSE, "U5 " );
    update_records (hdbc, ct2, rowcount,   1, TRUE,  "U50");
    update_records (hdbc, ct1, rowcount,  50, FALSE, "U5B");

    // repeat tests with a bigger table size

    ct1 = insert_records (hdbc, tablesize*9, INSERTBATCHSIZE, FALSE, FALSE, NULL);
    printf ("  *\ttest1 table has %d records\n\n", ct1);

    update_records (hdbc, ct1, rowcount,   1, FALSE, "U5P");

    drop_test_tables (hdbc);
    do_disconnect (hdbc);
}


// ----------------------------------------------------------------------------


void delete_records ( SQLHANDLE hdbc, int rowcount, int batch, int big, 
                      const char* testname
                    )
{
    SQLRETURN  ret;
    SQLHANDLE  hstmt     = SQL_NULL_HANDLE;
    SQLINTEGER id        = 0;
    SQLLEN indicator = 0;
    int        originalrecordct;
    int        i;
    double     start;

    printf ("\t%s delete %d records (%d per transaction)\n",
            (testname == NULL ? "" : testname), 
            rowcount, batch
           );

    id = insert_records (hdbc, rowcount, INSERTBATCHSIZE, big, FALSE, NULL);
    originalrecordct = id - rowcount;
    if (originalrecordct)
    {
        printf ("\t(test table initially had %d records)\n", originalrecordct);
    }

    alloc_stmt (hdbc, &hstmt);

    ret = SQLPrepare ( hstmt
                       , (big==FALSE
                          ? DELETE_FROM_TEST1_PARAM_SQL
                          : DELETE_FROM_TEST2_PARAM_SQL)
                       , SQL_NTS
                     );
    check_success (ret, SQL_HANDLE_STMT, hstmt);
    ret = SQLBindParameter ( hstmt, 1, SQL_PARAM_INPUT, 
                             SQL_C_SLONG, SQL_INTEGER, 
                             0, 0, &id, sizeof(SQLINTEGER), 
                             &indicator
                           );
    check_success (ret, SQL_HANDLE_STMT, hstmt);

    if (batch > 1)
    {
        /* Set manual commit */
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT, 
                                  (SQLPOINTER)SQL_AUTOCOMMIT_OFF, 0
                                );
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    start = the_tick ();

    for (i = 1; i <= rowcount; i++)
    {
        ret = SQLExecute (hstmt);
        check_success (ret, SQL_HANDLE_STMT, hstmt);
        if ((batch > 1) && (i % batch == 0))
        {
            ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
            check_success (ret, SQL_HANDLE_DBC, hdbc);
        }
        --id;
    }

    if (((batch > 1) && (rowcount % batch != 0)))
    {
        ret = SQLEndTran (SQL_HANDLE_DBC, hdbc, SQL_COMMIT);
        check_success (ret, SQL_HANDLE_DBC, hdbc);
    }

    double rate = HowFast (start, "delete", rowcount);
    if (testname != NULL)
    {
        Recorder->Record (testname, rate);
    }

    free_stmt (hstmt);

    /* TIDY-UP */
    if (batch > 1)
        ret = SQLSetConnectAttr ( hdbc, SQL_ATTR_AUTOCOMMIT, 
                                  (SQLPOINTER)SQL_AUTOCOMMIT_ON, 0
                                );
    check_success (ret, SQL_HANDLE_DBC, hstmt);

    /*
    // use a side-effect of insert_records to find out how many records
    // REMAIN in the table
    id = insert_records (hdbc, 0, 1, big, FALSE, NULL);
    if (id != originalrecordct)
    {
    fprintf (stderr, 
         "application error - delete_records did not work;"
         "final record count = %d, not %d.\n",
         id, originalrecordct
         );
    fail (__FILE__, __LINE__);
    }
    */

}


void deleteRows (SQLHANDLE henv,
		 int rowcount)
{
    SQLHANDLE  hdbc  = SQL_NULL_HANDLE;

    set_test ("Delete",
              "how fast can one delete individual records?"
              "\n\thow much does batching improve the performance?"
              "\n\thow much does table size affect the deletion rate?"
             );

    do_connect (henv, &hdbc, (SQLCHAR *)DSN);

    delete_records (hdbc, rowcount,   1, FALSE, "D5 ");
    delete_records (hdbc, rowcount,  50, FALSE, "D5B");
    delete_records (hdbc, rowcount,   1, TRUE,  "D50");

    // repeat tests with some records already there

    insert_records (hdbc, rowcount * 10, INSERTBATCHSIZE, FALSE, FALSE, NULL);
    delete_records (hdbc, rowcount, 1, FALSE, "D5P");

    drop_test_tables (hdbc);
    do_disconnect (hdbc);
}


// ----------------------------------------------------------------------------


#ifdef EXTRA

    #include "odbcxtra.hxx"

#endif


// ----------------------------------------------------------------------------
// invoke the tests.
// ----------------------------------------------------------------------------

double run_tests(SQLHANDLE henv)
{
    // first, the standard tests that do not use the database:
    // do these before we start the clock for the total test run,
    // as the time for this stage is not dependent on the DBMS
    // software.

#ifdef RAW
    raw_performance ();
#endif

    double start = the_tick ();

    display_version (henv);

#ifdef STANDARD
    // "just the facts, ma'm"
    // all the standard tests, and just the standard tests.

    //check_table_creation (henv); // include this when testing new DBMSes
    insert     (henv, RowCount);
    query      (henv, RowCount);
    update     (henv, RowCount);
    deleteRows (henv, RowCount);
#endif
#ifdef EXTRA
    extras (RowCount);
#endif

    printf ("\nTests complete.\n\a\n");
    double rate  = HowFast (start, "", 0);

#ifdef STANDARD
    #ifndef EXTRA

    /* only when it is the 'bog-standard' test do we want to produce
    // an extra record recording the total, otherwise we are not    
    // comparing like with like.

    // as we using the string in this fn (when we delete the Recorder)
    // we can use a local to hold a dynamically-created string:
    */
    static char total[20];
    sprintf (total, "total/%d", RowCount);

    Recorder->Record (total, rate);
    #endif
#endif
    return rate;
}

extern "C" int test_odbcapi ( const char *dsn,
                              const char *rowCount,
                              const char *delay,
			      const char *minSecsArg
                            )
{
    // Mimum test time in seconds - default 0 is no minimum.
    int minSecs = 0;

    if (dsn      != NULL) DSN       = Service = dsn;
    if (rowCount != NULL) RowCount  = atoi(rowCount);
    if (delay    != NULL) DelayTime = atoi(delay);
    if(minSecsArg   != NULL) minSecs = atoi(minSecsArg);

    printf ( "Polyhedra performance tester (using ODBC API);"
             "\n\tserver=%s, opcount = %d minimum = %d.\n\n"
             , Service, RowCount, minSecs
           );

    SQLHANDLE henv = SQL_NULL_HANDLE;
    alloc_env(&henv);

    Init_IO ();

    Recorder = new TestRecords ("odbc");

    double rate = run_tests(henv);

    if(minSecs && rate <  minSecs)
    {
	// Do more rows to run for the requested time.
	// Adding an extra 10% gets us closer to the requested minimum.
	RowCount = (int) (1.1 * RowCount * minSecs / rate);
	printf("Run time is less than %d, so re-running with %d rows.\n",
	       minSecs, RowCount);

	// Get rid of previous results.
	Recorder->Clear();

	rate = run_tests(henv);
    }

    delete Recorder;

    End_IO ();

    free_connect(henv, SQL_NULL_HANDLE);

    return 0;
}


// ----------------------------------------------------------------------------
// main function - 'main' on UNIX and Windows, 'perform' on embedded platforms
// that support the argv/argc command line stuff (on others, invoke
// test_odbcapi directly).
// ----------------------------------------------------------------------------

#if defined(EMBEDDED)
#define NO_MAIN
#endif

#ifdef NO_MAIN
// on platforms where one is not allowed/expected to redefine main(),
// either perform() or test_odbcapi() can be used; use the former
// if using a shell that supplies command line parameters as in Unix,
//the latter if one can invoke the call with arguments of the correct
// type.
//
extern "C" int poly_main (int argc, char* argv [])
//
#else
//
// unix-style 'main'.
//
extern "C" int main (int argc, char* argv [])
//
#endif
  {
      if (argc > 4)
      {
          fprintf (stderr, 
                   "usage: %s [<dsn>] [<opcount>[,minsecs]] [<inter-test_delay>]\n",
                   argv[0]);
          return 1;
      }
      else
      {
	  // Find the minSecs
	  char* minSecs = NULL;
	  if((argc >= 3) && (minSecs = strchr(argv[2],',')))
	  {
	      *minSecs = '\0';
	      minSecs++;
	  }
          return test_odbcapi ( (argc >= 2 ? argv[1] : NULL),
                                (argc >= 3 ? argv[2] : NULL),
                                (argc >= 4 ? argv[3] : NULL),
                                minSecs
				);
      }
  }



/*---------------------------------------------------------------------------*/
/*                          e n d   o f   f i l e                            */
/*---------------------------------------------------------------------------*/

