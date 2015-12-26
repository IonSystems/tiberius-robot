/*-+-----------------------------------------------------------------------+-//
//									     //
//             P O L Y H E D R A    T E S T    L I B R A R Y		     //
//									     //
//                Copyright (C) 1999-2014 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------//
//
//-+ Filename    : perform.cxx
//-+ Description : Client API timer tests.
//			
//-+ CVSID       : $Id: perform.cxx,v 1.14 2014/01/06 14:48:59 andy Exp $
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


const char *Poly_Errors_Name[25] = {
"POLY_OK",
"POLY_EALREADYINIT",
"POLY_ENOINIT",
"POLY_ENOSTART",
"POLY_ECONNECT",
"POLY_ECOLUMNNAME",
"POLY_ECOLUMNNO",
"POLY_ENOVALUE",
"POLY_ENULLVALUE",
"POLY_EQUERY",
"POLY_ESTARTTRANS",
"POLY_ECOMMIT",
"POLY_EDELTA",
"POLY_ETRUNCATED",
"POLY_EINUSE",
"POLY_ENOMEMORY",
"POLY_ENOINFO",
"POLY_ESHUTDOWN",
"POLY_ELOGIN",
"POLY_EQUERYINUSE",
"POLY_EWRONGCLIENT",
"POLY_ETRANSINUSE",
"POLY_ENOQUERY",
"POLY_ENOTINCOMMIT",
"POLY_ENOCHANGE"};

const char *Poly_Errors_Msg[25] = {
"No error.",
"The scheduler has already been initialised.",
"The scheduler has not been initialised.",
"The scheduler has not been started-up.",
"Failed to connect to database.",
"Invalid column name.",
"Invalid column number.",
"A column value has not changed.",
"A column value is null.",
"An SQL query has failed to execute.",
"A transaction has failed to start.",
"A transaction has failed to commit.",
"The delta for an active query has failed.",
"The data requested for a column has been truncated.",
"A client connection is in use and cannot be deleted.",
"No memory for static data segment.",
"Information requested for a query before it has returned.",
"Failed to shutdown a server.",
"Attempt to log onto server failed.",
"TransAPI::StartTrans has already been called",
"Attempt to add a query to a transaction on a different client",
"TransAPI::StartTrans has already been called",
"No queries have been added to the transaction using TransAPIAddQuery",
"TransAPI::Commit has not been called",
"A column value has not changed."};

// Poly_Print_Error prototype
void Poly_Print_Error(int err,const char *location);

// Poly_Print_Error implementation. I guess this could just be
// a macro!
void Poly_Print_Error(int err,const char *location)
// Print out Polyhedra error messages
{
	fprintf(stderr,"Error in %s. Code %d (%s)\n%s\n",
		location,err,Poly_Errors_Name[err],Poly_Errors_Msg[err]);
}

// define some useful constants

#define VERBOSITY     0
#define REALLYVERBOSE (VERBOSITY >= 2)
#define VERBOSE       (VERBOSITY >= 1)

#define BGTIMEOUT     10*3600

#if defined(INTEGRITY)
#define Connection CaConnection
#endif

// -----------------------------------------------------------------------------
//                       C o n t r o l O b j e c t
// -----------------------------------------------------------------------------
// define a class to keep track of what is happening: we will have just
// one of these. It defines the various (static) functions that the 
// client api will be calling to signal that it has done its work. 
// -----------------------------------------------------------------------------



// first declare our classes (to allow mutual references)


class ControlObject;          // we will have just one of these objects

class ControlledObject;       // (abstract class)
class Connection;             // handles connections
class Tracker;                // (abstract class for one-shots)
class ActiveQueryObject;      // handles active queries
class StaticQueryObject;      // handles static queries
class UpdateObject;           // handles SQL transactions


class ControlObject
{
    TransAPI*           Trans;
    TimerAPI*           MyTimer;
    TimerAPI*           MyBGTimer;

protected:

    friend class        ControlledObject;
    friend class        Tracker;
    friend class        ActiveQueryObject;

    AppAPI*             App;
    ActiveQueryObject*  ActiveQueryChain;
    int                 ActiveQueryPendingCt;
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
        ActiveQueryChain     = NULL;
        ActiveQueryPendingCt = 0;
        MyTimer              = NULL;
        MyBGTimer            = NULL;
        CompletedTrackers    = NULL;
        InScheduler          = FALSE;

        // create an AppAPI object to hold context for the scheduler
        App                  = AppAPI::Create ();
        CreateBackgroundTimer ();
    };

    ~ControlObject ()
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
                fprintf (stderr, "ControlObject::Run (NULL) done, res = %d.\n", Res);
            else
                fprintf (stderr, "ControlObject::Run (\"%s\") done, res = %d.\n", operation, Res);
        }
        return Res;
    };


    static const int DoSomething (void *userdata)
    {
        // called by the client API scheduler once it has been granted control.
        //
        // Given the way the demo has been coded, we will not have to do
        // anything here; everything necessary for the next stage of the demo
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

    // initiate a connection

    int  Connect ();                    

    // close a connection

    int Disconnect ();                    

    // block deltas from active queries

    int  BlockDeltas (int inscheduler); 
    static const void StartTransCallBack (void *userdata);

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
    }
    ;

    // called when ready to accept deltas
    int  CatchDeltas ();          
    static const void DeleteTransCallBack (void *userdata);

    // do something to the database
    int AlterDatabase (const char* sql, int ct = 1);

    // do a query on the database
    int DoQuery (const char* sql, int ct = 1, int* rowct = NULL);

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
        int res = ClientAPI::GetError (c->Client);
	c->ConnectRes = res;

        if (res != 0)
        {
            fprintf (stderr, "connect failed %d.\n", res);
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
        if (StopWhenDone == TRUE) Owner->Done (res);
    };
};


// ----------------------------------------------------------------------------
//                    A c t i v e Q u e r y O b j e c t
// ----------------------------------------------------------------------------
// next, a class to track the multiple active queries that will be launched,
// so that we will know which ones to block. 
// ----------------------------------------------------------------------------


class ActiveQueryObject : public ControlledObject
{
public:
    char*              Name;
    QueryAPI*          Query;
    int                DeltaReceived;
    int                RowCount;
    ActiveQueryObject* NextQuery;

    ActiveQueryObject ( ControlObject* owner, 
                        char* name, 
                        char* sql, 
                        int delaytime
                      )
    : ControlledObject (owner)
    {
        Name                          = name;
        RowCount                      = 0;
        DeltaReceived                 = FALSE;

        // chain together the active queries for a connection:
        Owner->ActiveQueryPendingCt  += 1;
        NextQuery                     = Owner->ActiveQueryChain;
        Owner->ActiveQueryChain       = this;

        // launch query (but don't fire off the scheduler):

        Query = QueryAPI::StartActiveQuery 
                ( GetClient(), 
                  sql,
                  ActiveQueryObject::RowCallBack,
                  ActiveQueryObject::RowCallBack,
                  ActiveQueryObject::RowCallBack,
                  ActiveQueryObject::DeltaDoneCallBack, 
                  this,
                  POLY_MAX_ROWS_UNLIMITED, 
                  0, // sleep
                  delaytime  // delay
                );
    }

    static const void RowCallBack (void *userdata)
    {
        // at present, called once for each row inserted, deleted or updated.

        ActiveQueryObject* qo  = (ActiveQueryObject*) userdata;
        int                res = QueryAPI::GetError(qo->Query);

        //printf ("ActiveQueryObject::RowCallBack called\n", n);

        if (res == 0)
        {
            qo->RowCount++;
        }
        else
        {
            fprintf ( stderr, 
                      "problem in query CallBack %d for query %s.\n", 
                      res, qo->Name
                    );
            qo->Done (res);
        }
    }
    static const void DeltaDoneCallBack (void *userdata)
    {
        // batch of changes complete.

        ActiveQueryObject* qo  = (ActiveQueryObject*) userdata;
        int                res = QueryAPI::GetError(qo->Query);

        if (res == 0)
        {
            printf ("%d rows inserted/updated/deleted on query '%s'.\n",
                    qo->RowCount, qo->Name
                   );
            qo->RowCount = 0;

            if (!qo->DeltaReceived)
            {
                // this is the first delta to be received for this query;
                // flag it as having been received, and decrement the 
                // number of pending initial deltas.

                qo->DeltaReceived                = TRUE;
                qo->Owner->ActiveQueryPendingCt -= 1;
                if (qo->Owner->ActiveQueryPendingCt == 0)
                {
                    if (VERBOSE)
                        fprintf (stderr, "all initial deltas received.\n");
                    qo->Done (0);
                }
                else
                {
                    if (VERBOSE)
                        fprintf (stderr, "(%d queries outstanding.)\n", 
                                 qo->Owner->ActiveQueryPendingCt);
                }
            }
        }
        else
        {
            fprintf (stderr, "SQL query failed %d.\n", res);
            qo->Done (res);
        }
    }
};


//-----------------------------------------------------------------------------
//                          S t a t i c Q u e r y O b j e c t
// -----------------------------------------------------------------------------
// class to launch a static query when created; control is returned when the
// query is complete (or, if count > 1, when the operation has been done the 
// indicated number of times).
// -----------------------------------------------------------------------------


class StaticQueryObject : protected Tracker
{
    QueryAPI* Query;
    const char*     SQL;   // the operation to perform
    int       Count; // how many times to do the operation

protected:
    friend class ControlObject;

public:

    int       RowCount;

    StaticQueryObject (ControlObject* owner, const char* sql, int ct = 1, int stop = TRUE) 
    : Tracker (owner, stop)
    {
        SQL      = sql;
        Count    = ct;
        RowCount = 0;
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

    static const void Row (void *userData)
    {
        StaticQueryObject* sqo = (StaticQueryObject*) userData;
        sqo->RowCount ++;
    }

    static const void QueryDone (void *userdata)
    {
        StaticQueryObject* sqo = (StaticQueryObject*) userdata;
        int res = QueryAPI::GetError(sqo->Query);
        sqo->Count--;
        if (sqo->Count <= 0 || res != 0)
            sqo->Completed (res);
        else
            sqo->LaunchQuery ();
    }
};


// ----------------------------------------------------------------------------
//                        U p d a t e O b j e c t
// ----------------------------------------------------------------------------
// a class to perform updates to the database a designated number of times,
// optionally quitting out of the scdeduler when the work is done.
//
// a repeat count of zero will be taken to mean that it is to be 
// attempted once, but no error message is to be generated if
// it fails.
// ----------------------------------------------------------------------------


class UpdateObject : protected Tracker
{
    TransAPI*      Trans;
    const char*          SQL;   // the operation to perform
    int            Count; // how many times to do the operation

public:

    UpdateObject (ControlObject* owner, const char* sql, int ct = 1, int stop = TRUE) 
    : Tracker (owner, stop)
    {
        SQL   = sql;
        Count = ct;
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
            if (uo->Count > 0 || REALLYVERBOSE)
            {
                fprintf ( stderr,
                          "transaction \"%s\" failed %d:\n\t%s\n", 
                          uo->SQL, res, buf
                        );
            }
            uo->Completed (res);
        }
        else
        {
            if (VERBOSE) fprintf (stderr, "%s\n", uo->SQL);
            if (uo->Count > 1)
            {
                //fprintf (stderr, "repeating transaction \"%s\".\n", uo->SQL);
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


//  -----------------------------------------------------
//  B l o c k D e l t a s
//
//  Code to block deltas until we explicitly release them
//  -----------------------------------------------------


int ControlObject::BlockDeltas (int inscheduler)
//
// set off a 'transaction' to block deltas on all my active queries
//
{
    const char*              separator = "block deltas on queries";
    ActiveQueryObject *qo        = ActiveQueryChain;

    if (qo == NULL)
    {
        if (VERBOSE) fprintf (stderr, "BlockDeltas: no active queries to block!\n");
        return 32767;
    }

    // create a local transaction object...
    Trans = TransAPI::CreateTrans (MyConnection->Client);

    // register the active queries as part of the transaction...
    while (qo != NULL)
    {
        if (inscheduler == FALSE && VERBOSE)
            fprintf (stderr, "%s '%s'", separator, qo->Name);
        separator = ",";
        TransAPI::AddQuery (Trans, qo->Query);
        qo = qo->NextQuery;
    }
    if (inscheduler == FALSE && VERBOSE) fprintf (stderr, "\n");

    // now 'start the transaction' - this just asks the server to
    // block all active queries associated with the transaction
    // object.
    // this requires client-server interaction, and in theory
    // any pending deltas should be sent up so that by the time
    // the start transaction is acked (and the callback triggered)
    // the client will be as up to date as possible.

    TransAPI::StartTrans ( Trans, 
                           ControlObject::StartTransCallBack, 
                           this
                         );

    if (inscheduler == FALSE)
    {
        // hand control to the scheduler
        return Run ("block deltas");
    }
    else
        return Res;
}


const void ControlObject::StartTransCallBack (void *userdata)
//
// called by the client API scheduler once the work involved with
// StartTrans has been done: the relevant queries have been blocked
// by this time.
//
{
    ControlObject *test = (ControlObject *)userdata;

    if (VERBOSE) fprintf (stderr, "Deltas blocked.\n");

    test->Done (0);
}


//  ---------------------
//  C a t c h D e l t a s
//  ---------------------


int ControlObject::CatchDeltas ()
//
// catch the deltas for the blocked active queries, leaving 
// the queries blocked.
//
{

    if (VERBOSE) fprintf (stderr, "Catch deltas...\n");
    if (Trans == NULL)
    {
        return 0;
    }
    TransAPI::DeleteTrans ( Trans, 
                            ControlObject::DeleteTransCallBack, 
                            this
                          );

    // hand control to the scheduler, which will hand it back
    // (all things being OK) when the next tranasction has
    // been established.

    return Run ("Returning from CatchDeltas");
}


const void ControlObject::DeleteTransCallBack (void *userdata)
//
// transaction deleted (by which time, any deltas should have
// been received. Block deltas again.
//
{
    ControlObject* test = (ControlObject*) userdata;
    if (VERBOSE) fprintf (stderr, "Transaction deleted.\n");
    test->Trans = NULL;
    test->BlockDeltas (TRUE);
}


//  -------------------------
//  A l t e r D a t a b a s e
//  -------------------------


int ControlObject::AlterDatabase (const char* sql, int ct)
//
{
    if (MyConnection == NULL)
    {
        return -1;
    }
    UpdateObject* uo = new UpdateObject (this, sql, ct);
    if (VERBOSE) fprintf (stderr, "about to execute \"%s\".\n", sql);
    // hand control to the scheduler
    return Run ("Alteration done");
}


//  -------------
//  D o Q u e r y
//  -------------


int ControlObject::DoQuery (const char* sql, int ct, int* rowct)
//
{
    StaticQueryObject* sqo = new StaticQueryObject (this, sql, ct);
    if (VERBOSE) fprintf (stderr, "about to execute \"%s\".\n", sql);
    // hand control to the scheduler
    int res = Run ("Query done");
    if (rowct != NULL) *rowct += sqo->RowCount;
    return res;
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


#define INSERT_INTO_TEST1_PARAM_SQL    \
    "insert into test1"                \
    "(id,col2,col3,col4,col5)"         \
    "values(%d,2.0,3.0,0,0)"


#define INSERT_INTO_TEST2_PARAM_SQL    \
    "insert into test2"                \
    "(id,   col2, col3, col4, col5"    \
    ",col6, col7, col8, col9, col10"   \
    ",col11,col12,col13,col14,col15"   \
    ",col16,col17,col18,col19,col20"   \
    ",col21,col22,col23,col24,col25"   \
    ",col26,col27,col28,col29,col30"   \
    ",col31,col32,col33,col34,col35"   \
    ",col36,col37,col38,col39,col40"   \
    ",col41,col42,col43,col44,col45"   \
    ",col46,col47,col48,col49,col50"   \
    ")values"                          \
    "(%d,2.0,3.0,0,0,0,0,0,0,0"        \
    ",0,0,0,0,0,0,0,0,0,0"             \
    ",0,0,0,0,0,0,0,0,0,0"             \
    ",0,0,0,0,0,0,0,0,0,0"             \
    ",0,0,0,0,0,0,0,0,0,0"             \
    ")"


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
    // general-purpose functions.
    // ------------------------------------------------------------------------

    int create_test1_table ()
    {
        int res;
        int rowct = 0;
        if (MyConnection == NULL)
            if ((res = Connect ()) != 0) return res;
        res = AlterDatabase (CREATE_TABLE_TEST1_SQL, 0);
        if (res != 0)
        {
            // table probably exists - how big is it?
            res = DoQuery ("select id from test1", 0, &rowct);
        }
        return rowct;
    }

    int drop_test1_table ()
    {
        AlterDatabase ("delete from test1");
        return AlterDatabase ("drop table test1");
    }

    int create_test2_table ()
    {
        int res;
        int rowct = 0;
        if (MyConnection == NULL)
            if ((res = Connect ()) != 0) return res;
        res = AlterDatabase (CREATE_TABLE_TEST2_SQL, 0);
        if (res != 0)
        {
            // table probably exists - how big is it?
            res = DoQuery ("select id from test2", 0, &rowct);
        }
        return rowct;
    }

    int drop_test2_table ()
    {
        AlterDatabase ("delete from test2");
        return AlterDatabase ("drop table test2");
    }

    // ------------------------------------------------------------------------
    // test speed of inserts
    // ------------------------------------------------------------------------

    int insert_records ( int rowcount, int batch, int big, 
                         int cleanup, const char* testname = NULL
                       )
    {
        int    i;
        int    id    = 0;
        double start;
        char   buffer[BUFFERSIZE];
        int    posn;
        int    paramct = (big==TRUE ? 50 : 5);
        char*  sql     = (char*) ( big == FALSE
                                   ? (INSERT_INTO_TEST1_PARAM_SQL)
                                   : (INSERT_INTO_TEST2_PARAM_SQL)
                                 );
        int    bufflimit = BUFFERSIZE - strlen(sql) - 6;

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        if (cleanup)
        {
            // report what this subtest is about to do, but not if the function
            // had been called to set up test data for another test.

            printf ( "\tinsert %d records" 
                     " (%d per transaction, %d attributes each)\n", 
                     rowcount, batch, paramct
                   );
        }

	if (big == FALSE)
	    id = create_test1_table( );
	else
	    id = create_test2_table ();

        if (cleanup && id > 0)
        {
            printf("\t(test table initially had %d records)\n", id);
        }
        start = the_tick ();
        posn  = 0;

        for (i = 1; i <= rowcount; i++)
        {
            ++id;
            if (posn > 0)
            {
                buffer[posn] = ';';
                posn        += 1;
                if (REALLYVERBOSE) fprintf (stderr, "%d ", posn);
            }
            posn += sprintf (&buffer[posn], sql, id);
            if ((batch <2) || (i % batch == 0) || posn > bufflimit)
            {
                if (REALLYVERBOSE && batch > 1)
                    fprintf (stderr, " - %d.\n%s\n", i, buffer);
                AlterDatabase (buffer);
                posn = 0;
            }
        }

        if (posn > 0)
        {
            AlterDatabase (buffer);
        }

        if (cleanup)
        {
            double rate = HowFast (start, "insert", rowcount);
            if (testname != NULL)
            {
                Recorder->Record (testname, rate);
            }
	    if (big == FALSE)
		id = drop_test1_table ();
	    else
		id = drop_test2_table ();

        }

        // return the number of records now in the table
        // (or that would have been there, if it hadn't
        // been cleaned up).

        return id;
    }

    int       Batch;
    int       Big;
    int       Rowcount;
    int       Id;
    int       ParamCt;
    TransAPI* InsertTrans;

    int async_insert_records ( int rowcount, int batch, int big, 
                               int cleanup, const char* testname = NULL
                             )
    {
        int    id    = 0;
        double start;
        int    paramct = (big==TRUE ? 50 : 5);

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        if (cleanup)
        {
            // report what this subtest is about to do, but not if the function
            // had been called to set up test data for another test.

            printf ( "\tinsert %d records asynchronously" 
                     " (%d per transaction, %d attributes each)\n", 
                     rowcount, batch, paramct
                   );
        }

	if (big == FALSE)
	    id = create_test1_table( );
	else
	    id = create_test2_table ();

        if (cleanup && id > 0)
        {
            printf("\t(test table initially had %d records)\n", id);
        }
        start = the_tick ();

        Batch    = batch;
        Big      = big;
        RowCount = rowcount;
        ParamCt  = paramct;
        Id       = id;

        AppAPI::Start (App, PerformanceTest::AsyncInsertFn, this);

        if (cleanup)
        {
            double rate = HowFast (start, "insert", rowcount);
            if (testname != NULL)
            {
                Recorder->Record (testname, rate);
            }
            if (big == FALSE)
		drop_test1_table ();
	    else
		drop_test2_table ();
        }

        // return the number of records now in the table
        // (or that would have been there, if it hadn't
        // been cleaned up).

        return Id;
    }


    static const int AsyncInsertFn (void *userdata)
    {
        PerformanceTest * pt = (PerformanceTest*) userdata;
        pt->DoSomeInserts();
        return FALSE;
    }

    static const void AsyncInsertCallback (void *userdata)
    {
        PerformanceTest * pt = (PerformanceTest*) userdata;
        
        if (RowCount <= 0)
            AppAPI::Stop (pt->App);
        else
            pt->DoSomeInserts();
    }

    void DoSomeInserts ()
    {
        int    i;
        char   buffer[BUFFERSIZE];
        int    posn = 0;
        char*  sql  = (char*) ( Big == FALSE 
                                ? (INSERT_INTO_TEST1_PARAM_SQL)
                                : (INSERT_INTO_TEST2_PARAM_SQL)
                              );
        int    bufflimit = BUFFERSIZE - strlen(sql) - 6;

        if (Batch > RowCount)
            Batch = RowCount;
        RowCount -= Batch;

        //fprintf (stderr, "%d -> %d.\n", Id+1, Id+Batch);

        for (i=1; i<=Batch; i++)
        {
            ++Id;
            if (posn > 0)
            {
                buffer[posn] = ';';
                posn        += 1;
            }
            posn += sprintf (&buffer[posn], sql, Id);
            if (posn > bufflimit) break;
        }
        InsertTrans = 
            TransAPI::StartTrans (MyConnection->Client,
                                  buffer,
                                  PerformanceTest::AsyncInsertCallback, 
                                  this
                                  );
    }

    /* ----------------------------------------*/

    /* insert_individually

       insert a number of records, one per transaction;
       report on the time taken and clear up afterwards.
    */
    void insert_individually (int rowcount, const char* testname)
    {
        insert_records (rowcount, 1, FALSE, TRUE, testname);
    }

    /* insert_tests

        this function performs the insert-related timing tests. It opens
        the connection, calls insert_records or insert_individually to 
        perform the individual tests,and then drops the connection. At
        the end of the tests, the database will be left empty.
    */
    int insert_tests (int rowcount)
    {
        int res;

        set_test("inserts",
                 "how fast can we insert records?"
                 "\n\thow much slower are inserts if there are many attributes?"
                 "\n\thow much does batching up the inserts improve performance?"
                 "\n\thow much does the size of the table affect insert speed?"
                );

        if ((res = Connect()) != 0) return res;

        // (individual record inserts)
        insert_individually (rowcount, "I5 ");

        // (individual record inserts, big records)
        insert_records (rowcount, 1, TRUE, TRUE, "I50");

        // (affect of batching)
        insert_records (rowcount, 100, FALSE, TRUE, "I5B");
#ifdef EXTRA
        insert_records (rowcount,  50, TRUE,  TRUE);
#endif

        // (check insert into pre-populated table)
        insert_records (rowcount*10, 100, FALSE, FALSE, NULL);
        insert_individually (rowcount, "I5P");

        // (try asych insert)
        async_insert_records (rowcount, 1, FALSE, TRUE, "I5A");

        // (no need to drop test table here, each subtest does that for itself)
        Disconnect();
	return 0;
    }

    // ------------------------------------------------------------------------
    // test speed of queries
    // ------------------------------------------------------------------------

    /* do_test_query

        this function does <querycount> queries, using the supplied SQL in 
        each case. If useparam is non-zero, it is treated as a batch count,
	and a where id in (...)' clause is added to the sql (or a
	'where id=...' if the batch count is 1). 
    */
    int do_test_query ( int rowcount, int queryct, int big, 
                           int useparam, const char* testname
                         )
    {
        int    i;
        int    ct      = 0;
        int    value   = 1;
        double start;
	int    res;
        int    paramct = (big==TRUE ? 50 : 5);
        char*  sql     = (char*) (big == FALSE 
                                  ? "select * from test1"
                                  : "select * from test2"
                                 );
	int    posn;
        char   buffer[BUFFERSIZE];
	int    bufflimit = BUFFERSIZE - 10;
	int    batch = useparam > MAXBATCHSIZE ? MAXBATCHSIZE : useparam ;

        printf ( "\t%d %s queries (%d attributes)\n", 
                 queryct, 
		 (batch>1 ? "batched" : 
	                    (useparam==0 ?  "table" : "individual record")),
		 paramct
               );

        start = the_tick ();
	posn  = 0;

        for (i = 0; i < queryct; i++)
        {
	    if (useparam==0) 
	    {
		sprintf (&buffer[0], sql);
		if ((res = DoQuery (buffer, 1, &ct)) != 0) return res;
	    }
	    else if (batch==1)
	    {
		sprintf (&buffer[0], "%s where id=%d", sql, value);
		if ((res = DoQuery (buffer, 1, &ct)) != 0) return res;
	    }
            else 
	    {
		if (posn==0)
		    posn = sprintf (&buffer[0], "%s where id in (%d)", sql, value);
		else
		    posn += sprintf (&buffer[posn-1], ",%d)", value) - 1;

		if ((i % batch == 0) || posn > bufflimit)
		{
		    if ((res = DoQuery (buffer, 1, &ct)) != 0) return res;
		    posn = 0;
		 }
	    }
	    value = (value % rowcount) + 1;
        }

	// read the last batch (in case rowcount not a multiple of batch size)

	if (batch > 1 && posn != 0) 
	{
	    if ((res = DoQuery (buffer, 1, &ct)) != 0) return res;
	}

        if (ct>queryct)
        {
            printf("\t%d records returned per query.\n", ct / queryct);
        }
        double rate = HowFast (start, "query", ct);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
        return 0;
    }
    
    int query5 (int rowcount, int queryct, const char* testname)
    {
        return do_test_query ( rowcount, queryct, FALSE, 
                               1, testname
                             );
    }


    int query50 (int rowcount, int queryct, const char* testname)
    {
        return do_test_query ( rowcount, queryct, TRUE,
                               1, testname
                             );
    }


    int query_all (int rowcount, int queryct, const char* testname)
    {
        return do_test_query ( rowcount, queryct, FALSE, 
                               0, testname
                             );
    }


    int batched_query (int rowcount, int queryct, const char* testname)
    {
        return do_test_query ( rowcount, queryct, FALSE, 
                               50, testname
                             );
    }

    /* query_tests

        this function is called to perform the individual query performance
        tests. It first opens the tests, uses insert_records to create some
        records, and then does some tests. The record count is then gradually
        increased and certain tests repeated to see how they are affected by
        table size. At the end, the table is emptied and dropped, and the
        connection closed.
    */
    int query_tests (int rowcount)
    {
        int        tablesize = (rowcount < 1000 ? rowcount : 1000);
        int        ct;

       set_test("Query",
                 "how fast can we retrieve individual records when we know the PK?"
                 "\n\thow is retrieval time affected by the number of attributes?"
                 "\n\thow is retrieval time affected by the size of table?");

       int res = Connect();
       if (res != 0) return res;

        ct = insert_records (tablesize,  INSERTBATCHSIZE, FALSE, FALSE);
        ct = insert_records (tablesize,  INSERTBATCHSIZE, TRUE,  FALSE);

        printf("  *\ttest tables have %d records\n\n", ct);
        query5    (ct, rowcount,     "Q5 " );
        query50   (ct, rowcount,     "Q50");
        //query_all (ct, rowcount/100, "Q5A" );
	batched_query (ct, rowcount, "Q5B");

        // now another factor of 10

        ct = insert_records (ct*9,  INSERTBATCHSIZE, FALSE, FALSE);

        printf("  *\ttest1 table has %d records\n\n", ct);
        query5    (ct, rowcount,     "Q5P");

        drop_test1_table();
        drop_test2_table();
        Disconnect();
        return 0;
    }

    // ------------------------------------------------------------------------
    // update tests
    // ------------------------------------------------------------------------

    void update_records ( int rowcount, int opct, int batch, int big, 
                          const char* testname = NULL
			  );
    // implementation is after class definition because of static

    int update_tests (int rowcount)
    {
        int        tablesize = (rowcount < 1000 ? rowcount : 1000);
        int        ct = 0;

        set_test("Update",
                 "how fast can one update individual records?"
                 "\n\thow much slower if many attributes updated per record?"
                 "\n\thow much does batching the updates speeed things up?"
                 "\n\thow much does table size affect the update rate?"
                );

        int res = Connect();
        if (res != 0) return res;

        // populate the test tables

        ct = insert_records (tablesize,  INSERTBATCHSIZE, FALSE, FALSE);
        ct = insert_records (tablesize,  INSERTBATCHSIZE, TRUE, FALSE);

        printf("  *\ttest tables have %d records\n\n", ct);

        update_records (ct, rowcount,   1, FALSE, "U5 " );
        update_records (ct, rowcount,   1, TRUE,  "U50");
        update_records (ct, rowcount,  50, FALSE, "U5B");

        // repeat tests with a bigger table size

        ct = insert_records (tablesize*9,  INSERTBATCHSIZE, FALSE, FALSE);

        printf("  *\ttest1 table has %d records\n\n", ct);

        update_records (ct, rowcount,   1, FALSE, "U5P");

        drop_test1_table();
        drop_test2_table();
        Disconnect ();
	return 0;
    }

    // ------------------------------------------------------------------------
    // delete tests
    // ------------------------------------------------------------------------


    void delete_records ( int rowcount, int batch, 
                          const char* testname = NULL
                        )
    {
        int    i;
        int    id;
        double start;
        char   buffer[BUFFERSIZE];
        int    posn;
        int    bufflimit = BUFFERSIZE - 10;

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        printf ("\tdelete %d records (%d per transaction)\n", rowcount, batch);

        id = insert_records (rowcount, INSERTBATCHSIZE, FALSE, FALSE);
        if (id>rowcount)
        {
            printf("\t(test1 table initially had %d records)\n", id-rowcount);
        }

        start = the_tick ();
        posn  = 0;

        for (i = 1; i <= rowcount; i++)
        {
            if (batch < 2)
            {
                sprintf (&buffer[posn], "delete from test1 where id=%d", id);
                AlterDatabase (buffer);
            }
            else
            {
                if (posn == 0)
                {
                    posn = sprintf (&buffer[0], 
                                     "delete from test1 where id in (%d)", id);
                }
                else
                {
                    posn --;
                    posn += sprintf (&buffer[posn], ",%d)", id);
                }
                if ((i % batch == 0) || posn > bufflimit)
                {
                    if (REALLYVERBOSE)
                        fprintf (stderr, "%s\n", buffer);
                    AlterDatabase (buffer);
                    posn = 0;
                }
            }
            --id;
        }

        if (posn > 0)
        {
            AlterDatabase (buffer);
        }

        double rate = HowFast (start, "delete", rowcount);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
    }


    int delete_tests (int rowcount)
    {
        int        ct;

        set_test("Delete",
                 "how fast can one delete individual records?"
                 "\n\thow much does batching improve the performance?"
                 "\n\thow much does table size affect the deletion rate?");

        int res = Connect();
        if (res != 0) return res;

        delete_records (rowcount,   1, "D5 ");
        delete_records (rowcount,  50, "D5B");

        // repeat tests with some records already there
        ct = insert_records (rowcount * 10,  INSERTBATCHSIZE, FALSE, FALSE);
        delete_records (rowcount,   1, "D5P");

        drop_test1_table();
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

void PerformanceTest::update_records ( int rowcount, int opct, int batch, int big, 
				       const char* testname
				       )
{
        int    i, j;
        int    id;
        double start;
        char   buffer[BUFFERSIZE];
        int    posn;
        int    paramct = (big==FALSE ? 5 : 50);
        int    bufflimit = BUFFERSIZE - (30+11*paramct);
	const char* table = (big==FALSE ? "test1" : "test2");
	static int call_count = 0; // Call 8414
	call_count++;

        if (batch > MAXBATCHSIZE)
            batch = MAXBATCHSIZE;

        printf ( "\tupdate %d records" 
                 " (%d per transaction, %d attributes each)\n", 
                 rowcount, batch, paramct
               );

        start = the_tick ();
        posn  = 0;
        id    = 0;

        for (i = 1; i <= opct; i++)
        {
            id = (id % rowcount) + 1;
            if (posn > 0)
            {
                buffer[posn] = ';';
                posn        += 1;
                if (REALLYVERBOSE) fprintf (stderr, "%d ", posn);
            }
            posn += sprintf (&buffer[posn], "update %s set col2=%d", table, call_count);
            for (j=3; j<=paramct; j++)
            {
                posn += sprintf (&buffer[posn], ",col%d=%d", j, call_count);
            }
            posn += sprintf (&buffer[posn], " where id=%d", id);
            if ((batch <2) || (i % batch == 0) || posn > bufflimit)
            {
                if (REALLYVERBOSE && batch > 1)
                    fprintf (stderr, " - %d.\n%s\n", i, buffer);
                AlterDatabase (buffer);
                posn = 0;
            }
        }

        if (posn > 0)
        {
            AlterDatabase (buffer);
        }

        double rate = HowFast (start, "update", opct);
        if (testname != NULL)
        {
            Recorder->Record (testname, rate);
        }
}

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

