//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2014 by Enea Software AB
//		All Rights Reserved
// Date:	$Date: 2014/01/06 14:48:59 $
// Revision:	$Id: persist.cxx,v 1.10 2014/01/06 14:48:59 andy Exp $
// Author:	Dave Stow
// Description:	
//------------------------------------------------------------------------------

//	
//	persist.cxx
//
//	Source code for the data persistence example
//	This takes a single parameter, being the maximum
//	size of the file. It launches an active query
//	on journalcontrol - whihc holds the size
//	of the load_file. When the load_file crosses the
//	the size boundary, then a "save into" is issued
//	to create a new snapshot of the data in memory.
//
//////////////////////////////////////////////////
//
//	v0.0	Dave Stow
//			First Version

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

#include <stdio.h>
#include <stdlib.h>

// Pick up all the client api headers... 
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

// Some useful constants
#define TRUE 1
#define FALSE 0

// JournalMon class is the class that holds the context of the 
// active query and a pointer to this is passed from callback
// to callback.
class JournalMon  
{
	ClientAPI*	Client;		// Pointer to the client instance
	QueryAPI*	Query;		// Pointer to the query instance
	TransAPI*	Trans;		// Pointer to the transaction instance
	long		MaxSize;	// Maximum size of the load_file
	long		SizeAtSave;	// Size of database at time of save
	const char *		Name;		// Name of the dataservice to connect to

public:
	AppAPI*		App;		// Pointer to the application instance

	JournalMon(int argc, char *argv[]) {
		if (argc == 2)
			Name = "8001";
		else
			Name = argv[2];

		MaxSize=atol(argv[1]);
		SizeAtSave = 0;		// Ok to carry out a save
	};

	~JournalMon () {};

	// User Function that makes connection, and the 
	// call back to say we are connected, and launches
	// the active query.
	static const int  Activate		(void *userdata);
	static const void CB_Connected	(void *userdata);
	static const void CB_Disconnect    (void *userdata);

	// Active Query Callbacks
	static const void CB_InsertUpdate	(void *userdata);
	static const void CB_Delete			(void *userdata);
	static const void CB_DeltaDone		(void *userdata);

	// Transaction complete callback
	static const void CB_TransDone	(void *userdata);

};


//	--------------------------
//	Active Query call-backs
//	--------------------------

const void JournalMon::CB_InsertUpdate (void *userdata)
//	Called when the journal control record is first seen,
//	or when it updates. Only the file_size could change, so
//	we ignore RowId and the ID column.
{
	long	FileSize = 0;		// Size of the load_file in bytes

	JournalMon	*context = (JournalMon *)userdata;
	int     res= QueryAPI::GetError(context->Query);
	
	if (res == POLY_OK)
	{
		if (QueryAPI::CopyColumn (context->Query,
								"file_size",
								&FileSize,
								4) ==0) {
			printf("no FileSize??\n");
			FileSize=0;
		}

		// SizeAtSave used to prevent false 'save into's issued
		// as filesize fluctuates during save into operation.
		if (FileSize < context->SizeAtSave) {
			// Okay to issue a 'save into'
			context->SizeAtSave = 0;
		}

		if (FileSize > context->MaxSize && context->SizeAtSave == 0) {
			// The maximum allowable filesize has been
			// transgressed. Issue a save into.

			printf("File size has reached %ld, so time to create new load_file.\n",
							FileSize);

			context->SizeAtSave = FileSize;

			context->Trans = TransAPI::StartTrans (
								context->Client,
								"save into 'test.dat'",
								JournalMon::CB_TransDone, 
								context);
		}

    }
	else
    {
		Poly_Print_Error(res,"call to insert/update callback");
    }
}

const void JournalMon::CB_Delete (void *userdata)
//	Called if the journal control record has been removed.
//	This is terminal - and would indicate some major problem,
//	so we elect to ditch out immediately if this happened.
{
	JournalMon	*context= (JournalMon *)userdata;
	int     res= QueryAPI::GetError(context->Query);
	
	if (res == POLY_OK)
	{
		fprintf(stderr,"Journal control record removed!\n");
		AppAPI::Stop(context->App);
    }
	else
    {
		Poly_Print_Error(res,"call to delete callback");
    }
}


const void JournalMon::CB_DeltaDone(void *userdata)

//	This delta is now complete.

{
	JournalMon *context= (JournalMon*) userdata;
	int res= QueryAPI::GetError(context->Query); 

	if (res != POLY_OK) {
		Poly_Print_Error(res,"call to delta complete");

		// If the query did not execute, maybe a database other than
		// the currency database has been started up?
		if (res == POLY_EQUERY) printf("Wrong database started up?\n");

		// Active query has failed - stop the program
		AppAPI::Stop(context->App);
    }
}

//	--------------------------------------
//	Save Into transaction has completed
//	--------------------------------------

const void JournalMon::CB_TransDone(void *userdata)
//	Called once the save into transaction has been competed
{
	JournalMon *context= (JournalMon*) userdata;
	int res= QueryAPI::GetError(context->Query); 

	if (res != POLY_OK) {
		Poly_Print_Error(res,"save into completion");
		AppAPI::Stop(context->App);
	}
	else {
		printf("Save into completed.\n");
	}

}


//	--------------------------------------
//	Activation and conncetion callbacks
//	--------------------------------------

const void JournalMon::CB_Connected(void *userdata)

//     Called once a connection to the database has been established (or if the
//     attempt to set it up failed.
//    
//     Check the error code and if all is ok, get on to the next part of the job.
//     in this case, all we need to do is launch the query, telling it which
//     functions are to be called back later.

{ 
	JournalMon *context= (JournalMon *) userdata; 
	int res = ClientAPI::GetError (context->Client);
  
	if (res != POLY_OK)
    {
      Poly_Print_Error(res,"connect to database");

	  // If there was no connection made, perhaps the database isn't
	  // started, or isn't started correctly.
	  if (res == POLY_ECONNECT) printf("Is the database started correctly?\n");

	  // Connect failed. Stop the program
      AppAPI::Stop (context->App);	
    }
	else
    {	
		printf("Connected, now launch active query on journal control\n");
		printf("and monitor file_size for it reaching %ld\n",context->MaxSize);

 
		// Launch active query, returning size of load file
		// Note that as we only have one record we are using the same
		// function for both the insert and update callbacks
		context->Query = 
			QueryAPI::StartActiveQuery (
					context->Client, 
					"select id,file_size from journalcontrol",
					JournalMon::CB_InsertUpdate, 
					JournalMon::CB_InsertUpdate, 
					JournalMon::CB_Delete, 
					JournalMon::CB_DeltaDone, 
					context,
					1);
    }
}

const void JournalMon::CB_Disconnect(void *userdata)
  //
  // called once a connection to the database has been broken
  //
{
  JournalMon *context = (JournalMon *) userdata;

  // Various tidying up must occur in this callback:
  // Abort all outstanding active queries.
  QueryAPI::StartAbort(context->Query,NULL, NULL);

  // Client will exit when no more callbacks registered.
}


const int JournalMon::Activate (void *userdata)
//	called by the client API scheduler once it has been granted control.
//
//	The argument is cast back to an Active pointer, and a connection
//	request is set up.
{
	JournalMon *context= (JournalMon *)userdata;
  
	printf ("Connecting to database at %s...\n",context->Name);
	
	// Initiate connection to our database
	context->Client = ClientAPI::StartConnect (
						context->App,
						context->Name,
						JournalMon::CB_Connected,
						context,
						JournalMon::CB_Disconnect,
						context);
 
	return FALSE; // Scheduler should not call this function again
}


//  -------
//	Main
//  -------

#if defined(EMBEDDED)
extern "C" int poly_main(int argc, char* argv [])
#else
int main (int argc, char* argv [])
#endif
// main. Initialise the API and start the scheduler
{
	int res;
	JournalMon *context;		/* Structure to hold application context */
  
  
	if (argc < 2) {
		fprintf (stderr, 
	       "Usage: %s <max size of load_file> [data service]\n",argv[0]);
		fprintf (stderr,
			"data service defaults to 8001\n");
		return 10;
	}

	// initialise the client api
	if (res = AppAPI::Init()) {
		Poly_Print_Error(res,"initialising the api");
		return 10;
	}  

	// create the monitoring structure:
	context = new JournalMon(argc,argv);

	// create an AppAPI object to give context to the scheduler
	context->App = AppAPI::Create();

	printf("Start the journal control monitoring process.\n");

	// pass control to the client API, telling it the first function
	// to call.
	AppAPI::Start(context->App, JournalMon::Activate, context);

	printf("Returned from scheduler. Finished.\n");

	// control has been returned: tidy up and quit.

	AppAPI::Delete(context->App);
	delete context;
	AppAPI::Tidy();

	return 0;
}
