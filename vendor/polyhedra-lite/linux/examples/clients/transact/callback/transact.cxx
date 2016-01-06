//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2015 by Enea Software AB
//		All Rights Reserved
// Author:	Dave Stow, Nigel Day
// Description:	
//------------------------------------------------------------------------------

//
//	POLYHEDRA DEMO SUITE
//
//	transaction
//
//	This program illustrates the use of simple transactions.
//	It connects to the database and then fires off a piece of SQL,
//	as specified by the program argument. 
//
//	The supplied value can be a single SQL DDL statement
//	(eg, create table, create schema, drop table), OR one or more SQL DML
//	statements (insert, delete or update) separated by semicolons, but should
//	not include any select statement. 
//
//////////////////////////////////////////////////////
//	
//	v0.0 -	Dave Stow/Nigel Day
//			First Version
//

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

#include <stdio.h>

// first, pick up all the client api headers...

#include <appapi.h>
#include <timerapi.h>
#include <clntapi.h>
#include <transapi.h>

// define some constants to make the code more readable...
#define FALSE 0
#define TRUE  1

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


// now, define a class to keep track of what is happening: we will have
// just one of these. It defines the various (static) functions that the 
// client api will be calling to signal that it has done its work. 
class Transact
{
	ClientAPI* 	Client;		// Client instance
	TransAPI*	Trans;		// Transaction instance
	char*		SQL;		// SQL string
	const char*		Name;		// Data service to connect to

public:
	AppAPI*	App;

	Transact(int argc, char *argv[])
	{
		if (argc == 2) 
			Name = "8001";
		else
			Name = argv[2];

		SQL    = argv[1];
		Client = NULL;
	};

	~Transact () {};
	void Stop();

	static const int  Activate		(void *userdata);
	static const void CB_Connect	(void *userdata);
	static const void CB_TransDone	(void *userdata);
	static const void CB_DeleteDone	(void *userdata);


};


const void Transact::CB_Connect(void *userdata)
// called once a connection to the database has been established (or if the
// attempt to set it up failed.
//
// check the error code and if all is ok, get on to the next part of the job.
//
// in this case, all we need to do is launch the transaction, telling it
// which function is to be called back later.
{
	Transact *context = (Transact *) userdata;
	int res = ClientAPI::GetError (context->Client);
  
	if (res != 0) {
		Poly_Print_Error(res,"connection to database");

		// Make tentative guess at the problem...
		if (res == POLY_ECONNECT) fprintf(stderr,"Is the database started correctly?\n");

		// Failure. Stop the program.
		AppAPI::Stop (context->App);
	}
	else {
		// Connected, now do some sql...

		printf("Connected successfully. Start the transaction:\n%s\n",context->SQL);

		context->Trans = TransAPI::StartTrans (
								context->Client,
								context->SQL,
								Transact::CB_TransDone, 
								context);
    }
}


const void Transact::CB_TransDone(void *userdata)
// all done - check for error, and quit.
{   
  Transact *context = (Transact *)userdata;
  char       buf[256];
  int        res   = TransAPI::GetError(context->Trans, buf, 255);
  
	if (res == 0) {
		printf("Transaction completed successfully.\n");
	}
	else {
		Poly_Print_Error(res,"transaction done callback");
	}
	context->Stop ();
}

void Transact::Stop()
//	called to disconnect the client

{
	if (Client)
		ClientAPI::DeleteClient(Client, 
					Transact::CB_DeleteDone, 
					this);
	else
		Transact::CB_DeleteDone(this);
}

const void Transact::CB_DeleteDone(void *userdata)
//	This callback is called when the client has been deleted.
//	As this is the end of this example the AppAPI::Stop
//	method is called.

{
	Transact *context = (Transact*) userdata;
	AppAPI::Stop(context->App);
} 



const int Transact::Activate (void *userdata)
//
// Called by the client API scheduler once it has been granted control.
//
// Initiates a connection to the data_service port 8000 on the
// local host. The ConnectCallBack function will be called when
//	the connection has been established.

{
  Transact *context = (Transact *)userdata;

  printf("Connecting to port %s...\n",context->Name);

  context->Client = ClientAPI::StartConnect (
						context->App,
						context->Name,
						Transact::CB_Connect,
						context);
  
  return FALSE; // that is, don't call me again! 
}


#if defined(EMBEDDED)
extern "C" int poly_main(int argc, char* argv [])
#else
extern "C" int main (int argc, char* argv [])
#endif

{
	int res;
  
	if (argc < 2) {
		fprintf (stderr, 
	       "Usage: %s <SQL statement> [data service]\n",argv[0]);
		fprintf (stderr,"data service will default to 8001.\n");
		return 10;
	}

	// initialise the client api:
	if (res = AppAPI::Init()) {
		Poly_Print_Error(res,"initialising the API");
		return 10;
	}  

	// create the monitoring object:
	Transact* context = new Transact(argc, argv);

	// create an AppAPI object to give context to the scheduler
	context->App = AppAPI::Create();

	// pass control to the client API, telling it the first function to call.
	AppAPI::Start(context->App, Transact::Activate, context);

	// control has been returned: tidy up and quit.
	AppAPI::Delete(context->App);
	delete context;
	AppAPI::Tidy();

	return 0;
}

