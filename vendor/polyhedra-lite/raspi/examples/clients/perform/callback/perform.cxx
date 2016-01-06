/*-+-----------------------------------------------------------------------+-//
//                                                                           //
//             P O L Y H E D R A    T E S T    L I B R A R Y                 //
//                                                                           //
//                Copyright (C) 1999-2015 by Enea Software AB                //
//                           All Rights Reserved                             //
//                                                                           //
//---------------------------------------------------------------------------//
//
//-+ Filename    : perform.cxx
//-+ Description : Client API timer tests.
//
//
//-+-----------------------------------------------------------------------+-*/

//#define EXTRA

// -----------------------------------------------------------------------------

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

#include "common.hxx"

// pick up all the client api headers that we use in this demo.

#include <appapi.h>
#include <timerapi.h>
#include <clntapi.h>
#include <queryapi.h>
#include <transapi.h>
#include <commandapi.h>

// define some useful constants

// define the verbosity of the program: if you want more messages,
// increase the value of verbosity appropriately. This is a debugging aid.
#define VERBOSITY     0
#define REALLYVERBOSE (VERBOSITY >= 2)
#define VERBOSE       (VERBOSITY >= 1)

#define BGTIMEOUT     10*3600

#define BIG     TRUE
#define SMALL   FALSE
#define LEAVE   FALSE
#define CLEANUP TRUE

#if defined(INTEGRITY)
#define Connection CaConnection
#endif


// -----------------------------------------------------------------------------
// declare our other classes, to allow mutual references when we define them.
// -----------------------------------------------------------------------------


class ControlObject;          // we will have just one of these objects

class ControlledObject;       // (abstract class)
class Connection;             // handles connections
class Tracker;                // (abstract class for one-shots)
class StaticQueryObject;      // handles static queries
class PreparedSQLObject;      // handles prepared queries
class UpdateObject;           // handles SQL transactions


// -----------------------------------------------------------------------------
//                       C o n t r o l O b j e c t
// -----------------------------------------------------------------------------
// define a class to keep track of what is happening: we will have just
// one of these. It defines the various (static) functions that the
// client api will be calling to signal that it has done its work.
// -----------------------------------------------------------------------------


class ControlObject
{
    TransAPI*           Trans;
    TimerAPI*           MyTimer;
    TimerAPI*           MyBGTimer;

protected:

    friend class        ControlledObject;
    friend class        Tracker;

    AppAPI*             App;
    Tracker*            CompletedTrackers;

public:

    const char*         ServerName;
    Connection*         MyConnection;
    int                 Res;
    int                 InScheduler;

    ControlObject (const char* name)
    {
        // save the server name
        ServerName           = name;
        Res                  = 0;
        MyConnection         = NULL;
        Trans                = NULL;
        MyTimer              = NULL;
        MyBGTimer            = NULL;
        CompletedTrackers    = NULL;
        InScheduler          = FALSE;

        // create an AppAPI object to hold context for the scheduler
        App                  = AppAPI::Create ();
        CreateBackgroundTimer ();
    };

    virtual ~ControlObject ()
    {
        if (MyTimer   != NULL) TimerAPI::StopTimer (MyTimer);
        if (MyBGTimer != NULL) TimerAPI::StopTimer (MyBGTimer);
        Disconnect ();
        AppAPI::Delete(App);
    };

    // scheduler interaction and housekeeping

    int Run (const char* operation)
    {
        if (REALLYVERBOSE)
        {
            if (operation == NULL)
                fprintf (stderr, "ControlObject::Run (NULL) called.\n");
            else
                fprintf (stderr, "ControlObject::Run (\"%s\") called.\n", 
                         operation);
        }
        InScheduler = TRUE;
        AppAPI::Start (App, ControlObject::DoSomething, this);
        InScheduler = FALSE;
        if (VERBOSE)
        {
            if (operation == NULL)
                fprintf (stderr, "\tControlObject::Run (NULL) done, res = %d.\n", Res);
            else
                fprintf (stderr, "\tControlObject::Run (\"%s\") done, res = %d.\n", operation, Res);
        }
        return Res;
    };


    static const int DoSomething (void *userdata)
    {
        // called by the client API scheduler once it has been granted control.
        //
        // Given the way the demo has been coded, we will not have to do
        // anything here (other than tidying up any completed Tracker objects);
        // everything necessary for the next stage of the demo
        // will have been initiated prior to the call of AppAPI::Start () which
        // had this function as a parameter.

        if (userdata != NULL)
            ((ControlObject*) userdata)->TidyUp ();

        return 0; // false - that is, don't call me again! 
    }

    const void Done (int res)
    {
        if (REALLYVERBOSE)
            fprintf (stderr, "\t\tControlObject::Done (%d) called.\n", res);
        Res = res;
        if (InScheduler)
            AppAPI::Stop (App);
        else if (VERBOSE)
            fprintf (stderr, "\t\t(were not in scheduler! Res = %d)\n", Res);
    }

    const void TidyUp ();

    int Peek ()
    {
        // enter the scheduler, and then leave it immediately.

        AppAPI::Start (App, ControlObject::DoNothing, this);
        return Res;
    };

    static const int DoNothing (void *userdata)
    {
        // used when testing how fast one can enter & leave the scheduler;
        // when the scheduler is called with this entry point, it should
        // immediately exit.

        ControlObject* co = (ControlObject*) userdata;
        AppAPI::Stop (co->App);
        return 0; // false - that is, don't call me again! 
    }

    // initiate a connection. The body of this function is defined later.

    int  Connect ();                    

    // close a connection. The body of this function is defined later.

    int Disconnect ();                    

    // wait in scheduler for a while

    int  PauseInScheduler (int deciseconds)
    {
        if (MyTimer == NULL)
        {
            MyTimer  = 
            TimerAPI::CreateOneShotTimer ( App,
                                           deciseconds, 
                                           ControlObject::TimeOut,
                                           this
                                         );
            return Run ("pause");
        }
        else
        {
            fprintf (stderr, 
                     "Application error? Apparently we are already paused.\n");
            return -1;
        }
    };
    static const void TimeOut (void *userdata)
    {
        ControlObject* co = (ControlObject*) userdata;
        co->MyTimer = NULL;
        co->Done (0);
    };

    // a background timer object so the scheduler is not idle

    void CreateBackgroundTimer ()
    {
        if (MyBGTimer == NULL)
        {
            if (REALLYVERBOSE)
                fprintf (stderr, "(CreateBackgroundTimer restarted)\n");
            MyBGTimer  = 
            TimerAPI::CreateOneShotTimer ( App,
                                           BGTIMEOUT, 
                                           ControlObject::BGTimeOut,
                                           this
                                         );
        }
        else
            fprintf (stderr, "* * * * problem with background timer.\n");
    };
    static const void BGTimeOut (void *userdata)
    {
        ControlObject* co = (ControlObject*) userdata;
        co->MyBGTimer = NULL;
        co->CreateBackgroundTimer ();
    };

    // do something to the database
    int AlterDatabase (const char* sql, int ct, int hard);

    // do a query on the database
    int DoQuery (const char* sql, int* rowct);

    // find the size of the table, which must exist (otherwise the
    // query will generate an assertion error. Assume the connection is open.

    int size_of_table (const char* tablename)
    {
        int id    = 0;
        int rowct = 0;
        char buffer [256];
        // make sure there's room in the buffer.
        assert (strlen(tablename)<200);
        sprintf (buffer, "select count(*) id from %s", tablename);
        id = DoQuery ((const char*) buffer, &rowct);
        assert (rowct == 1);
        if (REALLYVERBOSE)
            printf ("\t\t(table %s exists, with %d records.)\n", tablename, id);
        return id;
    }

    // create a table (connecting to the database if necessary, and
    // leaving the connection open. Don't complain if the table exists,
    // simply return the size of it.

    int create_table (const char* createstring, const char* tablename)
    {
        int res;

        if (MyConnection == NULL)
            if ((res = Connect ()) != 0) return res;

        res = AlterDatabase (createstring, 1, FALSE);
        if (res == 0) return 0;

        return size_of_table (tablename);
    }

    // prepare a query or update on the database...
    PreparedSQLObject* PrepareSQL (const char* sql, int argct, int batchct);
    // and execute it.
    int RunPreparedQuery (PreparedSQLObject* pso, int* argptr);
    int RunPreparedUpdate (PreparedSQLObject* pso, int* argptr, int* valueptr, double* doubleptr);


    virtual int Perform () = 0;
};


// ----------------------------------------------------------------------------
//                   C o n t r o l l e d O b j e c t
// ----------------------------------------------------------------------------
// abstract class with an owning ControlObject
// ----------------------------------------------------------------------------


class ControlledObject
{

protected:

    ControlObject*       Owner;

    ControlledObject (ControlObject* owner)
    {
        Owner  = owner;
    };

    virtual ~ControlledObject ()
    {
    };

    int Run (const char* operation)
    {
        return Owner->Run (operation);
    };

    void Done (int res)
    {
        if (REALLYVERBOSE)
            fprintf (stderr, "\t\tControlledObject::Done (%d) called.\n", res);
        Owner->Done (res);
    };

    AppAPI* GetApp ()
    {
        return Owner->App;
    };

    ClientAPI* GetClient ();
    // (method defined later, after Connection class defined)
};


// ----------------------------------------------------------------------------
//                          C o n n e c t i o n
// ----------------------------------------------------------------------------
// handle a connection into an indicated server.
// ----------------------------------------------------------------------------


class Connection : public ControlledObject
{
public:

    ClientAPI* Client;
    int        ConnectRes;

    Connection (ControlObject* owner, const char* name) 
    : ControlledObject (owner)
    {
        if (VERBOSE)  fprintf (stderr, "connecting to %s...\n", name);
        ConnectRes = 0;
        Client = ClientAPI::StartConnect ( GetApp (), 
                                           name,
                                           Connection::ConnectedCallBack,
                                           this
                                         );
        ConnectRes = -1;
        ConnectRes = Run ("connect");
    };

    virtual ~Connection ()
    {
        Disconnect ();
    };

    static const void ConnectedCallBack (void *userdata)
    {
        Connection *c = (Connection *) userdata;
        char        buf[256];
        int         res = ClientAPI::GetError (c->Client, buf, 255);
        c->ConnectRes = res;

        if (res != 0)
        {
            fprintf (stderr, "connect failed %d - %s.\n", res, buf);
            ClientAPI::DeleteClient ( c->Client,
                                      Connection::DisconnectedCallBack,
                                      c
                                    );         
        }
        else
        {
            if (VERBOSE) fprintf (stderr, "\tconnected!\n");
            c->Done (res);
        }
    };

    int Disconnect ()
    {
        if (Client != NULL)
        {
            if (VERBOSE) fprintf (stderr, "disconnecting...\n");
            ClientAPI::DeleteClient ( Client,
                                      Connection::DisconnectedCallBack,
                                      this
                                    );
            if (VERBOSE) fprintf (stderr, "\t\tRes = %d\n", Owner->Res);
            return Run ("disconnect");
        }
        return 0;
    };

    static const void DisconnectedCallBack (void *userdata)
    {
        Connection *c = (Connection *) userdata;
        c->Disconnected();
    }

    void Disconnected ()
    {
        int res = ClientAPI::GetError (Client);

        if (res != 0)
        {
            fprintf (stderr, "disconnect failed %d.\n", res);
        }
        else
        {
            if (VERBOSE) fprintf (stderr, "\tdisconnected!\n");
        }
        Client     = NULL;
        if (ConnectRes != 0)
            Done (ConnectRes);
        else
        {
            ConnectRes = res;
            Done (res);
        }
    };
};


ClientAPI* ControlledObject::GetClient ()
//
// define ControlledObject method that needs to know structure of Connection
//
{
    return Owner->MyConnection->Client;
}

// ----------------------------------------------------------------------------
//                             T r a c k e r
// ----------------------------------------------------------------------------
// an abstract class from which the classes for handling one-shot operations
// are derived, so that they can easily be deleted later.
// ----------------------------------------------------------------------------


class Tracker : public ControlledObject
{
    int            StopWhenDone;

    friend class   ControlObject;

protected:

    Tracker*       NextObject;

    Tracker (ControlObject* owner, int stop) : ControlledObject (owner)
    {
        StopWhenDone = stop;
    };

    void Completed (int res = 0)
    {
        NextObject = Owner->CompletedTrackers;
        Owner->CompletedTrackers = this;
        if (StopWhenDone == TRUE) Done (res);
    };
};


//-----------------------------------------------------------------------------
//                          S t a t i c Q u e r y O b j e c t
// -----------------------------------------------------------------------------
// class to launch a static query when created; control is returned when the
// query is complete.
// -----------------------------------------------------------------------------


class StaticQueryObject : protected Tracker
{
    QueryAPI*   Query;
    const char* SQL;   // the operation to perform
    int         Count; // how many times to do the operation

protected:
    friend class ControlObject;

public:

    int         RowCount; // number of rows returned by the query
    int         LastID;   // place to put id field returned by query

    StaticQueryObject (ControlObject* owner, const char* sql)
    : Tracker (owner, TRUE)
    {
        SQL      = sql;
        RowCount = 0;
        LastID   = -1;
        LaunchQuery ();
    }

    const void LaunchQuery ()
    {
        Query = QueryAPI::StartQuery ( GetClient (), 
                                       SQL,
                                       StaticQueryObject::Row, 
                                       StaticQueryObject::QueryDone, 
                                       this
                                     );
    };

    static const void Row (void *userdata)
    /*
     * increment the row count - and also steal a copy of the id column, if there is one.
     */
    {
        StaticQueryObject* sqo = (StaticQueryObject*) userdata;
        sqo->RowCount ++;
        // get "id"? Don't worry if there is no such attribute
        int res = QueryAPI::CopyColumn(sqo->Query, "id", &(sqo->LastID), sizeof(sqo->LastID));
        if (res == 0)
            {
                if (VERBOSE)
                    printf ("(no id attribute in query \"%s\")\n", sqo->SQL);
            }
        else if (REALLYVERBOSE)
            printf ("(id attribute holds %d in query \"%s\")\n", sqo->LastID,sqo->SQL);
    }

    static const void QueryDone (void *userdata)
    {
        StaticQueryObject* sqo = (StaticQueryObject*) userdata;
        char               buf[256];
        int                res = QueryAPI::GetError(sqo->Query, buf, 255);
        if (VERBOSE && res != 0)
            printf ("**** %d returned when handling the query:\n\t%s\n",res, buf);
        assert (res==0);
        sqo->Completed (sqo->LastID);
    }
};


// ----------------------------------------------------------------------------
//                             S c o u t
// ----------------------------------------------------------------------------
// an abstract class from which the classes for handling prepared queries etc
// can be derived. Scout motto: be prepared.
// ----------------------------------------------------------------------------


class Scout : public ControlledObject
{
    int            StopWhenDone;

    friend class   ControlObject;

    const char*    SQL;  /* for reporting/debugging? */
    CommandAPI*    Command;
    TransAPI*      Trans;
    int            BatchSize; // max size of batches (autoflush at his value)
    int            BatchCt;   // ops so far this batch

protected:

    Scout (ControlObject* owner, const char* sql, int stop, int batchsize) : ControlledObject (owner)
    {
        StopWhenDone = stop;
        SQL          = sql;
        Trans        = NULL;
        BatchSize    = batchsize;
        BatchCt      = 0;
        Command      = CommandAPI::CreateCommand (GetClient(), sql);
        int res = CommandAPI::StartPrepare (Command, Scout::PrepareCommandDone, this);
        Run ("Prepare SQL");
    };
    
    virtual ~Scout ()
    {
        DeleteTrans ();
        CommandAPI::DeleteCommand (Command, Scout::DeleteCommandDone, this);
        Run ("Delete prepared SQL");
    }

    CommandAPI* GetCommand ()
    {
        return Command;
    }

    TransAPI* GetTrans ()
    {
        if (Trans == NULL)
            Trans = TransAPI::CreateTrans (GetClient ());
        return Trans;
    }

    const char* GetSQL ()
    {
        return SQL;
    }

    void DeleteTrans ()
    {
        if (Trans != NULL)
        {
            TransAPI::DeleteTrans ( Trans,
                                    Scout::TransactionDeleted,
                                    this
                                  );
            Run ("delete transaction");
            Trans = NULL;
        }
    }

    static const void PrepareCommandDone (void *userdata)
    {
        Scout* s   = (Scout*) userdata;
        char   buf[256];
        int    res = QueryAPI::GetError(s->Command, buf, 255);
        if (VERBOSE && res != 0)
            printf ("**** rc=%d when preparing SQL statement - %s\n\tSQL was %s\n", res, buf, s->SQL);
        assert (res==0);
        s->Done (res);
    }

    static const void DeleteCommandDone (void *userdata)
    {
        Scout* s = (Scout*) userdata;
        s->Done (0);
    }

    void Completed (int res = 0)
    {
        if (StopWhenDone == TRUE) Done (res);
    };

    static const void QueryDone (void *userdata)
    {
        Scout* s = (Scout*) userdata;
        char   buf[256];
        int    res = QueryAPI::GetError(s->GetCommand(), buf, 255);
        if (res != 0)
            printf ("**** %d returned when handling the query - %s\n\tSQL was %s\n",res, buf, s->SQL);
        assert (res == 0);
        s->Done (res);
    }

    int AddCommand (const void (*collectArgs)(CommandAPI *, void *))
    //
     {
        int res = TransAPI::AddCommand ( GetTrans(),
                                         GetCommand (),
                                         collectArgs,
                                         this
                                       );
        BatchCt ++;
        FlushBatch (BatchSize);
        return 0;
    };

    int FlushBatch (int limit = 1)
    //
    // flush any pending operations if the batch is full; call with an arg
    // of one to flush
    {
        int res = 0;
        if (BatchCt >= limit)
        {
            res = TransAPI::Commit ( Trans,
                                     Scout::UpdateCallback,
                                     Scout::TransactionDone,
                                     this
                                   );
            Run ("execute prepared statement");
            BatchCt = 0;
            // note that if we wanted to, we could delete the TransAPI object
            // here - but it is more efficient to keep it around for re-use.
        }
        return res;
    }


    static const void UpdateCallback (QueryAPI *query, void *userdata)
    {
        //Scout* s = (Scout*) userdata;
        // we have to supply a function - but it does not have to do anything!
    }

    static const void TransactionDone (void *userdata)
    {
        Scout* s   = (Scout*) userdata;
        char   buf[256];
        int    res = TransAPI::GetError(s->Trans, buf, 255);
        if (res != 0)
            printf ("return code for transaction is %d - %s\n\t\t SQL = %s\n",
                    res, buf, s->SQL);
        assert (res == 0);
        s->Completed (res);
    }

    static const void TransactionDeleted (void *userdata)
    {
        Scout* s = (Scout*) userdata;
        s->Trans = NULL;
        s->Completed (0);
    }
};


//-----------------------------------------------------------------------------
//                        P r e p a r e d S Q L O b j e c t
// -----------------------------------------------------------------------------
// class to prepare an SQL command, and launch it when asked; control is
// returned when the object has been prepared, and when the query or update
// is complete.
// -----------------------------------------------------------------------------


class PreparedSQLObject : protected Scout
{
    int       ArgCt;     // number of args that will have to be supplied - default 1.
    int*      IdPtr;     // pointer to value to supply as 'id' argument
                         // (id of record to retrieve, or update, for example)
    int*      ValuePtr;  // pointer to value to supply for all other integerargs
    double*   DoublePtr; // pointer to value to supply for all double args
    int       RowCount;  // number of rows retrieved

protected:
    friend class ControlObject;

public:

    PreparedSQLObject (ControlObject* owner, const char* sql, int argct, int batchsize)
    : Scout (owner, sql, TRUE, batchsize)
    {
        ArgCt     = argct;
        if (REALLYVERBOSE)
            printf ("\t\tPreparedSQLObject(owner,\n"
                    "\t\t                  %s\n"
                    "\t\t                  %d, %d)\n", sql, argct, batchsize);
    }

    int PerformQuery (int* idptr = NULL)
    {
        IdPtr    = idptr;
        RowCount = 0;
        int res = CommandAPI::StartQuery ( GetCommand (),
                                           PreparedSQLObject::Row,
                                           Scout::QueryDone,
                                           this,
                                           PreparedSQLObject::CollectArgsCallback
                                         );
        Run ("execute query");
        return RowCount;
    };

    int PerformTransaction (int* idptr = NULL, int* valueptr = NULL, double* doubleptr = NULL)
    //
    // update the database (using the previous TransAPI object, if there is one)
    //
    {
        IdPtr    = idptr;
        ValuePtr = valueptr;
        DoublePtr = doubleptr;

        return AddCommand (PreparedSQLObject::CollectArgsCallback);
    };

    void Flush ()
    {
        FlushBatch ();
    }

    static const void CollectArgsCallback(CommandAPI *command, void *userdata)
    {
        PreparedSQLObject *pso = (PreparedSQLObject *)userdata;

        if (pso->ArgCt >= 1)
        {
            // id
            int res = QueryAPI::AddArg(command, NULL, 1, pso->IdPtr, sizeof(int));
            if (REALLYVERBOSE && res != 0) printf ("failed to assign arg 1");
            assert (res == 0);
        }

        if (pso->ArgCt >= 2)
        {
            // col2
            int res = QueryAPI::AddArg(command, NULL, POLY_TYPE_FLOAT, pso->ValuePtr, sizeof(*(pso->ValuePtr)));
            if (REALLYVERBOSE && res != 0) printf ("failed to assign arg 2");
            assert (res == 0);
        }
        if (pso->ArgCt >= 3)
        {
            // col3
            int res = QueryAPI::AddArg(command, NULL, POLY_TYPE_FLOAT, pso->DoublePtr, sizeof(*(pso->DoublePtr)));
            if (REALLYVERBOSE && res != 0) printf ("failed to assign arg 3");
            assert (res == 0);
        }

        for (int i=4; i<=pso->ArgCt; i++)
        {
            // col4 ...
            int res = QueryAPI::AddArg(command, NULL, POLY_TYPE_INTEGER, pso->ValuePtr, sizeof(*(pso->ValuePtr)));
            if (REALLYVERBOSE && res != 0) printf ("failed to assign arg %d",i);
            assert (res == 0);
        }
    }

    static const void Row (void *userdata)
    //
    // called once for each row returned. we can pick up the row contents
    // using functions defined by QueryAPI: the values are already available
    // in a buffer the client's address space, so there are no round trips
    // to the server involved in this.
    //
    // for this application it suffices to keep track of how many rows have
    // been returned.
    //
    {
        PreparedSQLObject* pso = (PreparedSQLObject*) userdata;
        pso->RowCount ++;
    }
};


// ----------------------------------------------------------------------------
//                        U p d a t e O b j e c t
// ----------------------------------------------------------------------------
// a class to perform updates to the database a designated number of times,
// optionally quitting out of the scheduler when the work is done.
//
// a repeat count of zero will be taken to mean that it is to be 
// attempted once, but no error message is to be generated if
// it fails.
// ----------------------------------------------------------------------------


class UpdateObject : protected Tracker
{
    TransAPI*      Trans;
    const char*    SQL;   // the operation to perform
    int            Count; // how many times to do the operation
    int            Hard;  // complain if the update fails?

public:

    UpdateObject ( ControlObject* owner,
                   const char*    sql,
                   int            ct   = 1,
                   int            hard = TRUE
                 )
    : Tracker (owner, TRUE)
    {
        SQL   = sql;
        Count = ct;
        Hard  = hard;
        if (REALLYVERBOSE)
            printf ("UpdateObject(*, %s, %d, %s)\n", sql, ct, hard==TRUE ? "hard" : "soft");
        Launch ();
    }

    const void Launch ()
    {
        // start off a new SQL transaction to update the database
        Trans = TransAPI::StartTrans ( GetClient (),
                                       SQL,
                                       UpdateObject::UpdateDone, 
                                       this
                                     );
    };

    static const void UpdateDone (void *userdata)
    {
        // all done - check for error, and put the completed object on the
        // chain of update monitor objects that can be deleted
        // (or repeat the operation if it worked and the repeat count had
        // not been met)

        UpdateObject *uo    = (UpdateObject *)userdata;
        char          buf[256];
        int           res   = TransAPI::GetError(uo->Trans, buf, 255);

        uo->Trans = 0;

        if (res != 0)
        {
            if (uo->Hard || REALLYVERBOSE)
            {
                fprintf ( stderr,
                          "transaction \"%s\" failed %d:\n\t%s\n", 
                          uo->SQL, res, buf
                        );
            }
            assert (uo->Hard != TRUE);
            uo->Completed (res);
        }
        else
        {
            if (VERBOSE) fprintf (stderr, "%s\n", uo->SQL);
            if (uo->Count > 1)
            {
                if (REALLYVERBOSE)
                    fprintf (stderr, "repeating transaction \"%s\".\n", uo->SQL);
                uo->Count -= 1;
                uo->Launch ();
            }
            else
            {
                uo->Completed (res);
            }
        }
    };
};


//-----------------------------------------------------------------------------
//                  C o n t r o l O b j e c t   m e t h o d s
// ----------------------------------------------------------------------------
// (these are the one we could not define earlier, as they use classes not
// defined at the time ContolObject was being defined)
// ----------------------------------------------------------------------------


//  -------------
//  C o n n e c t
//  -------------


int ControlObject::Connect ()
//
// initiate a connection and hand control to the scheduler; 
// return non-zero if an error seems to have occured by the
// time control returns here.
//
{
    if (MyConnection != NULL)
    {
        return -1;
    }
    else
    {
        if (REALLYVERBOSE)
            fprintf (stderr, "ControlObject::Connect () called.\n");
        MyConnection = new Connection (this, ServerName);
        int res = MyConnection->ConnectRes;
        if (res != 0)
        {
            delete MyConnection;
            MyConnection = NULL;
        }
        return res;
    }
}

//  -------------------
//  D i s c o n n e c t
//  -------------------


int ControlObject::Disconnect ()
//
// close the previously-opened connection.
//
{
    int res = 0;
    if (MyConnection != NULL)
    {
        if (REALLYVERBOSE)
            fprintf (stderr, "ControlObject::Disconnect () called.\n");
        res = MyConnection->Disconnect();
        if (REALLYVERBOSE)
        {
            fprintf (stderr, "ControlObject::Disconnect () resumed.\n");
        }
        delete MyConnection;;
        MyConnection = NULL;
    }
    return res;
}


//  -------------------------
//  A l t e r D a t a b a s e
//  -------------------------


int ControlObject::AlterDatabase (const char* sql, int ct = 1, int hard = TRUE)
//
{
    if (MyConnection == NULL)
    {
        return -1;
    }
    UpdateObject* uo = new UpdateObject (this, sql, ct, hard);
    if (VERBOSE) fprintf (stderr, "\tabout to execute \"%s\".\n", sql);
    // hand control to the scheduler
    return Run ("Alter DB");
}


//  -------------
//  D o Q u e r y
//  -------------


int ControlObject::DoQuery (const char* sql, int* rowct = NULL)
//
{
    StaticQueryObject* sqo = new StaticQueryObject (this, sql);
    if (REALLYVERBOSE)
        fprintf (stderr, "about to execute \"%s\".\n", sql);
    // hand control to the scheduler
    int res = Run ("DoQuery");
    if (rowct != NULL) *rowct += sqo->RowCount;
    if (REALLYVERBOSE)
        printf ("(ControlObject::DoQuery () done, res=%d)\n", res);
    return res;
}


//  -----------------------
//  P r e p a r e Q u e r y
//  -----------------------


PreparedSQLObject* ControlObject::PrepareSQL (const char* sql, int argct, int batchct = 1)
//
{
    PreparedSQLObject* pso = new PreparedSQLObject (this, sql, argct, batchct);
    return pso;
}


//  -------------------------------
//  R u n P r e p a r e d Q u e r y
//  -------------------------------


int ControlObject::RunPreparedQuery (PreparedSQLObject* pso, int* argptr = NULL)
{
    return pso->PerformQuery (argptr);
}


//  ---------------------------------
//  R u n P r e p a r e d U p d a t e
//  ---------------------------------


int ControlObject::RunPreparedUpdate (PreparedSQLObject* pso, int* argptr = NULL, int* valueptr = NULL, double* doubleptr = NULL)
{
    return pso->PerformTransaction (argptr, valueptr, doubleptr);
}


//  -----------
//  T i d y U p
//  -----------


const void ControlObject::TidyUp ()
{
    // throw away chain of structures for completed one-shot operations
    Tracker* t = CompletedTrackers;
    Tracker* t2;
    while (t != NULL)
    {
        t2 = t; 
        t  = t->NextObject;
        delete t2;
    }
    CompletedTrackers = NULL;
}


//-----------------------------------------------------------------------------
//                   P e r f o r m a n c e T e s t
//-----------------------------------------------------------------------------
// measure the performance of Polyhedra on this system.
//-----------------------------------------------------------------------------


class PerformanceTest : public ControlObject
{

protected:
    
    int  Opcount;
    char Total[20];

public:

    PerformanceTest (const char* name, int opcount) : ControlObject (name)
    {
        Opcount = opcount;
    };    

    // ------------------------------------------------------------------------
    // create and drop the test tables.
    // ------------------------------------------------------------------------

    int create_test1_table ()
    {
        return create_table (CREATE_TABLE_TEST1_SQL, "test1");
    }

    int drop_test1_table ()
    {
        AlterDatabase ("delete from test1");
        // don't worry if the table cannot be deleted
        return AlterDatabase ("drop table test1", 1, FALSE);
    }

    int create_test2_table ()
    {
        return create_table (CREATE_TABLE_TEST2_SQL, "test2");
    }

    int drop_test2_table ()
    {
        AlterDatabase ("delete from test2");
        // don't worry if the table cannot be deleted
        return AlterDatabase ("drop table test2", 1, FALSE);
    }

    // ------------------------------------------------------------------------
    // test speed of inserts
    // ------------------------------------------------------------------------

    /* insert_records_via_command

        this function does <rowcount> commands, using parameterised
        SQL to insert records one at a time. The time taken to
        prepare the command is not included in the results.
        <batch> controls the batchsize; if not set to one,
        the procedure needs to call a Flush method at the end to ensure
        the last chunk of updates is performed (to protect against
        the case where (opct REM batch) is non-zero; Flush behaves OK
        if batch = 1 or (optct REM batch) = 0)

        <cleanup> flags whether the table should be
        emptied, or left populated ready for the next (stage of a) test.
        If it is set false, then progress messages are suppressed.

    */
    int insert_records_via_command ( int rowcount, int batch, int big,
                                     int cleanup, const char* testname
                                   )
    {
        int          i;
        int          size;
        int          id;
        int          ct      = 0;
        int          value   = 0;
        double       start;
        int          res;
        int          paramct = (big == SMALL) ? 5 : 50;
        const char*  table   = (big == SMALL) ? "test1" : "test2";
        const char*  sql     = (big == SMALL)
                               ? "insert into test1 values (?,?,?,?,?)"
                               : "insert into test2 values (?,?,?,?,?,?,?,?,?,?,"
                                                           "?,?,?,?,?,?,?,?,?,?,"
                                                           "?,?,?,?,?,?,?,?,?,?,"
                                                           "?,?,?,?,?,?,?,?,?,?,"
                                                           "?,?,?,?,?,?,?,?,?,?)";

        if (cleanup)
        {
            // report what this subtest is about to do, but not if the function
            // had been called to set up test data for another test.
            printf ( "\t%d prepared inserts (%d attributes)",  rowcount, paramct);
            if (batch > 2)
            {
                printf(" in batches of %d",batch);
            }
            printf("\n");
        }

        // make sure the table exists; as a side-effect, find out its size.

        if (big == SMALL)
            size = create_test1_table ();
        else
            size = create_test2_table ();

        if (cleanup && size > 0)
        {
            printf("\t(test table initially had %d records)\n", size);
        }

        PreparedSQLObject* pso = PrepareSQL (sql, paramct, batch);
        id    = size;
        start = the_tick ();

        for (i = 0; i < rowcount; i++)
        {
           id++;
           res = RunPreparedUpdate (pso, &id, &value); // automatically batched as needed
        }
        pso->Flush (); // flush the last batch, if needed

        if (cleanup)
        {
            double rate = HowFast (start, "insert", rowcount);
            if (testname != NULL)
            {
                Recorder->Record (testname, rate);
            }
            // the next line is a logic check that must be done AFTER
            // calling HowFast, otherwise it will affect the reported
            // speed!
            assert (size_of_table (table) == size + rowcount);
            if (big == SMALL)
                id = drop_test1_table ();
            else
                id = drop_test2_table ();
        }
        else
            // check we have created enough rows.
            assert (size_of_table (table) == size + rowcount);

        delete pso;

        // return the number of records now in the table
        // (or that would have been there, if it hadn't
        // been cleaned up).

        return id;
    }

    int populate_table (int rowcount, int big)
    {
        int ct = insert_records_via_command (rowcount, INSERTBATCHSIZE, big, LEAVE, NULL);
        if (REALLYVERBOSE)
            printf ("\t\tPopulate (%d, %s) returned %d\n", rowcount, big ? "big" : "small", ct);
        return ct;
    }

    /* ----------------------------------------*/

    /* insert_tests

        this function performs the insert-related timing tests. It opens
        the connection, runs a variety of individual tests, and then drops
        the connection. The database will be left empty, as each test
        will tidy up after itself.
    */
    int insert_tests (int rowcount)
    {
        int res;

        double dummy = 0;

        set_test("inserts",
                 "how fast can we insert records?"
                 "\n\thow much slower are inserts if there are many attributes?"
                 "\n\thow much does batching up the inserts improve performance?"
                 "\n\thow much does the size of the table affect insert speed?"
                );

        if ((res = Connect()) != 0) return res;

        // (individual record inserts)
        insert_records_via_command (rowcount,   1, SMALL, CLEANUP, "I5");

        // (individual record inserts, big records)
        insert_records_via_command (rowcount,   1, BIG,   CLEANUP, "I50");

        // (affect of batching)
        insert_records_via_command (rowcount, 100, SMALL, CLEANUP, "I5B");

        // (check insert into pre-populated table)
        populate_table (rowcount*10, SMALL);
        insert_records_via_command (rowcount,   1, SMALL, CLEANUP, "I5P");

        // (no need to drop test table here, each subtest does that for itself)
        Disconnect();
        return 0;
    }

    // ------------------------------------------------------------------------
    // test speed of queries
    // ------------------------------------------------------------------------

    /* do_batch_query

        this function does <querycount> queries, in batches of <batch>,
        using 'where id in (<list>)' to get the required rows.
        The logic assumes that <batch> <= <rowcount>

    */
    int do_batch_query ( int rowcount, int queryct, int big, int batch,
                        const char* testname
                      )
    {
        int          i;
        int          ct      = 0;
        int          value   = 1;
        double       start;
        int          res;
        int          paramct = (big == SMALL) ? 5 : 50;
        const char*  table   = (big == SMALL) ? "test1" : "test2";
        int          posn;
        char         buffer[BUFFERSIZE];
        int          bufflimit = BUFFERSIZE - 10;

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        printf ( "\t%d records (each with %d attributes) fetched, in batches of %d\n",
                 queryct, paramct, batch
               );

        start = the_tick ();
        posn  = 0;

        // build up the string (overwriting the closing bracket of the 'in' clause)
        // and execute it when we hit the batch limit or the string is getting too long.

        for (i = 0; i < queryct; i++)
        {
            if (posn==0)
                posn = sprintf (&buffer[0], "select * from %s where id in (%d)", table, value);
            else
                posn += sprintf (&buffer[posn-1], ",%d)", value) - 1;

            if ((i % batch == 0) || posn > bufflimit)
            {
                DoQuery (buffer, &ct);
                posn = 0;
            }
            value = (value % rowcount) + 1;
        }

        // read the last batch (in case rowcount not a multiple of batch size)

        if (batch > 1 && posn != 0)
        {
            DoQuery (buffer, &ct);
        }

        if (ct!=queryct)
        {
            printf("\tcurious... %d records returned in %d queries!\n", ct, queryct);
        }

        double rate = HowFast (start, "query", ct);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
        return 0;
    }

    /* do_prepared_test_query

        this function does <querycount> queries, using parameterised
        SQL to retrieve records one at a time. The time taken to
        prepare the query is not included in the results.
    */
    int do_prepared_test_query (int rowcount, int queryct, int big, const char* testname)
    {
        int    i;
        int    id        = 1;
        int    ct        = 0;
        double start;
        int    paramct   = (big == SMALL) ? 5 : 50;
        const char*  sql = (big == SMALL) ? "select * from test1 where id=?"
                                          : "select * from test2 where id=?";
        PreparedSQLObject* pso = PrepareSQL (sql, 1, 1);

        printf ( "\t%d prepared queries (%d attributes)\n",  queryct, paramct);

        start = the_tick ();

        for (i = 0; i < queryct; i++)
        {
           int res = RunPreparedQuery (pso, &id);
           //if (res != 1)
           //    printf ("\t\todd: '%s' returned nothing when id=%d\n", sql, id);
           ct += res;
           id = (id % rowcount) + 1;
        }

        if (ct!=queryct)
        {
            printf("\tcurious... %d records returned in %d queries!\n", ct, queryct);
        }

        double rate = HowFast (start, "query", ct);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }

        delete pso;
        return 0;
    }

    /* query_tests

        this function is called to perform the individual query performance
        tests. It first opens the tests, uses populate_table() to create some
        records, and then does some tests. The record count is then gradually
        increased and certain tests repeated to see how they are affected by
        table size. At the end, the table is emptied and dropped, and the
        connection closed.
    */
    int query_tests (int queryct)
    {
        int    tablesize = (queryct < 1000 ? queryct : 1000);
        int    ct1, ct2;

        set_test("Query",
                 "how fast can we retrieve individual records when we know the PK?"
                 "\n\thow is retrieval time affected by the number of attributes?"
                 "\n\thow is retrieval time affected by the size of table?");

        int res = Connect();
        if (res != 0) return res;

        ct1 = populate_table (tablesize, SMALL);
        ct2 = populate_table (tablesize, BIG);

        if (ct1==ct2)
            printf("  *\ttest tables each have %d records\n\n", ct1);
        else
        {
            printf("  *\ttest1 table has %d records\n",   ct1);
            printf("  *\ttest2 table has %d records\n\n", ct2);
        }

        do_prepared_test_query (tablesize, queryct, SMALL,     "Q5" );
        do_prepared_test_query (tablesize, queryct, BIG,       "Q50");
        do_batch_query         (tablesize, queryct, SMALL, 50, "Q5B");

        // now increase table size by a factor of 10

        ct1 = populate_table (tablesize*9, SMALL);

        printf("  *\ttest1 table has %d records\n\n", ct1);
        do_prepared_test_query (ct1, queryct, SMALL, "Q5P");

        // clean up
        drop_test1_table();
        drop_test2_table();
        Disconnect();
        return 0;
    }

    // ------------------------------------------------------------------------
    // update tests
    // ------------------------------------------------------------------------

    /* update_records_via_command

        this function does <opct> commands over the first
        <rowcount> records of the table , using parameterised
        SQL to insert records one at a time. The time taken to
        prepare the command is not included in the results.
        <batch> controls the batchsize; if not set to one,
        the procedure needs to call a Flush method to ensure
        the last chunk of updates is performed (to protect against
        the case where opct REM batch is non-zero; Flush behaves OK
        if batch = 1 or optct REM batch = 0)
    */
    int update_records_via_command ( int rowcount, int opct, int batch, int big,
                                     const char* testname
                                   )
    {
        int          i;
        int          id      = 0;
        int          ct      = 0;
        int          value   = 0;
        double       start;
        int          res;
        int          paramct = (big == SMALL) ? 5 : 50;
        const char*  table   = (big == SMALL) ? "test1" : "test2";
        int          size    = size_of_table (table);
        const char*  sql     = (big == SMALL) ?
                              "insert or update test1 values (?,?,?,?,?)"
                            : "insert or update test2 values (?,?,?,?,?,?,?,?,?,?,"
                                                             "?,?,?,?,?,?,?,?,?,?,"
                                                             "?,?,?,?,?,?,?,?,?,?,"
                                                             "?,?,?,?,?,?,?,?,?,?,"
                                                             "?,?,?,?,?,?,?,?,?,?)";

        static int call_count = 0; // Call 8414

        printf ( "\t%d prepared updates over %d records (%d attributes)",  opct, rowcount, paramct);
        if (batch > 2)
        {
            printf(" in batches of %d",batch);
        }
        printf("\n");

        PreparedSQLObject* pso = PrepareSQL (sql, paramct, batch);
        start = the_tick ();

        for (i = 1; i <= opct; i++)
        {
            id = (id % rowcount) + 1;
            call_count++;
            res = RunPreparedUpdate (pso, &id, &call_count);
        }
        pso->Flush ();

        double rate = HowFast (start, "update", opct);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
        // check we did not accidentally create any records
        assert (size_of_table (table) == size);
        delete pso;
        return 0;
    }

    int update_tests (int opct)
    {
        int        tablesize = (opct < 1000 ? opct : 1000);
        int        ct        = 0;
        double     dummy     = 0;

        set_test("Update",
                 "how fast can one update individual records?"
                 "\n\thow much slower if many attributes updated per record?"
                 "\n\thow much does batching the updates speeed things up?"
                 "\n\thow much does table size affect the update rate?"
                );

        int res = Connect();
        if (res != 0) return res;

        // populate the test tables

        ct = populate_table (tablesize, SMALL);
        ct = populate_table (tablesize, BIG);

        printf("  *\ttest tables have %d records\n\n", ct);

        update_records_via_command (ct, opct,   1, SMALL, "U5");
        update_records_via_command (ct, opct,   1, BIG,   "U50");
        update_records_via_command (ct, opct,  50, SMALL, "U5B");

        // repeat tests with a bigger table size

        ct = populate_table (tablesize*9, SMALL);

        printf("  *\ttest1 table has %d records\n\n", ct);

        update_records_via_command (ct, opct,   1, SMALL, "U5P");

        drop_test1_table();
        drop_test2_table();
        Disconnect ();
    return 0;
    }

    // ------------------------------------------------------------------------
    // delete tests
    // ------------------------------------------------------------------------

    /* delete_records_via_command

        this function create another <rowcount> records, and then
        uses parameterised SQL to them one at a time.
        The time taken to create the records and to
        prepare the command is not included in the results.

        <batch> controls the batchsize; if not set to one,
        the procedure needs to call a Flush method to ensure
        the last chunk of updates is performed (to protect against
        the case where opct REM batch is non-zero; Flush behaves OK
        if batch = 1 or optct REM batch = 0)
    */
    int delete_records_via_command ( int rowcount, int batch, int big,
                                     const char* testname
                                   )
    {
        int          i;
        int          size;
        int          id;
        double       start;
        int          res;
        double       dummy = 0;
        const char*  table = (big == SMALL) ? "test1" : "test2";
        /*
        const char*  sql   = (big == SMALL) ? "delete from test1 where id=:<integer>id"
                                            : "delete from test2 where id=:<integer>id";
                                            */
        const char*  sql   = (big == SMALL) ? "delete from test1 where id=?"
                                            : "delete from test2 where id=?";

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        printf ("\tdelete %d records (%d per transaction)\n", rowcount, batch);

        size = populate_table (rowcount, big);
        if (size>rowcount)
        {
            printf("\t(test table initially had %d records)\n", size-rowcount);
        }

        PreparedSQLObject* pso = PrepareSQL (sql, 1, batch);
        id    = size;
        start = the_tick ();

        for (i = 1; i <= rowcount; i++)
        {
            res = RunPreparedUpdate (pso, &id);
            id--;
        }
        pso->Flush ();

        double rate = HowFast (start, "delete", rowcount);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }

        // check we deleted the right number of records
        assert (size_of_table (table) == size-rowcount);

        delete pso;
        return 0;
    }

    int delete_tests (int rowcount)
    {
        int    ct;
        double dummy = 0;

        set_test("Delete",
                 "how fast can one delete individual records?"
                 "\n\thow much does batching improve the performance?"
                 "\n\thow much does table size affect the deletion rate?");

        int res = Connect();
        if (res != 0) return res;

        delete_records_via_command (rowcount,   1, SMALL, "D5");
        delete_records_via_command (rowcount,   1, BIG,   "D50");
        delete_records_via_command (rowcount,  50, SMALL, "D5B");

        // repeat tests with some records already there

        ct = populate_table (rowcount * 10, SMALL);
        delete_records_via_command (rowcount,   1, SMALL, "D5P");

        drop_test1_table();
        drop_test2_table();
        Disconnect ();
    return 0;
    }

    // ------------------------------------------------------------------------
    // redefine the virtual work function, 'Perform', that make use of all the 
    // base pseudo-synchronous functions and also the ones defined above
    // ------------------------------------------------------------------------

    virtual int Do_the_tests ()
    {
       int res = 0;
      if (res==0) res = insert_tests (Opcount);
      if (res==0) res = query_tests (Opcount);
      if (res==0) res = update_tests (Opcount);
      if (res==0) res = delete_tests (Opcount);
        return res;
    };

    int Perform ()
    {
    // first the tests that don't use Polyhedra, but simply try to calibrate
    // the machine / OS in use.

    raw_performance ();

    // now the real tests:

        double start = the_tick ();
    int res = Do_the_tests ();
        printf ("\nTests complete.\n\007\n");
        double rate  = HowFast (start, "", 0);

    // record overall time:

    sprintf (Total, "total/%d", Opcount);
    Recorder->Record (Total, rate);
        return res;
    };

};


//-----------------------------------------------------------------------------


#ifdef EXTRA
  #include "callxtra.hxx"
#endif


//-----------------------------------------------------------------------------
// the main work functions: 'test_callback' and either 'main' or 'perform'.
//-----------------------------------------------------------------------------


extern "C" int test_callback (const char* name, int opcount, int delaytime)
//
// connect to the named database server, run the various tests with the
// supplied operations count, then return zero or a failure indicator.
//
{
    int   res;

    DelayTime = delaytime;

    printf ( "Polyhedra performance tester:\n\n\tusing callback API"
         "\n\tserver:  %s\n\topcount: %d\n\n",
         name, opcount
       );

    // initialise the client api:
    if (res = AppAPI::Init ())
    {
        fprintf (stderr, "AppAPI::Init failed %d.\n", res);
        return 10;
    }

    Init_IO (); // (call platform-specific initialisation needed for ping test

    Recorder = new TestRecords ("callback");

    // create the main object that controls the demo; it creates
    // its own AppAPI object.

    ControlObject* test =
    #ifdef EXTRA
    new ExtraTests (name, opcount);
    #else
        new PerformanceTest (name, opcount);
    #endif
    
    // call the function that >actually< does the test.

    res = test->Perform();

    // control has been returned: tidy up and quit. The assumption is that
    // each test sequence has tied up after itself (closed active queries,
    // dropped connections, dropped timers, etc) so that nothing needs
    // doing other than telling the Polyhedra libraries to clean up any
    // houskeeping guff it may have lying around, and then deleting
    // all structures created by the C++ code in tis file and in common.hxx

    delete Recorder;
    delete test;
    AppAPI::Tidy ();
    End_IO ();
    return((res == 0) ? 0 : 10);
}


#ifdef EMBEDDED
#define NO_MAIN
#endif

#ifdef NO_MAIN
// on platforms where one is not allowed/expected to redefine main(),
// either perform() or test_callback() can be used; use the former
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
    // set up default values:

    const char* name    = Service;
    int         opcount = RowCount;
    int         delaytime = DelayTime;

    // check the right number of args given

    if (argc > 34)
    {
        fprintf(stderr, "usage: %s [<dsn>] [<opcount> [<delaytime>]]\n", argv[0]);
        exit(1);
    }

    // pick up the supplied args

    if (argc >= 2) name      = argv[1];
    if (argc >= 3) opcount   = atoi (argv[2]);
    if (argc >= 4) delaytime = atoi (argv[3]);

    // do the tests, then stop.

    return test_callback (name, opcount, delaytime);
}


/*---------------------------------------------------------------------------*/
/*                          e n d   o f   f i l e                            */
/*---------------------------------------------------------------------------*/

