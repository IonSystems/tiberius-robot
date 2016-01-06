/*-+-----------------------------------------------------------------------+-//
//                                                                           //
//               P O L Y H E D R A    T E S T    L I B R A R Y               //
//                                                                           //
//                Copyright (C) 1999-2015 by Enea Software AB                //
//                           All Rights Reserved                             //
//                                                                           //
//---------------------------------------------------------------------------//
//	 
//-+ Filename    : jdbcapi.cxx
//-+ Description : performance test application - JDBC version
//
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

import java.sql.*;   // pick up JDBC interface classes
import java.util.*;  // Vector used for keeping performance records
import java.net.*;   // used to find name of this machine.
import java.text.*;  // used to format floating point numbers.


//-----------------------------------------------------------------------------
//                RECORDER (plus its helpers)
//-----------------------------------------------------------------------------


final class Record
//
// a class used to record the result of an individual test.
//
{
    protected String testName;
    protected String rate = "NULL";

    Record (String name, String rrate)
    {
        testName = name;
        rate     = rrate;
    }
    public String toString ()
    {
        return testName + " => " + rate;
    }
}


final class Recorder
//
// a class used to keep track of the individual test results, and
// print them all out at the end of the test run. Everything is done
// via statics - sigh - not good style, but the simplest way of
// mimicing what is done in the ODBC API test.
//
{
    // define a vector which will be used to kepp track of 
    // individual test results
    private static Vector records = new Vector ();

    // which subgroup of the test suite is currently being
    // run, and what kind of operation is being done n times
    // in each test.
    private static String testGroup;
    private static String testOpType;

    private static DecimalFormat dp0  = new DecimalFormat("0");
    private static DecimalFormat dp2  = new DecimalFormat("0.00");
    private static DecimalFormat dp3  = new DecimalFormat("0.000");
    private static DecimalFormat cdp3 = new DecimalFormat("###,##0.000");

    public static int majorVersion = 0;
    public static int minorVersion = 0;

    // now the static methods that are called in order to get this 
    // class to do something.

    public static void setTestGroup (String group, 
				     String opType, 
				     String purpose)
    {
        testGroup  = group;
        testOpType = opType;
        System.out.println ("\n" + group + "\n");
        if (purpose != null)
            System.out.println ("\t" + purpose + "\n");
    }

    public static long now ()
    {
        //java.util.Date d = new java.util.Date ();
        //return d.getTime ();
        return System.currentTimeMillis ();
    }

    public static int record_performance (long msecs, int opct, int batchct, String testName)
    //
    {
        String duration = ((msecs >= 300) ? dp2 :dp3) . format (msecs / 1000.0);
        String rate;
        int    result = 0;

        if (testName == null)
            testName = "";

        System.out.println ("\ttest " + testName + " took " + duration + " seconds" );

        if (opct > 1 )
        {
            double drate = (opct * 1000.0) / msecs;
            result = (int) drate;
            rate = ((drate>=100) ? dp0 : dp2 ) . format (drate);
            System.out.println ("\t" + testOpType + " rate: " + rate + " per second" );
        }
        else
            rate = duration;
        records.add (new Record (testName, rate));
        return result;
    }

    public static int calculate_performance (long startTick, int opct, int batchct, String testName)
    //
    {
        return record_performance (now()-startTick, opct, batchct, testName);
    }

    public static void report_performance ()
    //
    // print out the summary results.
    //
    {
        // try and find out the machine name.
        String machine = "java";
        try
        {
            machine = InetAddress.getLocalHost ().getHostName ();
        }
        catch ( UnknownHostException ehex)
        {
        }

        System.out.println ("\n\nresult summary for " + 
                            machine + 
                            " (JDBC API):\n\n");

        for (Enumeration e = records.elements() ; e.hasMoreElements() ;)
        {
            System.out.println("\t**** " + machine + " jdbc (" +
                               majorVersion + "." + 
                               minorVersion + ".?): " +  
                               e.nextElement());
        }
        System.out.print ("\n");
    }
}


//-----------------------------------------------------------------------------
//                C O N N E C T I O N M A N A G E R
//-----------------------------------------------------------------------------


final class TableManager
//
// keep track of the state of a test table in the database, and also the 
// specific substrings needed to operate on it. NB: the code assumes that
//
//  *  the 1st column is an integer called ID and is the primary key; 
//  *  attributes 2 and 3 are real; and,
//  *  all other attributes are integers.
//
{
    String name;
    int    fieldct; // number of columns
    String create;
    String insert;
    String query;
    String update;

    int    ct;

    public TableManager (String n, int fct, String c, String i, String q, String u)
    {
        ct      = -1; // -ve => table probably does not exist.
        name    = n;
        fieldct = fct;
        create  = "CREATE TABLE " + n + " ( persistent, " + c + ")";
        insert  = "INSERT INTO " + n + " " + i;
        query   = "SELECT " + q + " FROM " + n;
        update  = "UPDATE " + n + " SET " + u + " WHERE id=?";
    }
}


final class connectionManager
//
// a class to connect to the database and do some operations.
// NB: in the expectation that most JDBC errors are fatal, no 
// errors are caught except where we expect something to go
// wrong - like where we create tables that may already exist.
//
{
    // ----------------------------------------------------------------
    // first the static attributes that will be common to all instances
    // for reasons of laziness; we know we will always be connecting
    // to the same database in a given run.
    // ----------------------------------------------------------------

    public static String url            = "";
    public static String uid            = null;
    public static String pwd            = null;
    public static String database       = null;
    public static int    errorLevel     = 16;
    public static int    queryTimeout   = 8;
    public static int    connectTimeout = 8;

    public static TableManager smallTable = 
    new TableManager ("test1", 5, 
                      // column definitions
                      "id INTEGER primary key, col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER",
                      // insert string
                      "(id, col2, col3, col4, col5) VALUES (?, ?, ?, ?, ?)",
                      // query string
                      " id, col2, col3, col4, col5",
                      // update string
                      "col2=?, col3=?, col4=?, col5=?");

    public static TableManager bigTable = 
    new TableManager ("test2", 50,
                      // column definitions
                      "  id INTEGER primary key, col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER" +
                      ", col6  INTEGER, col7  INTEGER, col8  INTEGER, col9  INTEGER, col10 INTEGER" +
                      ", col11 INTEGER, col12 INTEGER, col13 INTEGER, col14 INTEGER, col15 INTEGER" +
                      ", col16 INTEGER, col17 INTEGER, col18 INTEGER, col19 INTEGER, col20 INTEGER" +
                      ", col21 INTEGER, col22 INTEGER, col23 INTEGER, col24 INTEGER, col25 INTEGER" +
                      ", col26 INTEGER, col27 INTEGER, col28 INTEGER, col29 INTEGER, col30 INTEGER" +
                      ", col31 INTEGER, col32 INTEGER, col33 INTEGER, col34 INTEGER, col35 INTEGER" +
                      ", col36 INTEGER, col37 INTEGER, col38 INTEGER, col39 INTEGER, col40 INTEGER" +
                      ", col41 INTEGER, col42 INTEGER, col43 INTEGER, col44 INTEGER, col45 INTEGER" +
                      ", col46 INTEGER, col47 INTEGER, col48 INTEGER, col49 INTEGER, col50 INTEGER",
                      // insert string
                      "( id,    col2,  col3,  col4,  col5"  +
                      ", col6,  col7,  col8,  col9,  col10" +
                      ", col11, col12, col13, col14, col15" +
                      ", col16, col17, col18, col19, col20" +
                      ", col21, col22, col23, col24, col25" +
                      ", col26, col27, col28, col29, col30" +
                      ", col31, col32, col33, col34, col35" +
                      ", col36, col37, col38, col39, col40" +
                      ", col41, col42, col43, col44, col45" +
                      ", col46, col47, col48, col49, col50" +
                      ") VALUES"                            +
                      "( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      +
                      ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      +
                      ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      +
                      ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      +
                      ", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"      +
                      ")",
                      // query string
                      "  id,    col2,  col3,  col4,  col5"  +
                      ", col6,  col7,  col8,  col9,  col10" +
                      ", col11, col12, col13, col14, col15" +
                      ", col16, col17, col18, col19, col20" +
                      ", col21, col22, col23, col24, col25" +
                      ", col26, col27, col28, col29, col30" +
                      ", col31, col32, col33, col34, col35" +
                      ", col36, col37, col38, col39, col40" +
                      ", col41, col42, col43, col44, col45" +
                      ", col46, col47, col48, col49, col50",
                       // update string
                      "col2=?,  col3=?,  col4=?,  col5=?" +
                      ",  col6=?,  col7=?,  col8=?,  col9=?, col10=?" +
                      ", col11=?, col12=?, col13=?, col14=?, col15=?" +
                      ", col16=?, col17=?, col18=?, col19=?, col20=?" +
                      ", col21=?, col22=?, col23=?, col24=?, col25=?" +
                      ", col26=?, col27=?, col28=?, col29=?, col30=?" +
                      ", col31=?, col32=?, col33=?, col34=?, col35=?" +
                      ", col36=?, col37=?, col38=?, col39=?, col40=?" +
                      ", col41=?, col42=?, col43=?, col44=?, col45=?" +
                      ", col46=?, col47=?, col48=?, col49=?, col50=?"
		      );

    // --------------------------------------------------------
    // methods for connecting, disconnecting, are we connected?
    // --------------------------------------------------------

    private static Connection MyConnection = null;

    public void connect () throws SQLException
        //
        // connect to the database. If it is not available, 
        // either an exception will be thrown - but being
        // paranoid (some drivers may not be properly
        // implemented), I check an object has been returned.
        // Either way, a failure to connecte will stop the
        // test application.
    {       
        // ensure not already connected:
        disconnect ();

        java.util.Properties prop = new java.util.Properties();
        if (uid != null)
            prop.put("user", uid);
        if (pwd != null)
            prop.put("password", pwd);
        if (database != null)
            prop.put("database", pwd);

        //System.out.println ("(in connect() function, about to call getConnection(" +url+")...)");
        DriverManager.setLoginTimeout(3);
        MyConnection = DriverManager.getConnection(url, prop);
        //System.out.println ("(in connect() function, getConnection(" +url+") complete");
        if (MyConnection == null)
        {
            System.out.println("Unable to connect to JDBC Driver");
            System.exit (1);
        }
        //return(MyConnection != null);
    }

    public void disconnect () throws SQLException
        //
        // disconnect if connected.
        //
    {       
        if (MyConnection != null)
                MyConnection.close();
        MyConnection = null;
    }

    public boolean isConnected ()
    // 
    // are we currently connected?
    //
    {
        return(MyConnection != null);
    }

    public void ensureConnected () throws SQLException
    //
        // connect to the database if we are not 
        // currently connected.
        //
        {
        if (!isConnected ()) connect ();
    }

    // ---------------
    // utility methods
    // ---------------

    public void GetMetaData () throws SQLException
    //
    // get some interesting data about the connection
    //
    {
        ensureConnected ();

        try
        {
            DatabaseMetaData dbd = MyConnection.getMetaData();

            // database version info

            System.out.println ( "\tdatabase manager is "        +
                                 dbd.getDatabaseProductName()    +
                                 ", version "                    +
                                 dbd.getDatabaseProductVersion() );

            // JDBC driver info

            System.out.println ( "\tjdbc driver is "    + 
                                 dbd.getDriverName()    +
                                 ", version "           +
                                 dbd.getDriverVersion() );
            Recorder.majorVersion = dbd.getDriverMajorVersion();
            Recorder.minorVersion = dbd.getDriverMinorVersion();
        }
        catch (SQLException ex)
        {
        }
    }

    public int doQuery (String sql) throws SQLException
    //
    // execute an SQL query; return the number of rows retrieved.
    // don't catch errors.
    //
    {
        int row = 0;
        ensureConnected ();
        Statement statement = MyConnection.createStatement();
        ResultSet resultSet = statement.executeQuery(sql);

        // iterate over result set to ensure it has all
        // been retrieved from the server.

        for (; resultSet.next(); row++)
        {
        }

        // close jdbc objects
        //resultSet.close();
        statement.close();
        return row;
    }

    public int doSQL (String sql) throws SQLException
    //
    // execute SQL DDL or DML, return number of records affected.
    // don't catch errors, as we want them to be fatal.
    // For use in setting up things ready
    // for a test, or tidying up afterwards, as it does not use
    // prepared statements.
    //
    {
        int rowct = -1;
        ensureConnected();
        Statement statement = MyConnection.createStatement();
        rowct = statement.executeUpdate(sql);
        statement.close();
        return rowct;
    }

    private int howBig (String tablename) throws SQLException
    //
    // how many records are in the given table?
    //
    // (we will get an exception if the table does not exist;
    // trap it so that my caller can give an appropriate
    // error message.)
    //    
    {
        ensureConnected ();
        Statement statement = MyConnection.createStatement ();
        try
        {
	    ResultSet resultSet = 
		statement.executeQuery ("SELECT COUNT(*) FROM " + tablename);
	    resultSet.next ();
	    int rows = resultSet.getInt (1);

	    // close jdbc objects
	    resultSet.close ();
	    statement.close ();
	    //System.out.println ("\t\t("+tablename+"contains "+rows+" records)");
	    return rows;
        }
        catch (SQLException sx)
        {
            // ouch! I don't think we should get here.
	    //System.out.println ("count(*) on "+tablename+
	    //		" failed - is this an application problem?");
        }
	return -1;
    }

    // ----------------------------------
    // create and delete our test tables.
    // ----------------------------------

    public int createTestTable (boolean big) throws SQLException
    //
    // ensure the test table exists - if it already exists,
    // find out how big it is. don't catch errors except for
    // ones that may indicate table pre-existence.
    //
    {
        TableManager table = (big ? bigTable : smallTable);
        int rows = -1;

        ensureConnected ();
        Statement statement = MyConnection.createStatement ();
        try
        {
            statement.executeUpdate (table.create);
            rows = 0;
        }
        catch (SQLException sx)
        {
            // creation failed - perhaps the table exists?
	    //System.out.println ("(test to see if table "+table.name+" exists)");
            rows = howBig (table.name);
	    if (rows < 0) 
	    { 
		System.out.println ("*** PROBLEM in SQL \""+table.create+"\"");
		throw sx;
	    }
        }
        finally
        { 
            statement.close ();
        }
        table.ct = rows;
        return rows;
    }

    public void emptyTestTable (boolean big) throws SQLException
    //
    // ensure the test table is empty, if it exists.
    //
    {
        TableManager table = (big ? bigTable : smallTable);

        ensureConnected ();
        Statement statement = MyConnection.createStatement ();
        try
        {
            statement.executeUpdate ("DELETE FROM " + table.name);
        }
        catch (SQLException sx)
        {
            // deletion failed - perhaps the table didn't exist?
        }
        statement.close ();
        table.ct = 0;
    }

    public void dropTestTable (boolean big) throws SQLException
    //
    // ensure the test table doesn't exist.
    //
    {
	TableManager table = (big ? bigTable : smallTable);

        ensureConnected ();
        Statement statement = MyConnection.createStatement ();
        try
        {
            statement.executeUpdate ("DROP TABLE " + table.name);
        }
        catch (SQLException sx)
        {
            // drop failed - perhaps the table didn't exist? 
        }
        statement.close ();
        table.ct = -1;
    }

    // ----------------------
    // insert lots of records
    // ----------------------

    public long insertRecords (int count, int batchSize, boolean big) 
    throws SQLException
    //
    // insert lots of records, reporting the time
    // taken in milliseconds for the main loop.
    //
    {
        TableManager table = (big ? bigTable : smallTable);

        // prepare a statement and fill in the parameter values
        // we won't be varying in the test. (we want to pass over
        // the right number of values, but as we are merely 
        // testing performance of the interface+database, we 
        // don't care what the values are!)

        PreparedStatement ps = MyConnection.prepareStatement(table.insert);
        ps.setDouble(2, 2.0);
        ps.setDouble(3, 3.0);
        for (int i=4; i<=table.fieldct; i++)
        {
            ps.setInt(i, i);
        }

        // start the sequence of inserts

        long start = Recorder.now ();

        if (batchSize <= 1)
        {
            // insert the records one per transaction

            for (int i=1; i<=count; i++)
            {
                ps.setInt(1, ++table.ct);
                ps.executeUpdate ();
            }
        }
        else
        {
            // insert the records in batches, by turning off autocommit
            // and the periodically commiting a batch.

            MyConnection.setAutoCommit (false);
            for ( int i=1; i<=count; i++)
            {
                ps.setInt(1, ++table.ct);
                ps.executeUpdate ();
                if (i % batchSize == 0)
                    MyConnection.commit ();
            }
            // commit the final batch, if necessary
            if (count % batchSize != 0)
                MyConnection.commit ();
            MyConnection.setAutoCommit (true);
        }
        long res = Recorder.now () - start;
        ps.close ();
        return res;
    }

    public void populateTable (int ct, boolean big) throws SQLException
    //
    // ensure the table has a particular number of records, 
    // bulk-deleting or inserting as needed. Also, ensure
    // the table exists!
    //
    {
        TableManager table = (big ? bigTable : smallTable);

        /*System.out.println ("\t\t(populateTable (" + ct + 
                            ", " + big + 
                            ") called, " + 
                            (table.ct < 0 ? "unknown number of" : table.ct) + 
                            " records currently in " + 
                            table.name);
        */

        if (table.ct < 0)
            createTestTable (big);

        if (ct > table.ct)
            insertRecords (ct-table.ct, 25, big);
        else if (ct < table.ct)
        {
            doSQL ("DELETE FROM " + table.name + " WHERE id>" + ct);
            // double-check the table is now the right size.
	    // (if it is not, another application may have been
	    // playing with 'my' table.
	    int actualsize = howBig (table.name);
	    if (actualsize != ct)
	    {
		System.out.println ("\n\napplication error: table " + table.name +
				    " has " + actualsize + 
				    " records, but should have " + ct + "\n");
	    }
	    table.ct = ct;
        }
    }

    // ----------------------
    // delete lots of records
    // ----------------------

    public long deleteRecords (int ct, int batchSize, boolean big) 
    throws SQLException
    //
    // delete the indicated number of records from the relevant test table;
    // return the time taken.
    //
    // note that when deleting a batch of records, we are doing it as 
    // a number of individual record deletions with autocommit off, 
    // rather than a single DELETE statement with a range of records
    // specified in the delete clause. Thus, the test is fair.
    // an alternative approach is to build up an SQL string of the form...
    //    delete from <table> where id in (<num>, ... )
    // and then executing this statement directly
    // instead of using a prepared statement. This, however, could
    // be more work in both client (building up the string) and the 
    // server (parsing versus the use of a prepared statement).
    //
    {
        TableManager table = (big ? bigTable : smallTable);
        PreparedStatement ps = 
            MyConnection.prepareStatement("DELETE FROM " + table.name + 
                                          " WHERE id=?");
        if (ct > table.ct)
            ct = table.ct;
        long start = Recorder.now ();

        if (batchSize <= 1)
        {
            // delete the records one per transaction.

            int rc; 
            for (int i=1; i<=ct; i++)
            {
                ps.setInt(1, table.ct--);
                rc = ps.executeUpdate ();
                if (rc != 1)
                    System.err.println ("\t(warning: " + rc + 
                                        "records deleted, not one!)");
            }
        }
        else
        {
            // delete the records in batches, by turning off
            // autocommit and then periodically calling the
            // commit function. 

            MyConnection.setAutoCommit (false);
            for (int i=1; i<=ct; i++)
            {
                ps.setInt(1, table.ct--);
                ps.executeUpdate ();
                if (i % batchSize == 0)
                    MyConnection.commit ();
            }
            // commit the final batch, if necessary.
            if (ct % batchSize != 0)
                MyConnection.commit ();
            MyConnection.setAutoCommit (true);
        }
        long res = Recorder.now () - start;
        ps.close ();
        return res;
    }


    // ----------------------
    // update lots of records
    // ----------------------

    public long updateRecords (int rowcount, int count, int batchSize, boolean big) 
    throws SQLException
    //
    // update lots of records, reporting the time
    // taken in milliseconds for the main loop.
    //
    {
        int          id    = 0;
        TableManager table = (big ? bigTable : smallTable);

        // prepare a statement but dont fill in the parameter values;
        // we will need to do that inside the main loop, as we want to
        // ensure we actually change the attribute values.
        // (nb - when we do the parameter settings, we need to recall
        // that the id field is the last parameter, all other columns are 
        // one before where one sees them in the insert statement)


        PreparedStatement ps = MyConnection.prepareStatement(table.update);

        // start the sequence of updates

        long start = Recorder.now ();
	double col2 = 2;
	double col3 = 3;

        if (batchSize <= 1)
        {
            // update the records one per transaction

            for (int i=1; i<=count; i++)
            {
                ps.setDouble(1, ++col2);
                ps.setDouble(2, ++col3);
                for (int j=4; j<=table.fieldct; j++)
                {
                    ps.setInt(j-1, -i);
                }
                id = (id % rowcount) + 1;
                ps.setInt(table.fieldct, id);
                ps.executeUpdate ();
            }
        }
        else
        {
            // update the records in batches, by turning off autocommit
            // and the periodically commiting a batch.

            MyConnection.setAutoCommit (false);
            for ( int i=1; i<=count; i++)
            {
                ps.setDouble(1, ++col2);
                ps.setDouble(2, ++col3);
                for (int j=4; j<=table.fieldct; j++)
                {
                    ps.setInt(j-1, -i);
                }
                id = (id % rowcount) + 1;
                ps.setInt(table.fieldct, id);
                ps.executeUpdate ();
                if (i % batchSize == 0)
                    MyConnection.commit ();
            }
            // commit the final batch, if necessary
            if (count % batchSize != 0)
                MyConnection.commit ();
            MyConnection.setAutoCommit (true);
        }
        long res = Recorder.now () - start;
        ps.close ();
        return res;
    }

    // ----------------------
    // query lots of records
    // ----------------------

    public long queryRecords (int rowcount, int count, int batchSize, boolean big) 
    throws SQLException
    //
    // query lots of records, reporting the time
    // taken in milliseconds for the main loop.
    //
    {
        int          id    = 0; // used to decide which record to fetch
        int          ct    = 0; // number of records retrieved to date
        TableManager table = (big ? bigTable : smallTable);

        long start, res;

        if (batchSize <= 1)
        {
            // prepare a statement but dont fill in the parameter value;
            // we will need to do that inside the main loop 

            PreparedStatement ps = MyConnection.prepareStatement(table.query + " where id=?");
            
            // record the time AFTER setting up the statement, since
            // in a typical application the preparation of all necessary
            // statements is only done once, when a program establishes
            // its connection to the server.

            start = Recorder.now ();

            // query the records one per transaction

            for (int i=1; i<=count; i++)
            {
                id = (id % rowcount) + 1;
                ps.setInt(1, id);
                ResultSet rs = ps.executeQuery();
                // iterate over result set to ensure it has all
                // been retrieved from the server.
                for (; rs.next(); ct++)
                {
                }
            }
            res = Recorder.now () - start;
            ps.close ();
        }
        else
        {
            // 'batched query'. use 'where id in (,,,)'.
            // we shall ignore the prepared statement and use 
            // the DoQuery function instead.
            start = Recorder.now ();
            String str = "";
            for ( int i=1; i<=count; i++)
            {
                id = (id % rowcount) + 1;
                if (i % batchSize == 1)
                    str = "" + id;
                else 
                {
                    str = str + "," + id;
                    if (i % batchSize == 0)
                        ct += doQuery ("select * from " + table.name + " where id in (" + str + ")");
                }
            }
            // fetch the final batch, if necessary
            if (count % batchSize != 0)
                ct += doQuery ("select * from " + table.name + " where id in (" + str + ")");
            
            res = Recorder.now () - start;
        }
        if (ct != count) {
        }
        return res;
    }

    // -----------
    // miscellany.
    // -----------

    public void ListTables ()
    // 
    // the standard 'tables' example, reporting the tables in a
    // polyhedra database and information about inheritance.
    //
    // Will not work against non-polyhedra databases as it assumes
    // that the schema metadata is made available in the 'tables'
    // table.
    //
    {
        if (isConnected ())
        {
            try
            {
                String sql          = "select name from tables" +
                                      " where system=false and type=0";
                Statement statement = MyConnection.createStatement();
                ResultSet resultSet = statement.executeQuery(sql);

                // print result set
                System.out.println("Tables:\n");
                for (int row = 1; resultSet.next(); row++)
                    System.out.println ("\t[" + row + "] " + 
                                        resultSet.getString(1));

                // close jdbc objects
                resultSet.close();
                statement.close();
            }

            catch (SQLException sx)
            {
                jdbcError(sx);
            }
        }
    }

    // --------------------
    // housekeeping methods
    // --------------------

    public static void jdbcError(SQLException sex)
    {
        long errorLevel = (sex instanceof SQLWarning) ? 1 : 16;
        if (errorLevel >= errorLevel)
        {
            System.out.println("Msg " + sex.getErrorCode() + 
                               ", Level " + errorLevel +
                               ", State " + sex.getSQLState() + ":");
            System.out.println(sex.toString());
        }

    }

    protected void finalize() throws SQLException
    {
        if (MyConnection != null)
            MyConnection.close();
    }
}


//-----------------------------------------------------------------------------
//                T E S T _ P E R F O R M A N C E
//-----------------------------------------------------------------------------


final class test_performance
//
// the class to run the various tests, making use of the
// connectionManager class to do the donkey work.
//
{   
    private connectionManager Conn = null;

    static int opCount =  0;
    static int batch   = 25;

    // -----------------------------------------------------------------------

    private void VersionInfo () throws SQLException
    {
        if (Conn == null)
            Conn = new connectionManager ();
        //System.out.println ("(entering VersionInfo() function...)");
        Conn.ensureConnected ();

        //System.out.println ("(still in VersionInfo() function, now connected...)");
        Conn.GetMetaData ();
        //System.out.println ("(still in VersionInfo() function, get metadata...)");
        Conn.dropTestTable (true);
        //System.out.println ("(still in VersionInfo() function, dropped wide table...)");
        Conn.dropTestTable (false);
        //System.out.println ("(still in VersionInfo() function, dropped narrow table...)");
        Conn.disconnect ();
        //System.out.println ("(still in VersionInfo() function, now disconnected.)");
    }

    // -----------------------------------------------------------------------

    private int ConnectCycle (int ct) throws SQLException
    {
        Recorder.setTestGroup ("Connecting", "connect/disconnect cycle",
                               "how fast can we establish and drop connections?"
                              );
        if (Conn == null)
            Conn = new connectionManager ();

        long start = Recorder.now ();
        for (int i = 1; i < ct; i++)
        {
	    Conn.ensureConnected ();
	    Conn.disconnect ();
        }
        int res = Recorder.calculate_performance (start, ct, 1, "CONN");
        return res;
    }

    private int CreateDropCycle (int ct) throws SQLException
    {
        Recorder.setTestGroup ("Creating & dropping", "create/drop cycle",
                               "how fast can we establish and drop tables?"
                              );
        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();
        long start = Recorder.now ();
        for (int i = 1; i < ct; i++)
        {
            Conn.dropTestTable (true);
            Conn.createTestTable (true);
        }
        int res = Recorder.calculate_performance (start, ct, 1, "TABL");
        Conn.disconnect ();
        return res;
    }

    // -----------------------------------------------------------------------
    // test insert speed.
    // -----------------------------------------------------------------------

    private void insertRecords (int ct, int initPop, 
                                int batch, 
                                boolean big, 
                                String test) 
    throws SQLException
    //
    // insert some records and record the performance
    //
    {
        // report what we are about to do.

        String batchinfo = " in batches of " + batch;
        String popinfo   = ", where table already has " + initPop + " records";
        System.out.println ("\n\t" + test + ": insert " + ct + 
                            (big ? " big" : "") + " records" +
                            (batch > 1 ? batchinfo : "")     +
                            (initPop > 0 ? popinfo : "")
                           );

        // ensure there are the right number of initial records in the table.

        Conn.populateTable (initPop, big);

        // do the test and record the results.

        long msecs = Conn.insertRecords (ct, batch, big);
        Recorder.record_performance (msecs, ct, batch, test);
    }

    private void TestInserts (int ct) throws SQLException
    //
    // run a series of tests to find out how fast we can insert records
    //
    {
        Recorder.setTestGroup ("Inserting", "insert",
                               "how fast can we insert records?" +
                               "\n\thow much slower are inserts if there are many attributes?" +
                               "\n\thow much does batching up the inserts improve performance?" +
                               "\n\thow much does the size of the table affect insert speed?"
                              );

        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();

        insertRecords (ct, 0,     1,     false, "I5 ");
        insertRecords (ct, 0,     1,     true,  "I50");
        insertRecords (ct, 0,     batch, false, "I5B");
        insertRecords (ct, ct*10, 1,     false, "I5P");

        // clean up:
        Conn.dropTestTable (true);
        Conn.dropTestTable (false);
        Conn.disconnect ();
    }

    // -----------------------------------------------------------------------
    // test deletion speed
    // -----------------------------------------------------------------------

    private void deleteRecords (int ct, int initPop, 
                                int batch, 
                                boolean big, 
                                String test) 
    throws SQLException
    //
    // insert some records and record the performance
    //
    {
        // report what we are about to do.

        String batchinfo = " in batches of " + batch;
        String popinfo   = ", where table already has " + initPop + " records";
        System.out.println ("\n\t" + test + ": delete " + ct + 
                            (big ? " big" : "") + " records" +
                            (batch > 1 ? batchinfo : "")     +
                            (initPop > 0 ? popinfo : "")
                           );

        // ensure there are the right number of initial records in the table.

        Conn.populateTable (initPop+ct, big);

        // do the test and record the results.

        long msecs = Conn.deleteRecords (ct, batch, big);
        Recorder.record_performance (msecs, ct, batch, test);
    }

    private void TestDeletes (int ct) throws SQLException
    //
    // run a series of tests to find out how fast we can insert records
    //
    {
        Recorder.setTestGroup ("Deleting", "deletion",
                               "how fast can one delete individual records?" +
                               "\n\thow much does batching improve the performance?" +
                               "\n\thow much does table size affect the deletion rate?"
                              );

        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();
        deleteRecords (ct, 0,     1,     false, "D5 ");
        deleteRecords (ct, 0,     batch, false, "D5B");
        deleteRecords (ct, 0,     1,     true , "D50");
        deleteRecords (ct, ct*10, 1,     false, "D5P");

        // clean up:
        Conn.dropTestTable (true);
        Conn.dropTestTable (false);
        Conn.disconnect ();
    }

    // -----------------------------------------------------------------------
    // test update speed.
    // -----------------------------------------------------------------------

    private void updateRecords (int ct, int initPop, 
                                int batch, 
                                boolean big, 
                                String test) 
    throws SQLException
    //
    // insert some records and record the performance
    //
    {
        // report what we are about to do.

        String batchinfo = " in batches of " + batch;
        String popinfo   = ", where table has " + initPop + " records";
        System.out.println ("\n\t" + test + ": update " + ct + 
                            (big ? " big" : "") + " records" +
                            (batch > 1 ? batchinfo : "")     +
                            (initPop > 0 ? popinfo : "")
                           );

        // ensure there are the right number of initial records in the table.

        Conn.populateTable (initPop, big);

        // do the test and record the results.

        long msecs = Conn.updateRecords (initPop, ct, batch, big);
        Recorder.record_performance (msecs, ct, batch, test);
    }

    private void TestUpdates (int ct) throws SQLException
    //
    // run a series of tests to find out how fast we can update records
    //
    {
        int tablesize = (ct < 1000 ? ct : 1000);
        Recorder.setTestGroup ("Updating", "update",
                               "how fast can we update records?" +
                               "\n\thow much slower are updates if there are many attributes?" +
                               "\n\thow much does batching up the updates improve performance?" +
                               "\n\thow much does the size of the table affect update speed?"
                              );

        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();

        updateRecords (ct, tablesize,    1,     false, "U5 ");
        updateRecords (ct, tablesize,    1,     true,  "U50");
        updateRecords (ct, tablesize,    batch, false, "U5B");
        updateRecords (ct, tablesize*10, 1,     false, "U5P");

        // clean up:
        Conn.dropTestTable (true);
        Conn.dropTestTable (false);
        Conn.disconnect ();
    }

    // -----------------------------------------------------------------------
    // test query speed.
    // -----------------------------------------------------------------------

    private void queryRecords (int ct, int initPop, 
                                int batch, 
                                boolean big, 
                                String test) 
    throws SQLException
    //
    // insert some records and record the performance
    //
    {
        // report what we are about to do.

        String batchinfo = " in batches of " + batch;
        String popinfo   = ", where table has " + initPop + " records";
        System.out.println ("\n\t" + test + ": retrieve " + ct + 
                            (big ? " big" : "") + " records" +
                            (batch > 1 ? batchinfo : "")     +
                            (initPop > 0 ? popinfo : "")
                           );

        // ensure there are the right number of initial records in the table.

        Conn.populateTable (initPop, big);

        // do the test and record the results.

        long msecs = Conn.queryRecords (initPop, ct, batch, big);
        Recorder.record_performance (msecs, ct, batch, test);
    }

    private void TestQueries (int ct) throws SQLException
    //
    // run a series of tests to find out how fast we can update records
    //
    {
        int tablesize = (ct < 1000 ? ct : 1000);
        Recorder.setTestGroup  ("Query", "retrieve",
                                "how fast can we retrieve individual records when we know the PK?" +
                                "\n\thow is retrieval time affected by the number of attributes?" +
                                "\n\thow is retrieval time affected by the size of table?");

        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();

        queryRecords (ct, tablesize,    1,     false, "Q5 ");
        queryRecords (ct, tablesize,    1,     true,  "Q50");
        queryRecords (ct, tablesize,    batch, false, "Q5B");
        queryRecords (ct, tablesize*10, 1,     false, "Q5P");

        // clean up:
        Conn.dropTestTable (true);
        Conn.dropTestTable (false);
        Conn.disconnect ();
    }
    
    // -----------------------------------------------------------------------
    // special code to test query space
    // -----------------------------------------------------------------------

    private void TestQuery (int ct) throws SQLException
    //
    // run a series of tests to find out how fast we can query records
    //
    {
        String test = "X5B";
	int batch = 5;
	int tablesize = (ct < 1000 ? ct : 1000);
        Recorder.setTestGroup  ("Query2", "retrieve",
                                "how fast can we retrieve individual records, not using prepared queries?");

        if (Conn == null)
            Conn = new connectionManager ();

        Conn.ensureConnected ();

	System.out.println ("\n\t" + test + ": retrieve " + ct + 
			    " records" 
			    );

	// ensure there are the right number of initial records in the table.

	Conn.populateTable (batch, false);

	// do the test and record the results.
	long start = Recorder.now ();
        for (int i = 1; i < ct/batch; i++)
        {
	    Conn.doQuery(Conn.smallTable.query);
        }

	Recorder.record_performance (Recorder.now()-start, ct, batch, test);

        // clean up:
        Conn.dropTestTable (true);
        Conn.dropTestTable (false);
        Conn.disconnect ();
    }

    // -----------------------------------------------------------------------
    // work function.
    // -----------------------------------------------------------------------

    public void work () throws SQLException
    {
        long start = Recorder.now ();
        System.out.println ("\nPolyhedra performance tester (using JDBC API);" + 
                            "\n\tserver = " + Conn.url + 
                            ", opcount = " + opCount + ".\n\n");

        VersionInfo ();
        
        // initial tests said that if we get (say) 40 cycles per second, an
        // opcount of 200 is probably appropriate (so that no individual subtest
        // too short a time for a reasonable measurement)

        if (opCount == 0)
        {
	    int scaletest = ConnectCycle (50);
            opCount = (scaletest > 0) ? ((7 * scaletest)/10)*10 : 100 ;
            System.out.println ("opcount tuned to " + opCount + "\n\n");
        }
	else
	{
	    // before doing the first timed test, to some work so that the
	    // bulk of the driver is compiled.
	    //System.out.println ("(exercise the driver briefly to give time for code compilation)");
	    Conn.ensureConnected ();
	    Conn.createTestTable (false);
	    Conn.insertRecords (opCount, 1, false);
	    Conn.dropTestTable (false);
	    Conn.disconnect ();
	}
	
        TestInserts (opCount);
        TestDeletes (opCount);
        TestUpdates (opCount);
        TestQueries (opCount);
	//TestQuery (opCount);

        System.out.println ("\n");
        Recorder.calculate_performance (start, 1, 1, "total/" + opCount);
        Recorder.report_performance ();
    }
}


//-----------------------------------------------------------------------------
//               J D B C A P I
//-----------------------------------------------------------------------------


public final class jdbcapi
//
// the main class - or more accurately, the class with main.
//
{
    public static void main (String[] argv)

    throws SQLException
    ,      ClassNotFoundException
    ,      InstantiationException
    ,      IllegalAccessException
    {
        jdbcapi api = new jdbcapi ();

        // load Polyhedra JDBC Driver
        // automatically registers with JDBC Driver Manager

        // note: the newInstance() is required for Visual J++
        Class.forName ("com.polyhedra.jdbc.JdbcDriver").newInstance();

        // get url
        if (argv.length > 0) // use 1st commandline arg if specified
            connectionManager.url = "jdbc:polyhedra://:" + argv[0];
        else
            connectionManager.url = "jdbc:polyhedra://:8001";

        // get opcount
        if (argv.length > 1) // use 2nd commandline arg for opcount
            test_performance.opCount = Integer.parseInt (argv[1]);

        // get name
        if (argv.length > 2) // use 3nd commandline arg for user name
            connectionManager.uid = argv[2];

        // get password
        if (argv.length > 3) // use 4nd commandline arg for password
            connectionManager.pwd = argv[3];

        try
        {
            test_performance tester = new test_performance ();
            tester.work ();
        }

        catch (SQLException sx)
        {
            connectionManager.jdbcError (sx);
        }
    }
}

/*---------------------------------------------------------------------------*/
/*                          e n d   o f   f i l e                            */
/*---------------------------------------------------------------------------*/



