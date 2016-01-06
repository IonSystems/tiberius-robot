//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2015 by Enea Software AB
//		All Rights Reserved
// Author:	Dave Stow
// Description:	
//------------------------------------------------------------------------------

/*
//	Animate.cxx
//
//	Code to animate the currency exchange rate
//	table in a saw-tooth walk.
//
//	Initial values are read in as the zero line 
//	around which the walk takes place. The
//	limits of the walk are 5% of either side of 
//	the zero line.
//
//	Note that this code uses Updates through
//	Active Query to keep track of what currencies
//	are in the table, and also to change them
//
////////////////////////////////////
//
//	v1.0  - Dave Stow - August 2000
//			First Version

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

*/

#include <stdio.h>
#include <string.h>

// first, pick up all the client api headers...

#include <appapi.h>
#include <timerapi.h>
#include <clntapi.h>
#include <queryapi.h>
#include <transapi.h>

// define some constants to make the code more readable...

#define FALSE 0
#define TRUE  1

#define MAX_CURRENCIES 100 // Maximum number of currencies we can handle
#define LIMIT           10 // percentage limit on sawtooth walk
#define UPDATE_PERIOD   20 // number of deciseconds between updates



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

class CurrRow
{

public:
	long RowId;			// Active Query Row ID for this currency
	char code[10];		// Currency code	
	double usdollar;	// Current US Dollar value
	double zeroline;	// Initial US Dollar value
	double change;		// Current delta direction in the walk

	// Constructor - does nothing
	CurrRow() {};

	// Destructor - does nothing
	~CurrRow() {};

	void Init();
};

class Animate
{
	// Structures to hold instances of client, 
	// transactions, queries and timer
	ClientAPI* 	Client;
	TransAPI*	Trans;
	QueryAPI*	Query;
	TimerAPI*	Timer;

	// Class to hold values used in the 'random' walk.
	// Note that to keep the client simple, they
	// are all held here in the client, in an array.

	CurrRow walk_vals[MAX_CURRENCIES];

	int     Num_Rows;    // Actual number of rows of currency codes
	int     InitialSet;  // Was this the initial result set for the aquery

	const char *  Name;        // Name of the database to connect to
	int     FT;          // Fault toleranct connection

	// Public members
    public:
	AppAPI* App;         // Application instance structure

	// Constructor - set initial values
	Animate  (int argc, char *argv[])
	{
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
		Client			= NULL;
		Trans			= NULL;
		Query			= NULL;
		Num_Rows		= 0;
		InitialSet		= TRUE;
	};

	// Destructor - does nothing
	~Animate () {};

	// Functions in this class
	// First User function Activate makes a connection to
	// the database, and CB_Connect is called when the connection
	// is made.
	static const int  Activate         (void *userdata);
	static const void CB_Connect       (void *userdata);
	static const void CB_Disconnect    (void *userdata);
	static const void CB_ModeChange    (void *userdata);

	// These are the callbacks for the Active Query
	static const void CB_Insert        (void *userdata);
	static const void CB_Update        (void *userdata);
	static const void CB_Delete        (void *userdata);
	static const void CB_DeltaDone     (void *userdata);

	// DoWalk starts the transaction in which one step of the
	// 'ransom' walk takes place. CB_CalculateStep works out
	// the new set of currency values, and CD_TransDone is 
	// called when the transaction is done, deletes the
	// transaction and the callback for this starts a new
	// timer off.
	static const void DoWalk           (void *userdata);
	static const void CB_CalculateStep (QueryAPI *Qry,void *userdata);
	static const void CB_TransDone     (void *userdata);
	static const void CB_TransDeleted  (void *userdata);
};


void CurrRow::Init()
{
	// Initialise this currency entry based on
	// its US dollar value - reset the zero line and
	// and calculate initial change
	double StepLimit;
	StepLimit = LIMIT/1000.0;

	zeroline=usdollar;
	change = zeroline*StepLimit;

}


// ---------------------
// Connection call-backs
// ---------------------


const void Animate::CB_Connect(void *userdata)
  //
  // called once a connection to the database has been established (or if the
  // attempt to set it up failed.
  //
  // check the error code and if all is ok, get on to the next part of the job.
  //
  // in this case, all we need to do is launch the transaction, telling it
  // which function is to be called back later.
{
  Animate *context = (Animate *) userdata;
  int res = ClientAPI::GetError (context->Client);
  
  if (res != 0)
    {
      Poly_Print_Error(res,"connection");
      AppAPI::Stop (context->App);
    }
  else
    {
	  fprintf(stderr,"Connection made successfully.\n");
	  CB_ModeChange(context);

	  // Connected, get the initial values for the 
	  // 'random' walk into the walk_vals array.

	  context->Query = QueryAPI::StartActiveQuery(
						context->Client,
						"Select code,usdollar from currency",
						Animate::CB_Insert,
						Animate::CB_Update,
						Animate::CB_Delete,
						Animate::CB_DeltaDone,
						context,
						MAX_CURRENCIES);
    }

}

const void Animate::CB_Disconnect(void *userdata)
  //
  // called once a connection to the database has been broken
  //
{
  Animate *context = (Animate *) userdata;
  fprintf(stderr,"Connection to database lost; stopping the client application.\n");

  // Various tidying up must occur in this callback:
  // Abort all outstanding active queries.
  QueryAPI::StartAbort(context->Query,NULL, NULL);

  // Stop all outstanding timers.
  if(context->Timer) TimerAPI::StopTimer(context->Timer);

  // Finally stop the scheduler.
  AppAPI::Stop (context->App);
}

const void Animate::CB_ModeChange(void *userdata)
  //
  // called whenever the database to which we are connected changes state.
  //
{
  Animate *context = (Animate *) userdata;
  int mode = ClientAPI::GetFTMode (context->Client);
  char buffer[100];
  ClientAPI::GetServiceName(context->Client, buffer, 100);
  fprintf(stderr,"\n\07database %s is in mode %d.\n\n", buffer, mode);
}


// ---------------
// query callbacks
// ---------------


// Row received from query call back

const void Animate::CB_Insert(void *userdata)

{
	Animate *context = (Animate *)userdata;
	int res = QueryAPI::GetError(context->Query);
	double StepLimit;		// 1/10 of limit percentage for calculating initial step

	StepLimit=LIMIT/1000.0;

	if (res == 0) {						// Did this row arrive OK - almost always OK

		// Get the Server Row ID for this row
		context->walk_vals[context->Num_Rows].RowId = QueryAPI::GetRowId(context->Query);

		// Get the Currency Code
		if (QueryAPI::CopyColumn(
					context->Query,
					"code",
					context->walk_vals[context->Num_Rows].code,
					4) == 0 ) {
			fprintf(stderr,"Copy of CODE column failed.\n");
		}

		// Get the USDollar column
		if (QueryAPI::CopyColumn(
					context->Query,
					"usdollar",
					&context->walk_vals[context->Num_Rows].usdollar,
					sizeof(double)) == 0 ) {
			fprintf(stderr,"Copy of USDOLLAR column failed.\n");
		}

		context->walk_vals[context->Num_Rows].Init();

		fprintf(stderr,"Row %d - Code: %s, 1 US Dollar = %lf. Initial change will be %lf.\n",
					context->Num_Rows,
					context->walk_vals[context->Num_Rows].code,
					context->walk_vals[context->Num_Rows].zeroline,
					context->walk_vals[context->Num_Rows].change);

		// Finally - increment the number of rows.
		context->Num_Rows++;
	}
	else {
		Poly_Print_Error(res,"row returned callback");
	}

}

const void Animate::CB_Update(void *userdata)
// Row in currency table updated.
// Not sure why this would happen, as we are updating via the
// active query. As such, if it was the usdollar column, then 
// we'll take it as a reset of the zero line.
{
	Animate *context = (Animate *)userdata;
	int res = QueryAPI::GetError(context->Query);
	int Row;
	double new_zeroline;
	int Elem;
	double StepLimit;

	StepLimit=LIMIT/1000.0;

	if (res == 0) {
		Row = QueryAPI::GetRowId(context->Query);

		if (QueryAPI::CopyColumn(context->Query,
						"usdollar",
						&new_zeroline,
						sizeof(double)) > 0 ) {
			// The us dollar column was changed, so make it the new zeroline
			for (Elem = 0;Elem < context->Num_Rows; Elem++)		// Search the array for the matching row id.
				if (context->walk_vals[Elem].RowId == Row) {		// Got it - initialise the array
						context->walk_vals[Elem].usdollar = new_zeroline;
						context->walk_vals[Elem].Init();
				}
		}

	}
	else {
		Poly_Print_Error(res,"update callback");
	}

}

const void Animate::CB_Delete(void *userdata)
// Row in currency table deleted
// User has chosen to remove one of the currencies. 
// We'll update our array here to reflect this, and as
// its an array and this is a simple application we'll
// just shuffle everything else up. 
{
	Animate *context = (Animate *)userdata;
	int res = QueryAPI::GetError(context->Query);
	int Elem;
	int Shuffle = FALSE;
	int Row;

	if (res == 0) {
		Row = QueryAPI::GetRowId(context->Query);
		for(Elem=0;Elem<context->Num_Rows;Elem++) {
			if (context->walk_vals[Elem].RowId == Row) {
				Shuffle = TRUE;
			}

			if (Shuffle) {		// Take the next element of walk array up and copy if over me
				memcpy(&(context->walk_vals[Elem]),&(context->walk_vals[Elem+1]),sizeof(CurrRow));
			}
		}
		context->Num_Rows--;
	}
	else {
		Poly_Print_Error(res,"Delete callback");
	}

}



const void Animate::CB_DeltaDone(void *userdata)
//
//	Query has completed. Using the data in the query, 
//	begin the animation process.
//

{
	Animate *context = (Animate *)userdata;
	int res = QueryAPI::GetError(context->Query);

	if (res != 0) {
		Poly_Print_Error(res,"delta complete");
		if (context->InitialSet) {
			// No point in carrying on if the initial
			// set of values has failed.
			AppAPI::Stop(context->App);
		}
	}
	else {
		fprintf(stderr,"Delta Complete\n");

		if (context->InitialSet) {
			// This was the end of the initial result set
			// Flag as such, and start off the timer to get
			// the 'random' walk going
			context->InitialSet = FALSE;
			fprintf(stderr,"Initiate animation of currency data.\n");
			context->Timer = TimerAPI::CreateOneShotTimer(context->App,
												UPDATE_PERIOD,
												Animate::DoWalk,
												context);
		}
	}
}


// Timer call back - animate the data.
const void Animate::DoWalk(void *userdata)
//
//	Walk the data - update each row in turn with a new value
//	based on a sawtooth walk, with the original value as the zeroline
//	and with the limits being zero line +/- <LIMITS>%.
//	This function starts a transaction on the active query and
//	that calls the function which actually creates the new value and
//	updates the rows.
// 
{
	Animate *context = (Animate *)userdata;
	int res;
	int res2;

	fprintf(stderr,"Start update through active query\n");

	// The triggering timer is now invalid.
	context->Timer = NULL;

	// Create new Transaction instance
	context->Trans=TransAPI::CreateTrans(context->Client);

	// Associate the query with the new transaction
	if(res = TransAPI::AddQuery(context->Trans,context->Query)) {
		fprintf(stderr,"Error in AddQuery: %d.\n",res);
	}

	// Commit the transaction through the query, calling
	// CB_CalculateStep to work out the new values
	if (res = TransAPI::Commit(context->Trans,
							Animate::CB_CalculateStep,
							Animate::CB_TransDone,
							context,
							FALSE)) {
	        res2=TransAPI::GetError(context->Trans);
		if (res2==POLY_ENOQUERY)
		    fprintf(stderr,"   cannot commit: server(s) not ready?\n");
		else 
		    fprintf(stderr,"Error in Commit: %d %d.\n",res, res2);
		TransAPI::DeleteTrans(context->Trans,Animate::CB_TransDeleted,context);
	}

	
}

const void Animate::CB_CalculateStep(QueryAPI *Qry, void *userdata)
// Calculate one step in the random walk for each currency
// and add it to the transaction.
{

	Animate *context = (Animate *)userdata;
	int Row;			// Which row we are walking
	double limit;		// Limit value in the direction we are travelling
	double new_value;	// New calculated value for usdollar fileld

	fprintf(stderr,"Calculate new values for the currencies.\n");

	for (Row=0;Row<context->Num_Rows;Row++) {

		new_value = context->walk_vals[Row].usdollar + context->walk_vals[Row].change;

		// Check if new value has crossed the limit in the direction we are going
		// If it has, swap the sign of the change, and recalculate the new value
		if (context->walk_vals[Row].change < 0) {	
			limit = context->walk_vals[Row].zeroline - ((LIMIT/100.0) * context->walk_vals[Row].zeroline);
			if (new_value < limit) {
				context->walk_vals[Row].change = -context->walk_vals[Row].change;
				new_value = context->walk_vals[Row].usdollar + context->walk_vals[Row].change;
				printf("Lower limit crossed.\n");
			}
		}
		else {
			limit = context->walk_vals[Row].zeroline + ((LIMIT/100.0) * context->walk_vals[Row].zeroline);
			if (new_value > limit) {
				context->walk_vals[Row].change = -context->walk_vals[Row].change;
				new_value = context->walk_vals[Row].usdollar + context->walk_vals[Row].change;
				printf("Upper limit crossed\n");
			}
		}

		context->walk_vals[Row].usdollar = new_value;
		printf("%ld - %s: %lf. Change: %lf, limit: %lf\n",
			context->walk_vals[Row].RowId,
			context->walk_vals[Row].code,
			context->walk_vals[Row].usdollar,
			context->walk_vals[Row].change,
			limit);

		//fprintf(stderr,"Value of %s is now %lf.\n",
		//			context->walk_vals[Row].code,context->walk_vals[Row].usdollar);

		// Now we have calculated the new value for the row we need to get it to the database.
		if (QueryAPI::UpdateColumn(	context->Query,
									context->walk_vals[Row].RowId,
									2,
									&new_value,
									sizeof(double))) {
				fprintf(stderr,"Error occurred when writing new usdollar value for %s.\n",context->walk_vals[Row].code);
		}


	}


}

const void Animate::CB_TransDone(void *userdata)
// The random walk single step has completed on the database
// Check it all worked OK and then start another timer off for the
// next step.
{
	Animate *context = (Animate *)userdata;
	char buf[1024];
	buf[0] = '\0';

	fprintf(stderr,"Transaction complete\n");

	if (TransAPI::GetError(context->Trans,buf,1000)) {
		fprintf(stderr,"An error occurred during commit: %s\n",buf);
	}

	TransAPI::DeleteTrans(context->Trans,Animate::CB_TransDeleted,context);

}

const void Animate::CB_TransDeleted(void *userdata)
// The transaction has been deleted. Ready for another one.
{

	Animate *context = (Animate *)userdata;

	// Start timer for next stap in the 'random' walk.
	context->Timer = TimerAPI::CreateOneShotTimer(context->App,
										UPDATE_PERIOD,
										Animate::DoWalk,
										context);
}




// --------
// Activate
// --------


const int Animate::Activate (void *userdata)
 //
 // Called by the client API scheduler once it has been granted control.
 //
 // Initiates a connection to the indicated port (by default, 8001 on the
 // local host). The ConnectCallBack function will be called when
 // the connection has been established.

{
	Animate *context = (Animate *)userdata;

	if (context->FT)
		fprintf(stderr,"Connecting to %s Fault Tolerant...\n",context->Name);
	else
		fprintf(stderr, "Connecting to %s...\n",context->Name);

	context->Client = ClientAPI::StartConnect (
						context->App,
						context->Name,
						Animate::CB_Connect,
						context,
						Animate::CB_Disconnect,
						context,
						Animate::CB_ModeChange,
						context);
  
	// Fault tolerant connection - set the right options. No other
	// changes required. Not that the connection has NOT yet been
	// lauched, merely queued for launching, so that we are not
	// 'changing' the connection, merely changing the mode that it
	// it will be in, once established.

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

	return FALSE; // that is, don't call me again! 
}


// ----
// Main
// ----

#if defined(EMBEDDED)
extern "C" int poly_main(int argc, char* argv [])
#else
extern "C" int main (int argc, char* argv [])
#endif

{

	int res;
  
  // initialise the client api:
  if (res = AppAPI::Init())
    {
      Poly_Print_Error(res,"AppAPI::Init failed.");
    }  

  // create the monitoring object:
  Animate* context = new Animate(argc, argv);

  // create an AppAPI object to give context to the scheduler
  context->App = AppAPI::Create();

  // pass control to the client API, telling it the first function to call.
  AppAPI::Start(context->App, Animate::Activate, context);

  // control has been returned: tidy up and quit.
  AppAPI::Delete(context->App);
  delete context;
  AppAPI::Tidy();

  return 0;
}


/*------------------------------------------------------------------------
--		  	     End of File			   	--
------------------------------------------------------------------------*/
