/*-+-----------------------------------------------------------------------+-//
//									     //
//             P O L Y H E D R A    T E S T    L I B R A R Y		     //
//									     //
//                Copyright (C) 1999-2015 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------//
//	 
//-+ Filename	 : common.hxx
//-+ Description : stuff in common to the odbc and callback versions
//                 of the performance test applications
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

#undef _POSIX_SOURCE
#if defined(VXWORKS)
#include "vxWorks.h"
#include "sysLib.h"
#include "taskLib.h"
#include "sockLib.h"
#include "hostLib.h"
#endif

#if defined(OSE)
// Problem with redefinition of OSE in ose.h
#undef OSE
#include "ose.h"
#endif

/* Service 
*/
const char *Service = "8001";


/* Data Source Name 
*/
const char *DSN = "8001";


/* default number of rows to insert/query, etc per test 
*/
int RowCount = 1000;


/* delay between tests? 
*/
int DelayTime = 0;


/* batch size for inserting when not doing an insert timer test
*/
#define INSERTBATCHSIZE 15

// size of buffer for generated SQL, assumed be at least 600
#if defined(EMBEDDED)
#define BUFFERSIZE    1000
#else
#define BUFFERSIZE    10000
#endif

/* a safety limit on the size of a batch
*/
#define MAXBATCHSIZE  100


#define CREATE_TABLE_TEST1_SQL \
    "create table test1 "      \
    "( persistent       "      \
    ", id INTEGER primary key, col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER" \
    ")"


#define CREATE_TABLE_TEST2_SQL \
    "create table test2 "      \
    "( persistent       "      \
    ", id INTEGER primary key, col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER" \
    ", col6  INTEGER, col7  INTEGER, col8  INTEGER, col9  INTEGER, col10 INTEGER" \
    ", col11 INTEGER, col12 INTEGER, col13 INTEGER, col14 INTEGER, col15 INTEGER" \
    ", col16 INTEGER, col17 INTEGER, col18 INTEGER, col19 INTEGER, col20 INTEGER" \
    ", col21 INTEGER, col22 INTEGER, col23 INTEGER, col24 INTEGER, col25 INTEGER" \
    ", col26 INTEGER, col27 INTEGER, col28 INTEGER, col29 INTEGER, col30 INTEGER" \
    ", col31 INTEGER, col32 INTEGER, col33 INTEGER, col34 INTEGER, col35 INTEGER" \
    ", col36 INTEGER, col37 INTEGER, col38 INTEGER, col39 INTEGER, col40 INTEGER" \
    ", col41 INTEGER, col42 INTEGER, col43 INTEGER, col44 INTEGER, col45 INTEGER" \
    ", col46 INTEGER, col47 INTEGER, col48 INTEGER, col49 INTEGER, col50 INTEGER" \
    ")"


// similar definitions to the above, but avoiding the word 'persistent' so that
// we can use the same code to access databases managed by other DBMSes.
// I have also made the keywords (but not the names) upper case, and made it
// explicit that primary keys are not null. If making the table names upper case,
// it will be neccesary to be consistent throughout the application, as some
// DBMSes are case-sensitive, at least on some platforms (such as MySQL on unix).
// further changes may be needed as we test against other servers.

#define CREATE_TABLE_TEST1_STANDARD_SQL \
    "CREATE TABLE test1 "      \
    "( id INTEGER NOT NULL PRIMARY KEY" \
                            ", col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER" \
    ")"

#define CREATE_TABLE_TEST2_STANDARD_SQL \
    "CREATE TABLE test2 "      \
    "( id INTEGER NOT NULL PRIMARY KEY" \
                            ", col2 REAL,col3 REAL, col4  INTEGER, col5  INTEGER" \
    ", col6  INTEGER, col7  INTEGER, col8  INTEGER, col9  INTEGER, col10 INTEGER" \
    ", col11 INTEGER, col12 INTEGER, col13 INTEGER, col14 INTEGER, col15 INTEGER" \
    ", col16 INTEGER, col17 INTEGER, col18 INTEGER, col19 INTEGER, col20 INTEGER" \
    ", col21 INTEGER, col22 INTEGER, col23 INTEGER, col24 INTEGER, col25 INTEGER" \
    ", col26 INTEGER, col27 INTEGER, col28 INTEGER, col29 INTEGER, col30 INTEGER" \
    ", col31 INTEGER, col32 INTEGER, col33 INTEGER, col34 INTEGER, col35 INTEGER" \
    ", col36 INTEGER, col37 INTEGER, col38 INTEGER, col39 INTEGER, col40 INTEGER" \
    ", col41 INTEGER, col42 INTEGER, col43 INTEGER, col44 INTEGER, col45 INTEGER" \
    ", col46 INTEGER, col47 INTEGER, col48 INTEGER, col49 INTEGER, col50 INTEGER" \
    ")"


#define MaxColumnCount 50


// ----------------------------------------------------------------------------
// pick up headers
// ----------------------------------------------------------------------------


// pick up the standard headers, which may differ between platforms.
#if defined(WIN32)
    #include <winsock.h>
    #include <windows.h>
    #undef errno
    #define errno    WSAGetLastError()
    #define close(s) closesocket(s)
#else
    #undef INET_SKIP_PROTOTYPES
    #include <unistd.h>
    #include <errno.h>
    #include <string.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #if !defined(OSE)
        #include <netinet/in.h>
        #include <arpa/inet.h>
    #endif
    #include <netdb.h>
#endif


#include <stdlib.h>
#include <stdio.h>
#include <limits.h>


// Polyhedra version number (filled in later!)

int Poly_major_number = 0;
int Poly_minor_number = 0;
int Poly_build_number = 0;


// ----------------------------------------------------------------------------
// some extra flags to decide what to test: set up AFTER picking up the 
// standard headers, since on some platforms the platform-identifying
// flags are set up there rather than by the compiler.
//-----------------------------------------------------------------------------


// define a flag that will be undefined on those platforms where we will not
// be wanting to do a UDP-based 'bounce' timing test.


#if defined(VXWORKS) || defined(OSE) || defined(INTEGRITY)
#else
#define TEST_BOUNCE
#endif


// define a flag which will cause a series of 'ticks' to be written out
// when testing the clock granularity, as a visual cross-check.

#if defined(OSE)
//#define VISUAL_CLOCK_CHECK
//#include "ose.h"
#endif


// ----------------------------------------------------------------------------
// more platform-specific stuff
// ----------------------------------------------------------------------------


#if defined(OSE)

// on some OSE platforms, gethostname might not be defined,
// so define a dummy version instead.

#if !defined(softOSE)
int gethostname (char *name, size_t len)
{
    strncpy (name, "localhost", len);
    return 0;
}
#endif
#endif


#if defined(WIN32)

// on Windows, we have to call some extra initialisation to set the scene
// for the UDP-based 'bounce' test.

  int Init_IO ()
  {
      WSAData data;
      int res;

      if ((res = ::WSAStartup(MAKEWORD(2, 2), &data)) != 0)
          {
          printf("WARNING: failed to startup Winsock %d\n", res);
      }
      return res;
  }

  void End_IO ()
  {
    ::WSACleanup();

  }
#else
  int Init_IO ()
  {
      return 0;
  }

  void End_IO ()
  {
  }  
#endif



// ----------------------------------------------------------------------------
// timer code.
// 
// note that the behaviour of clock () difers between machines; on Windows, for
// example, it returns elapsed time, whereas on Linux it is the CPU time 
// consumed by the client (ignoring the time taken in comms and in the
// database) and so useless to us for all except the 'raw CPU power' tests.
// ----------------------------------------------------------------------------

#include <time.h>

// on certain platforms, the CLOCKS_PER_SEC might not be set right, so
// define TICKTIME = CLOCKS_PER_SEC here, so that it can be redefined in
// platform-specific fashion where appropriate.

#define TICKTIME CLOCKS_PER_SEC


#if defined(WIN32)

    #define USE_CLOCK YES

    void sleep (int secs)
    {
      Sleep (secs * 1000);
    }

#elif defined(OSE)
    
    #define USE_CLOCK YES
    
    // work round bug in ose4.4/powerpc/include/time.h:
    // CLOCKS_PER_SEC is 1,000 not 1,000,000
    #undef  TICKTIME
    #define TICKTIME 1000000
    
    void sleep (int secs)
    {
      delay (secs * 1000);
    }

#endif


/* define the_tick (and the_microsecond, currently only used
   in testing clock resolution; to be meaningful, it should
   use the same underlying mechanism as the_tick).
*/

#if defined(VXWORKS)

    void sleep (int secs)
    {
	taskDelay (CLOCKS_PER_SEC * secs);
    }

    double the_tick ()
    {
	struct timespec t;
	double seconds;

	clock_gettime(CLOCK_REALTIME, &t);
	seconds = t.tv_sec + ((double)t.tv_nsec)/1000000000.0;
	return seconds;
    }

    int the_microsecond ()
    {
	struct timespec t;

	clock_gettime(CLOCK_REALTIME, &t);
	return t.tv_nsec / 1000;
    }

#elif defined(USE_CLOCK)

    // the clock function is supposed to return the time
    // taken by the current process, but on some systems
    // just measures the time since the process (or
    // machine) started - which is actually just what we
    // we want, as we need to include the time taken in
    // the database and in comms delays.

    double the_tick ()
    {
	return(double) (clock ()) / TICKTIME;
    }

    int the_microsecond ()
    {
	return (clock () % TICKTIME) * (1000000 / TICKTIME);
    }

#else

#if defined(INTEGRITY)
    extern "C"
    {
#endif
    #include <sys/times.h>
#if defined(INTEGRITY)
    }
#endif

    double the_tick ()
    {
	tms tmsbuff;

	#ifndef CLK_TCK
	int CLK_TCK = sysconf(_SC_CLK_TCK);
	#endif
	return (double) (times (&tmsbuff)) / CLK_TCK;
    }

    int the_microsecond ()
    {
	tms tmsbuff;
	#ifndef CLK_TCK
	int CLK_TCK = sysconf(_SC_CLK_TCK);
	#endif
	return (times (&tmsbuff) % CLK_TCK) * (1000000 / CLK_TCK);
    }
#endif


/* apparent minimal interval, in seconds
 */

double MinInterval = 0.0;


/* Number of times one can read the clock per second
*/
int ReadTicksPerSec = 0;


/* how many seconds did an operation take?
*/
double HowLong (double start)
{
    return the_tick () - start;
}


/* print out the time taken by an operation, and a rate indication
  where an opcount is given.
*/
double HowFast (double start, const char* optype, int opcount)
{
    double duration = HowLong (start);
    double rate     = 0.0;
    const char*  gt = "";

    printf ("\ttime: %2.2lf seconds\n", duration);
    if (opcount > 1)
    {
        if (duration==0)
        {
            duration = MinInterval;
            gt = "> ";
        }
        if (duration > 0)
        {
            rate = (double)opcount / duration;
            if (rate > 1000)
                printf ("\t%s rate: %s%2.0lf per second\n", optype, gt, rate);
            else
                printf ("\t%s rate: %s%2.2lf per second\n", optype, gt, rate);
        }
    }
    else
    {
        rate = duration;
    }
    printf("\n");
    return rate;
}


// -----------------------------------------------------------------------------
//                      T e s t R e c o r d ,   e t c .
// -----------------------------------------------------------------------------
// stuff to record info about test results, for later display
// -----------------------------------------------------------------------------


char* identify (char* name, size_t len)
{
    if (gethostname (name, len) != 0)
        return (char*) "unknown";
    else
        return name;
}


class TestRecord
{
public:
    const char* Test;
    double      Rate;
    TestRecord* Next;

    TestRecord (const char* test, double rate)
    {
        Test = test;
        Rate = rate;
        Next = NULL;
    }
};

class TestRecords
{
    TestRecord* FirstRecord;
    TestRecord* LatestRecord;
    char*       Platform;
    const char* API;
    char        PlatformArea[50];

public:
    TestRecords (const char* api)
    {
        Platform     = identify (PlatformArea, sizeof (PlatformArea));
        API          = api;
        FirstRecord  = NULL;
        LatestRecord = NULL;

        // wait a bit before running the sequence of tests, to allow the
        // database (if running) to settle down. On UNIX platforms we make
        // use of the 'sleep' command in a shell script.
        if (DelayTime > 0)
	{ 
	    printf ("(delaying %d seconds to let database stabilise)\n", DelayTime);
	    sleep (DelayTime); 
	}
    };

    ~TestRecords ()
    {
        TestRecord* tr = FirstRecord;
        TestRecord* tr2;

        printf("\n\nresult summary for %s (%s API):\n\n", Platform, API);

        while (tr != NULL)
        {
            printf( "\t**** %s %s (%d.%d.%d): %s => %2.2lf\n", 
                    Platform, API, 
		    Poly_major_number, Poly_minor_number, Poly_build_number,
		    tr->Test, tr->Rate
                   );
            tr2 = tr->Next;
            delete tr;
            tr = tr2;
        }
        printf("\nend of summary.\n\n");
    };

    void Clear()
    {
        TestRecord* tr = FirstRecord;
        TestRecord* tr2;
        while (tr != NULL)
        {
            tr2 = tr->Next;
            delete tr;
            tr = tr2;
        }
	FirstRecord = NULL;
	LatestRecord = NULL;
    }

    void Record (const char* test, double rate)
    {
        TestRecord* tr = new TestRecord (test, rate);
        if (FirstRecord == NULL)
        {
            FirstRecord = tr;
        }
        else
        {
            LatestRecord->Next = tr;
        }
        LatestRecord = tr;
        if (DelayTime > 0) sleep (1); // give the system time to become idle.
    };
};


// ----------------------------------------------------------------------------


TestRecords* Recorder = NULL;


// ----------------------------------------------------------------------------
// useful macros, constants and functions
// ----------------------------------------------------------------------------


#if !defined(TRUE)
    #define TRUE  1
    #define FALSE 0
#endif


#define MAX_STRING_BUFFER_LENGTH	1024

#define MAX_COLUMN_BUFFER_LENGTH	256


/* Name of current test */
const char *CurrentTest = "No test";


/* Set-up name of current test 
*/
void set_test ( const char *name,
                const char *purpose = NULL
              )
{
    CurrentTest = name;
    printf("\nTest: %s\n\n", CurrentTest);
    if (purpose != NULL)
    {
        printf("\t%s\n\n", purpose);
    }
}


/* Fail 
*/
void fail ( const char *    filename,
            int             lineno
          )
{
    printf ( "%s: Failed on line %d of file %s\n",
             CurrentTest, lineno, filename
           );
    exit(1);
}


/* Assert
*/
#define assert(x) assert_line((x), __FILE__, __LINE__)
void assert_line ( int          e,
                   const char * filename,
                   int          lineno
                 )
{
    if (e) return;
    fail(filename, lineno);
}


// ----------------------------------------------------------------------------
//  some simple, Polyhedra-independent calibration tests.
// ----------------------------------------------------------------------------

/* do a number of 'pings' (sending a message to oneself, and then 
   reading it), and return the time taken to do that many - which is
   of course half the time to do that many ping-pongs with a partner.
 */
double pings (int s1, int s2, int ct)
{
    int     i;
    double start = the_tick ();

    //fprintf (stderr, "ping (..., %d) called.\n", ct);

    for (i=0; i<ct; i++)
    {
        #if defined(OSE)
            inet_send (s2, "TEST", 4, 0);
        #else
            send      (s2, "TEST", 4, 0);
        #endif
        
        int len = 0;
        char b[4];
        if (recvfrom (s1, b, 4, 0, NULL, 0) != 4)
        {
            // Output streams are not set-up for this task
            // We should terminate the task?
            printf ("Failed to receive valid message %d %d\n",
                    errno, len);
            return -1;
        }
        //printf(".");
    }
    return the_tick() - start;
}


int bounce (int portno)
{
    int result = -1;

#ifdef TEST_BOUNCE

    // first set up the 'public' socket, known port,
    // to which we shall send messages.

    struct hostent *hp;
    if ((hp = gethostbyname("127.0.0.1")) == NULL)
    {
        fprintf(stderr, "cannot get local host info\n");
        return result;
    }

    int s1 = socket (hp->h_addrtype, SOCK_DGRAM, 0);
    if (s1 < 0)
    {
        printf ("Failed to create 1st socket %d %d\n", s1, errno);
        return result;
    }

    sockaddr_in addr1;
    memset (&addr1, 0, sizeof (addr1));
    addr1.sin_family      = hp->h_addrtype;
    addr1.sin_addr.s_addr = INADDR_ANY;
    addr1.sin_port        = htons (portno); 
    if (bind (s1, (sockaddr *)&addr1, sizeof (addr1)) != 0)
    {
        printf ("Failed to bind 1st socket, error code %d\n", errno);
    }
    else
    {
        // first socket set up OK, and bound.
        // now lets try setting up the sending socket...

        int s2 = socket (AF_INET, SOCK_DGRAM, 0);
        if (s2 < 0)
        {
            printf ("Failed to create 2nd socket %d %d\n", s2, errno);
        }
        else
        {
            sockaddr_in addr2;
            memset (&addr2, 0, sizeof (addr2));
            addr2.sin_family      = AF_INET;
            addr2.sin_addr.s_addr = inet_addr("127.0.0.1");
            addr2.sin_port        = htons(portno); 
            if (connect(s2, (sockaddr *)&addr2, sizeof (addr2)) != 0)
            {
                printf ("Failed to connect 2nd socket, error code %d\n",
                        errno);
            }
            else
            {
                // need to send on s2, read on s1, repeat ad nauseam - 
                // Oh, and keep track of time.
                // we shall be naive, and assume no-one else is
                // sending to us, which would confuse things a trifle.

                int  i = 50;
                double pingres;

                for (;;)
                {
                    i *= 2;
                    if ((pingres = pings (s1, s2, i)) >= 1)
                    {
                        break;
                    }
                    //printf ("bounce %d %g\n", i, pingres);
                }

                // calculate round trips per second.
                result = (int)( (double)i / (pingres*2) );
            }
            close (s2);
        }
    }
    close (s1);

#endif // TEST_BOUNCE

    return result;
}


void printSpeed (double d)
{
    if (d <0.5)
        printf ( "%1.2f\n", d);
    else if (d < 10)
        printf ( "%1.1f\n", d);
    else
        printf ( "%3.0f\n", d);
}


#define ASIZE 10000
#define namelen 100


int raw_performance ()
{
    char    name[namelen] ;
    int     i;
    int     j;
    int     k = 0;
    long    interval;
    double  start, finish;
    double  duration, rate;

    set_test("raw CPU/OS performance",
             "determine how fast is the machine on which we are about "
             "\n\tto run Polyhedra.");

    printf ("\tMachine name is %s.\n", identify (name, namelen));
    printf ("\tSystem constant 'CLOCKS_PER_SEC' is set to %ld.\n",
            CLOCKS_PER_SEC
           );
    Recorder->Record ("clocks_per_sec", CLOCKS_PER_SEC);
    if (TICKTIME!=CLOCKS_PER_SEC)
    {
        printf ("\tSystem constant 'CLOCKS_PER_SEC' should be %ld!\n",
                TICKTIME
                );
        Recorder->Record ("ticktime", TICKTIME);
    }

    /* estimate minimum interval */

    start = the_tick ();
    while ((finish=the_tick ()) == start)
        ;
    //interval    = finish-start;
    //MinInterval = (double)(finish - start) / TICKTIME;
    MinInterval = finish - start;
    interval = (long)((MinInterval + 0.5/TICKTIME) * TICKTIME);
    printf ( "\tMinimal interval seems to be %ld ticks, 1/%d of a second.\n", 
             interval, (int)(1/MinInterval));
    Recorder->Record ("interval", MinInterval);

    /* how expensive is it reading the clock? */

    double tick1 = the_tick ();
    j = 0;
    while (the_tick() < tick1+1)
    {
        j++;
    }
    ReadTicksPerSec = j;

    printf("\tCan read the clock %d times per second.\n", ReadTicksPerSec);
    Recorder->Record ("readTicksPerSec", ReadTicksPerSec);
    
    /* guess how much can be done in a few clock ticks */

    i = 200000L;
    do 
    {
        j  = i;
        i *= 2;
        start = the_tick ();
        while ( j-- )
            k++;
        finish = the_tick ();
    } while (finish-start <= 4 * MinInterval && i > 0);
    i *= 4;
    j = k; // do anything to stop the compiler warning 'k set but not used'!

    if (i < 0)
    { 
        i = INT_MAX;
    }

    /* Measure 1 of processor speed - all cached, might be optimised out?
    */

    printf ( "\tTime to do %d almost-empty loops is ", i );
    j = i;
    start = the_tick();

    while ( j-- )
        k++;

    duration = the_tick () - start;
    printf ( "%2.2f seconds\n\tspeed factor 1 = ", 
             duration);
    if (duration == 0)
        rate = 0;
    else
        rate = (double) i / (duration * 1700000);
    printSpeed (rate);
    //Recorder->Record ("speed1", rate);

    /* Measure 2 of processor speed - 
        I suspect the code will still be cached, but perhaps not the data
    */

    int* area = new int[ASIZE];
    if (area==0)
    {
        printf("no room!\n");
        return 0;
    }
    for (j=0; j<ASIZE; j++ )
    {
        area[j]=0;
    }

    j = (i / 129) * 20;
    printf ( "\tTime to do  %d non-empty    loops is ", j );
    start = the_tick ();

    while (j >= 20)
    {
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;

        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;

        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;

        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
        j--; area[j % ASIZE]++;
    }
    delete area;

    duration = the_tick () - start;
    printf ("%2.2f seconds\n\tspeed factor 2 = ", duration);
    rate = (double) i / (duration * 2500000);
    printSpeed (rate);
    Recorder->Record ("speed2", rate);

    // estimate I/O cost.

    int bres = bounce (8001);
    if (bres < 0)
    {
        printf(" - failed to determine UDP bounce rate.\n");
    }
    else
    {
        printf ( "\tusing UDP, sent %d round-trip messages per second.\n", 
                 bres);
        Recorder->Record ("bounce", bres);
    }

    return 0;
}

int check_clock ()
{
    long    i;
    long    j;

    if (MinInterval == 0.0 || ReadTicksPerSec == 0)
    {
	printf ("\n(cannot run check_clock () "
		"as clock granularity unknown.)\n");
	return -1;
    }

    if (MinInterval < 0.001 || MinInterval < 1.0 / ReadTicksPerSec)
    {
	printf ("\n(cannot run check_clock () as MinInterval "
		"too small for reasonable results.)\n");
	return -1;
    }

    set_test("check tick distribution",
             "see if the times reported by the clock are evenly"
             "\n\tspread within the second.");

    int intervalCt = (int) (1 / MinInterval);
    int resolution = 1000000 / intervalCt;
    int* tick_ct   = new int[intervalCt+1];
    if (tick_ct != NULL)
    {
	// empty the array of counts

	for (j=0; j<=intervalCt; j++)
	{
	    tick_ct[j] = 0;
	}

	// gather data for a few seconds

	int samples = ReadTicksPerSec * 9;
	for (j=0; j<samples; j++)
	{
	    i = the_microsecond() / resolution;
	    tick_ct[i]++;
	}

	// calculate mean & variance, and look for anomalies. 
	// ideally we want a flat distribution of times, with
	// no bumps or hollows. for a uniform distribution the
	// variance should be 1/12.

	double sum = 0;
	double var = 0;
	int    ok  = TRUE;
	double avg = samples / intervalCt;

	for (j=0; j<intervalCt; j++)
	{
	    double x  = j / ((double)intervalCt);
	    double y = tick_ct[j] / ((double)samples);
	    double z = tick_ct[j] / avg - 1;
	    if (z*z > 0.05)
	    {
		// value seems far out of range; flag it by
		// setting it -ve, and clear 'OK' to get a
		// report generated later.
		ok = FALSE;
		tick_ct[j] = -tick_ct[j];
	    }
	    sum +=  x*y;
	    var +=  x*x*y;
	}
	var -=sum*sum;

	// print out statistics, and also a map if anomalies seen.

	printf("\tmean of tick in seconds is %0.4f (target 0.5);\n", sum);
	printf("\tvariance is %0.4f (target 0.0833).\n", var);
	if (ok == FALSE                    // odd value noticed
	    || sum < 0.450 || sum > 0.550  // mean     out of range
	    || var < 0.078 || var > 0.088  // variance out of range
	    ) 
	{
	    printf ("\nChart showing distribution of clock times; "
		    "distribution should be even,"
		    "\neach value approximately %d. "
		    "Anomalous readings are flagged with a *.\n"
		    "(NB: other work on the m/c will cause unevenness, "
		    "so don't panic unduly.)\n",
		    (int)avg);

	    for (j=0; j<intervalCt; j++)
	    {  
		if (j % 10 == 0) 
		    printf ("\n");
		else
		    printf(" ");
		i = tick_ct[j];
		if (i >0) 
		    printf ("%6ld ", i);
		else
		    printf ("%6ld*", -i);
	    }
	    printf ("\n\n");
	}
	delete tick_ct;
    }

    #ifdef VISUAL_CLOCK_CHECK
    /* allow watcher to visually check clock is clicking OK
    */
    printf("\n\anow do a number of 1/10th-second ticks.\n\n");

    int systick  = system_tick();
    int tickspersecond = 1000000 / systick;
    printf("(systick=%d, tickspersecond=%d.)\n", systick, tickspersecond);

    struct timeval tv;
    struct timezone tz;
    OSTICK micro, ticks;
    int secs, usecs, res, tov_secs, tov_usecs;
    
    for (j=1;j<=50;j++)
    {
	double next_tick = the_tick () + 0.05;
        while (the_tick () < next_tick)
	{
	}

	ticks = get_systime(&micro);
	secs = ticks / tickspersecond;
	usecs = micro + (ticks % tickspersecond) * systick;
	res = ::gettimeofday(&tv, &tz);
	tov_secs  = tv.tv_sec;
	tov_usecs = tv.tv_usec;

	printf("tick %2d, clock = %d, the_tick=%f, get_systime=%d+%04d (%d.%06d), gettov=%d (%d.%06d).\n",
	              j, clock (),   the_tick (), ticks, micro, secs, usecs,   res, tov_secs, tov_usecs);
    }
    printf ("\n");
    #endif

    return 0;
}

/*---------------------------------------------------------------------------*/
/*                          e n d   o f   f i l e                            */
/*---------------------------------------------------------------------------*/
