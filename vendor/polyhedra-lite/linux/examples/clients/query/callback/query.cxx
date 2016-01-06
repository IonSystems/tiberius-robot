//
//	POLYHEDRA DEMO SUITE
//
//	Copyright (C) 2000-2015 by Enea Software AB
//
//	Query
//
//	This program illustrates how a static query may be launched 
//	using the Polyhedra callback API.
//
//	The static_query executable is run and given a single
//	arguement - the data service of the rtrdb.
//
//	The query "select * from currency" is run, the results
//	of which are displayed.
//
//	---------------------------------------
//
//	V1.0 -	Dave Stow
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

#define FALSE 0
#define TRUE 1

//	Define a global with the sql select string in it
//	Feel free to play with this, but remember that you
//	will need to alter the RowCallBack method in the
//	StaticQuery class. 
char SQL_String[]="select * from currency";

// Prototype for the Polyhedra Error message output
void Print_Error(int err,const char *location);

//	Define a class to keep track of what is happening:
//	we will have just one of these. It defines the various
//	(static) functions that the client api will be calling
//	to signal that it has done its work. 
class StaticQuery
{
  ClientAPI*	Client;		// Client instance
  QueryAPI*		Query;		// Query instance
  const char*			Name;		// Name of dataservice to connect to
  
public:
	AppAPI*    App;
  
	StaticQuery  (int argc, char *argv[])
	{
		if (argc == 1)
			Name = "8001";
		else
			Name = argv[1];

		Client = 0;
	};
  
	~StaticQuery () {};
	void Stop();
  
	// Define the various methods - these are all callbacks
	// Activate is called when the scheduler is started. It
	// calls StartConnect, and CB_Connect is called when the
	// the connection to the database is made.
	static const int  Activate		(void *userdata);
	static const void CB_Connect	(void *userdata);

	// Inside CB_Connect the query is started. CB_Row is called
	// once for each row returned by the query. CB_QueryDone is
	// called when all rows have been returned.
	static const void CB_Row		(void *userdata);
	static const void CB_QueryDone	(void *userdata);
	static const void CB_DeleteDone	(void *userdata);

};


const int StaticQuery::Activate (void *userdata)
//	Called by the client API scheduler once it has
//	been granted control. Returns 0 to prevent the
//	scheduler calling it again.
//
//	The argument is cast back to an StaticQuery pointer,
//	and a connection request is set up. Also, for security,
//	a fail-safe timer is set off


{	
  StaticQuery *context = (StaticQuery *)userdata;

  printf ("Connecting to database at %s...\n",context->Name);

  context->Client = ClientAPI::StartConnect (
						context->App,
						context->Name,
						StaticQuery::CB_Connect,
						context);
  
  return FALSE; // false - that is, don't call me again! 
}



const void StaticQuery::CB_Connect(void *userdata)
//	Called once a connection to the database has either 
//	been established or the	attempt to set it up failed.
//
//	Check the error code and if all is ok, get on to the
//	next part of the job. In this case, all we need to do
//	is launch the query, telling it which functions are
//	to be called back later.

{ 

	StaticQuery *context = (StaticQuery *) userdata;
	int res = ClientAPI::GetError (context->Client);
  
	if (res != 0) {
		Print_Error(res,"connect to database");

		// Make a tentative guess about why the connect failed
		if (res == POLY_ECONNECT) printf("Is the database started correctly?\n");

		// We've failed. Stop the program.
		context->Stop();
	}
	else {
		printf ("Connected, now launch query...\n");

		context->Query = QueryAPI::StartQuery (
							context->Client, 
							SQL_String,
							StaticQuery::CB_Row,
							StaticQuery::CB_QueryDone, 
							context);
	}

}


//	-------------------------------------
//	Call backs associated with the query
//	-------------------------------------

const void StaticQuery::CB_Row(void *userdata)
//	This is called for each row returned by the query.
//	Each column is accessed using the CopyColumn function
//	call. 
//
//	As it stands, the query returns the columns
//	country, name, and usdollar. If you modify the query 
//	to return different columns, then you will need to 
//	modify this routine.

{
	StaticQuery *context = (StaticQuery*) userdata;
	int res  = QueryAPI::GetError(context->Query);

	// Variables to hold column values

	char code[4];		// Currency code
	char ctry[100];		// Country column
	char name[100];		// Name of currency
	double d_val;		// US dollar value

	if (res == 0) {

		// Copy column "code"
		if (QueryAPI::CopyColumn(context->Query,
									"code",
									code,
									4) == 0) {
			code[0]='\0';
		}

		// Copy column "country"
		if (QueryAPI::CopyColumn(context->Query,
									"country",
									ctry,
									100) == 0) {
			ctry[0]='\0';
		}

		// Copy column "name"
		if (QueryAPI::CopyColumn(context->Query,
									"name",
									name,
									100) == 0) {
			name[0]='\0';
		}

		// Copy column "usdollar"
		if (QueryAPI::CopyColumn(context->Query,
									"usdollar",
									&d_val,
									sizeof(double)) == 0) {
			d_val=0;
		}

		printf("Currency code: %s: 1 US Dollar buys %0.2lf %s %s.\n",
					code,d_val,ctry,name);

	}
	else {
		// Very unlikely to get called here - if the query
		// fails you would get a failed code in the 
		// Query Complete call back.
		Print_Error(res,"row callback");

		// Its failed - stop to program
		context->Stop();
	}

}


const void StaticQuery::CB_QueryDone(void *userdata)
//	This callback is called when the query has completed.
//	time to disconnect, using the Stop method

{
	StaticQuery *context = (StaticQuery*) userdata;
	int res = QueryAPI::GetError(context->Query);

	if (res == 0) {
		printf("All rows returned.\n");
	}
	else {
		Print_Error(res,"query done");

		// Make a tentative guess about why the query failed.
		if (res == POLY_EQUERY) printf("Is the right database started?\n");

		// Failure. Stop the program
	}
	context->Stop();
}

void StaticQuery::Stop()
//	called to disconnect the client

{
	if (Client)
		ClientAPI::DeleteClient(Client, 
					StaticQuery::CB_DeleteDone, 
					this);
	else
		StaticQuery::CB_DeleteDone(this);
}

const void StaticQuery::CB_DeleteDone(void *userdata)
//	This callback is called when the client has been deleted.
//	As this is the end of this example the AppAPI::Stop
//	method is called.

{
	StaticQuery *context = (StaticQuery*) userdata;
	AppAPI::Stop(context->App);
} 

void Print_Error(int err,const char *location)
// Print out Polyhedra error messages
{
	fprintf(stderr,"Error in %s. Code %d (%s)\n%s\n",
		location,err,Poly_Errors_Name[err],Poly_Errors_Msg[err]);
}

#if defined(EMBEDDED)
extern "C" int poly_main(int argc, char* argv [])
#else
extern "C" int main (int argc, char* argv [])
#endif

//	Main - this is the entry point into the program.
{
	int res;
  
	// initialise the client api:
	if (res = AppAPI::Init()) {
		Print_Error(res,"initialisation of API");
		return 10;
    }

	// create the monitoring object:
	StaticQuery* context = new StaticQuery(argc,argv);
  
	// create an AppAPI object to give context to the scheduler
	context->App = AppAPI::Create();

	// pass control to the client API, telling it the
	// first function to call.
	AppAPI::Start(context->App, StaticQuery::Activate, context);

	// control has been returned: tidy up and quit.
	AppAPI::Delete(context->App);
	delete context;
	AppAPI::Tidy();
	return 0;
}


/*------------------------------------------------------------------------
--		  	     End of File			   	--
------------------------------------------------------------------------*/
