//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2015 by Enea Software AB
//		All Rights Reserved
// Author:	Dave Stow
// Description:	
//------------------------------------------------------------------------------

//	
//	active.cxx
//
//	Source code for Active Query example client
//	Launch an active query on the database and display
//	the changing data.
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
#include <string.h>

// Pick up all the client api headers... 
#include <appapi.h>
#include <timerapi.h>
#include <clntapi.h>
#include <queryapi.h>

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

// Maximum number of currencies we want to deal with
#define MAX_CURRENCIES 100

// Active class is the class that holds the context of the 
// active query and a pointer to this is passed from callback
// to callback.
class Active  
{
	ClientAPI*	Client;		// Pointer to the client instance
	QueryAPI*	Query;		// Pointer to the query instance
	const char*		Name;		// Name of the database to connect to
	int		FT;		// Fault Tolerant connection

	// An array to hold the map between the Row Ids, and the
	// currency codes which are the primary keys. In a real
	// application this would be a linked list unless the number
	// of rows was known beforehand.
	struct {
		long RowId;
		char code[10];
	} Rows[MAX_CURRENCIES];

	int NumRows;	// Number of rows actually in this array

public:
	AppAPI*		App;		// Pointer to the application instance

	// Constructor and destructor do nothing
	Active(int argc, char *argv[]) {

		// Use parameters to set data service to connect
		// to and fault tolerant mode.
		switch (argc) {

		case 2: {
			Name = argv[1];
			FT = FALSE;
			break;
				}

		case 3: {
			Name = argv[1];
			if (strcmp(argv[2],"FT") == 0)
				FT = TRUE;
			else
				FT = FALSE;

			break;
				}

		case 1:
		default: {
			Name = "8001";
			FT = FALSE;
			break;
				}

		}

		NumRows = 0;
	};
	~Active () {};

	// User Function that makes connection, and the 
	// call back to say we are connected, and launches
	// the active query.
	static const int  Activate	(void *userdata);
	static const void CB_Connected	(void *userdata);
	static const void CB_Disconnect (void *userdata);

	// Active Query Callbacks
	static const void CB_Insert	(void *userdata);
	static const void CB_Update	(void *userdata);
	static const void CB_Delete	(void *userdata);
	static const void CB_DeltaDone	(void *userdata);

	// Method to find the element in the array which is
	// maps onto the given Row Id.
	int FindRow			(long RowId);
};


//	--------------------------
//	Active Query call-backs
//	--------------------------

const void Active::CB_Insert (void *userdata)
//	Called when a row is added to the result set.
{

	double	usd;		// US Dollar value

	Active	*context = (Active *)userdata;
	int     res= QueryAPI::GetError(context->Query);
	
	if (res == 0)
	{
		context->Rows[context->NumRows].RowId = QueryAPI::GetRowId(context->Query);

		if (QueryAPI::CopyColumn (context->Query,
								"code",
								context->Rows[context->NumRows].code,
								4) ==0) {
			printf("no currency code?\n");
			context->Rows[context->NumRows].code[0] = '\0';
		}

		if (QueryAPI::CopyColumn (context->Query,
								"usdollar",
								&usd,
								sizeof(double)) ==0) {
			printf("no currency value?\n");
			usd=0;
		}

		printf("Row Added - Code: %s, 1 Dollar buys: %lf.\n",
					context->Rows[context->NumRows].code,usd);

		context->NumRows++;

    }
	else
    {
		Poly_Print_Error(res,"call to insert callback");
    }
}

const void Active::CB_Update (void *userdata)
/*
	Called when a row in the result set changes
*/
{
	long	RowId;			// Row Id of row that has changed
	int	Elem;			// Element of the array that matches this Row Id
	char	tmp_code[4];		// Temp store for new code (if any)
	double	usd;			// New US Dollar value (if any)

	Active *context= (Active *)userdata;
	int res = QueryAPI::GetError(context->Query);

	if (res == 0)
	{
		RowId = QueryAPI::GetRowId(context->Query);		// Get the Row Id of this row
		Elem = context->FindRow(RowId);					// Get the Element in the array

		if (QueryAPI::CopyColumn(context->Query, "code", tmp_code,4) > 0) 
		{
		    // either the Currency code has been changed - unlikely, but 
		    // we'd better handle it - or the database has been set up
		    // (by means of the query_delta_pk resource, say) to transmit
		    // the PK attributes in all active query deltas.
		    if (strcmp (context->Rows[Elem].code, tmp_code) != 0)
		    {
			printf("Currency code changed from %.4s to %.4s.\n",
			       context->Rows[Elem].code,
			       tmp_code);
			strncpy(context->Rows[Elem].code,tmp_code,4);
		    }
		}

		if (QueryAPI::CopyColumn(context->Query, "usdollar", &usd, sizeof(double)) >0) {
			// US Dollar value has changed. Display an appropriate message
			printf("Code: %s, 1 US Dollar now buys %lf.\n",
						context->Rows[Elem].code,
						usd);
		}
	}
	else {
		Poly_Print_Error(res,"call to update callback");
    }
}

const void Active::CB_Delete (void *userdata)

//	Called when a row is removed from the result set.

{
	long	RowId;		// Row that has been deleted
	int	Elem;		// Element of the array that need to be deleted

	Active	*context= (Active *)userdata;
	int     res= QueryAPI::GetError(context->Query);
	
	if (res == 0)
	{
		RowId = QueryAPI::GetRowId(context->Query);
		Elem = context->FindRow(RowId);

		printf("Currency %s removed from resultset\n",
			   context->Rows[Elem].code);

		context->NumRows--;		// Reduce the number of rows by one

		// Shuffle the array down over this removed row
		for (;Elem<context->NumRows;Elem++) {
			context->Rows[Elem].RowId = context->Rows[Elem+1].RowId;
			strncpy(context->Rows[Elem].code,context->Rows[Elem+1].code,4);
		}
    }
	else
    {
		Poly_Print_Error(res,"call to delete callback");
    }
}


const void Active::CB_DeltaDone(void *userdata)

//	This delta is now complete.

{
	Active *context= (Active*) userdata;
	int res= QueryAPI::GetError(context->Query); 

	if (res == 0)
    {
		printf ("Delta complete - success.\n\n");

		// Debug info prints out array mapping row id to primary key
//		for(int n=0;n<context->NumRows;n++)
//			printf("Element: %d, RowId: %ld, Code: %s\n",
//						n,context->Rows[n].RowId,context->Rows[n].code);

    }
	else
    {
		Poly_Print_Error(res,"call to delta complete");

		// If the query did not execute, maybe a database other than
		// the currency database has been started up?
		if (res == POLY_EQUERY) printf("Wrong database started up?\n");

		// Active query has failed - stop the program
		AppAPI::Stop(context->App);
    }
}


//	--------------------------------------
//	Activation and conncetion callbacks
//	--------------------------------------

const void Active::CB_Connected(void *userdata)

//     Called once a connection to the database has been established (or if the
//     attempt to set it up failed.
//    
//     Check the error code and if all is ok, get on to the next part of the job.
//     in this case, all we need to do is launch the query, telling it which
//     functions are to be called back later.

{ 
	Active *context= (Active *) userdata; 
	int res = ClientAPI::GetError (context->Client);
  
	if (res != 0)
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
		fprintf (stderr, "Connected, now launch active query...\n");
 
		// Launch active query, returning currency code and us dollar value
		context->Query = 
			QueryAPI::StartActiveQuery (
					context->Client, 
					"select code,usdollar from currency",
					Active::CB_Insert, 
					Active::CB_Update, 
					Active::CB_Delete, 
					Active::CB_DeltaDone, 
					context,
					MAX_CURRENCIES);
    }
}

const void Active::CB_Disconnect(void *userdata)
  //
  // called once a connection to the database has been broken
  //
{
  Active *context = (Active *) userdata;
  fprintf(stderr,"Connection to database lost; stopping the client application.\n");

  // Various tidying up must occur in this callback:
  // Abort all outstanding active queries.
  QueryAPI::StartAbort(context->Query,NULL, NULL);
}


const int Active::Activate (void *userdata)
//	called by the client API scheduler once it has been granted control.
//
//	The argument is cast back to an Active pointer, and a connection
//	request is set up.
{
	Active *context= (Active *)userdata;
 
	if (context->FT)
		fprintf(stderr,"Connecting to %s Fault Tolerant...\n",context->Name);
	else
		fprintf(stderr, "Connecting to %s...\n",context->Name);

	context->Client = ClientAPI::StartConnect (
						context->App,
						context->Name,
						Active::CB_Connected,
						context,
						Active::CB_Disconnect,
						context);
  
	// Fault tolerant connection - set the right options. No other
	// changes required.
	if (context->FT) {
		// The order is important. POLY_FT_OPTION_ENABLE
		// must be set first
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_ENABLE,TRUE);

		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_HEALTHCHECK_INTERVAL,1000);
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_HEALTHCHECK_TIMEOUT,1000);
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_RECONNECTION_INTERVAL,1000);
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_RECONNECTION_TIMEOUT,1000);
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_RECONNECTION_RETRIES,1000);
		ClientAPI::SetOption(context->Client,POLY_FT_OPTION_MAP_ROWIDS,TRUE);
	}
 
	return FALSE; // Scheduler should not call this function again
}


// Find Row method
int Active::FindRow(long RowId)
//	Find the element in the array that holds the
//	Row Id.
{
	int n;
	int Result;

	for(n=0;n<NumRows;n++)
		if (Rows[n].RowId == RowId) {
			Result=n;
			n=NumRows;
		}

	return Result;

}

//  -------
//	Main
//  -------

#if defined(EMBEDDED)
extern "C" int poly_main(int argc, char* argv [])
#else
int main(int argc, char* argv [])
#endif
// main. Initialise the API and start the scheduler
{
  int res;
  Active *context;		/* Structure to hold application context */
  
  // initialise the client api
  if (res = AppAPI::Init())
    {
	  Poly_Print_Error(res,"initialising the api");
      return 10;
    }  

  // create the monitoring structure:
  context = new Active(argc,argv);

  // create an AppAPI object to give context to the scheduler
  context->App = AppAPI::Create();

  // pass control to the client API, telling it the first function
  // to call.
  AppAPI::Start(context->App, Active::Activate, context);

  // control has been returned: tidy up and quit.

  AppAPI::Delete(context->App);
  delete context;
  AppAPI::Tidy();

  return 0;
}
