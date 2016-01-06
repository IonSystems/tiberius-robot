/*------------------------------------------------------------------------------
-- Project:	Polyhedra Demo Suite
-- Copyright:	Copyright (C) 1994-2015 by Enea Software AB
--		All Rights Reserved
-- Author:	Don More
-- Description: Historian streaming client example
------------------------------------------------------------------------------*/

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#if defined(WIN32)
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#else
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

#include "polyhiststream.h"

/*----------------------------------------------------------------------------*/
int ProcessStatus(unsigned char* b)
{
    unsigned int blocks;
    unsigned int blockid;
    PHS_Value t;
    PHS_Value t2;
    unsigned int blockusecs;
    unsigned int connid;
    unsigned int columns;
    unsigned int context;
    unsigned int columnId;
    unsigned int typeId;
    unsigned int nameLen;
    unsigned char* name;
    unsigned int names;
    unsigned int tagId;


    connid = PHS_GetStatusConnectionId(b);
    printf("Connection Id %d\n",connid);

    blocks = PHS_GetStatusBlocks(b);
    printf("Blocks %d\n",blocks);

    blockid = PHS_GetStatusEarliestBlock(b);
    t = PHS_GetStatusEarliestTimestamp(b);
    t2 = PHS_GetStatusEarliestEndTimestamp(b);
    printf("Earliest block %d timestamp %d/%d/%d %02d:%02d:%02d.%06d - %d/%d/%d %02d:%02d:%02d.%06d\n",
	   blockid,
	   t.DateTime.Year,
	   t.DateTime.Month,
	   t.DateTime.Day,
	   t.DateTime.Hour,
	   t.DateTime.Minute,
	   t.DateTime.Second,
	   t.DateTime.Microsecond,
	   t2.DateTime.Year,
	   t2.DateTime.Month,
	   t2.DateTime.Day,
	   t2.DateTime.Hour,
	   t2.DateTime.Minute,
	   t2.DateTime.Second,
	   t2.DateTime.Microsecond
	   );

    blockid = PHS_GetStatusLatestBlock(b);
    t = PHS_GetStatusLatestTimestamp(b);
    t2 = PHS_GetStatusLatestEndTimestamp(b);
    printf("Latest block %d timestamp %d/%d/%d %02d:%02d:%02d.%06d - %d/%d/%d %02d:%02d:%02d.%06d\n",
	   blockid,
	   t.DateTime.Year,
	   t.DateTime.Month,
	   t.DateTime.Day,
	   t.DateTime.Hour,
	   t.DateTime.Minute,
	   t.DateTime.Second,
	   t.DateTime.Microsecond,
	   t2.DateTime.Year,
	   t2.DateTime.Month,
	   t2.DateTime.Day,
	   t2.DateTime.Hour,
	   t2.DateTime.Minute,
	   t2.DateTime.Second,
	   t2.DateTime.Microsecond
	   );

    columns = PHS_GetStatusColumns(b);
    printf("Columns %d\n",columns);

    context = 0;

    while(context = PHS_GetStatusNextColumn(b,context, &columnId,&name,
					    &nameLen, &typeId))
    {
	printf("Column %d \"",columnId);
	fwrite(name,1,nameLen,stdout);
	printf("\" (%d) type %d\n",nameLen,typeId);
    }

    names = PHS_GetStatusNames(b);
    printf("Names %d\n",names);

    context = 0;
    while(context = PHS_GetStatusNextName(b, context, &tagId, &name, &nameLen))
    {
	printf("Name %d \"",tagId);
	fwrite(name,1,nameLen,stdout);
	printf("\" (%d)\n",nameLen);
    }
    return 0;
}
/*----------------------------------------------------------------------------*/

unsigned int StartSample(unsigned char* userdata,
			 unsigned int objectId,
			 PHS_Value* timestamp,
			 unsigned int isDeleted)
{
    printf("* StartSample userdata 0x%lx object %d time %d/%d/%d %02d:%02d:%02d.%06d%s\n",
	   (unsigned long)userdata,objectId,
	   timestamp->DateTime.Year, timestamp->DateTime.Month, timestamp->DateTime.Day, timestamp->DateTime.Hour, timestamp->DateTime.Minute, timestamp->DateTime.Second, timestamp->DateTime.Microsecond,isDeleted ? " DELETED" : "");
    return 0;
}
/*----------------------------------------------------------------------------*/
unsigned int SampleColumn(unsigned char* userdata,
			  unsigned int colId,
			  unsigned int colType,
			  PHS_Value* colValue)
{
    printf("** Sample Column userdata 0x%lx id %d type %d value ",(unsigned long)userdata,colId,colType);

    if(!colValue)
    {
	/* Null value */
	printf("NULL");
    }
    else
    {
	switch(colType)
	{
	case PHS_BYTE:
	    printf("BYTE %d", (int) colValue->Byte);
	    break;

	case PHS_SHORT:
	    printf("SHORT %d", (int) colValue->Short);
	    break;

	case PHS_INTEGER:
	    printf("INTEGER %d", colValue->Integer);
	    break;

	case PHS_INTEGER64:
	    printf("INTEGER64 %lld", colValue->Integer64);
	    break;

	case PHS_FLOAT:
	    printf("FLOAT %f", (double) colValue->Float);
	    break;

	case PHS_DOUBLE:
	    printf("DOUBLE %f", colValue->Double);
	    break;

	case PHS_DATETIME:
	    printf("DATETIME %d/%d/%d %02d:%02d:%02d.%06d",
		   colValue->DateTime.Year,
		   colValue->DateTime.Month,
		   colValue->DateTime.Day,
		   colValue->DateTime.Hour,
		   colValue->DateTime.Minute,
		   colValue->DateTime.Second,
		   colValue->DateTime.Microsecond);
	    break;

	case PHS_STRING:
	    printf("STRING (%d) \"%s\"",colValue->String.Length,colValue->String.Buffer);
	    break;

	case PHS_BINARY:
	    printf("BINARY (%d) ",colValue->Binary.Length);
	    {
		int count = colValue->Binary.Length;
		unsigned char* s = colValue->Binary.Buffer;
		while(count--)
		{
		    printf("%02x%s",(unsigned int) *(s++), count ? "," : "");
		}
	    }
	    break;

	case PHS_BOOLEAN:
	    printf("BOOLEAN %s",colValue->Boolean ? "true" : "false");
	    break;
	}
    }
    printf("\n");
    return 0;
}
/*----------------------------------------------------------------------------*/
unsigned int EndSample(unsigned char* userdata,
			 unsigned int objectId,
			 PHS_Value* timestamp,
			 unsigned int isDeleted)
{
    printf("* EndSample   userdata 0x%lx object %d time %d/%d/%d %02d:%02d:%02d.%06d%s\n",
	   (unsigned long)userdata,objectId,
	   timestamp->DateTime.Year, timestamp->DateTime.Month, timestamp->DateTime.Day, timestamp->DateTime.Hour, timestamp->DateTime.Minute, timestamp->DateTime.Second, timestamp->DateTime.Microsecond,isDeleted ? " DELETED" : "");
    return 0;
}
/*----------------------------------------------------------------------------*/
unsigned int NewName(unsigned char* userdata,
		     unsigned int tagId,
		     unsigned int nameLength,
		     unsigned char* name)
{
   int i;
   printf("  New Name userdata 0x%lx id %d '",(unsigned long)userdata,tagId);
   for(i=0;i<nameLength;i++)
   {
	if(name[i]) putchar(name[i]);
    }
    printf("' (%d)\n",nameLength);
    return 0;
}
/*----------------------------------------------------------------------------*/
unsigned int Flush(unsigned char* userdata,
	      unsigned int blockno,
	      unsigned int isUserFlush,
	      PHS_Value* timestamp,
	      PHS_Value* endTimestamp)
{
    int i;
    printf("* %s userdata 0x%lx block %d timestamp %d/%d/%d %02d:%02d:%02d.%06d - %d/%d/%d %02d:%02d:%02d.%06d\n",
	   isUserFlush ? "User Flush" : "Block Finished",
	   (unsigned long)userdata,blockno,
	   timestamp->DateTime.Year, timestamp->DateTime.Month,
	   timestamp->DateTime.Day, timestamp->DateTime.Hour,
	   timestamp->DateTime.Minute, timestamp->DateTime.Second,
	   timestamp->DateTime.Microsecond,
	   endTimestamp->DateTime.Year, endTimestamp->DateTime.Month,
	   endTimestamp->DateTime.Day, endTimestamp->DateTime.Hour,
	   endTimestamp->DateTime.Minute, endTimestamp->DateTime.Second,
	   endTimestamp->DateTime.Microsecond
	   );
    return 0;
}
/*----------------------------------------------------------------------------*/
int ProcessFetch(unsigned char* b)
{
    PHS_Value timestamp = PHS_GetFetchTimestamp(b);
    PHS_Value endTimestamp = PHS_GetFetchEndTimestamp(b);
    printf("Block timestamp %d/%d/%d %02d:%02d:%02d.%06d - %d/%d/%d %02d:%02d:%02d.%06d\n",
	   timestamp.DateTime.Year, timestamp.DateTime.Month,
	   timestamp.DateTime.Day, timestamp.DateTime.Hour,
	   timestamp.DateTime.Minute, timestamp.DateTime.Second,
	   timestamp.DateTime.Microsecond,
	   endTimestamp.DateTime.Year, endTimestamp.DateTime.Month,
	   endTimestamp.DateTime.Day, endTimestamp.DateTime.Hour,
	   endTimestamp.DateTime.Minute, endTimestamp.DateTime.Second,
	   endTimestamp.DateTime.Microsecond
	);
    return PHS_FetchVisitSamples(b,
				 (unsigned char*)0x101,
				 &StartSample,
				 &SampleColumn,
				 &EndSample);
}
/*----------------------------------------------------------------------------*/
int ProcessStream(unsigned char* b)
{
    int res = PHS_StreamVisitSamples(b,
				     (unsigned char*)0x101,
				     &StartSample,
				     &SampleColumn,
				     &EndSample,
				     &NewName,
				     &Flush);
    return res;
}
/*----------------------------------------------------------------------------*/
int ParseInt(char* s, int* ok)
{
    char* endptr;
    int val = strtol(s, &endptr, 0);
    if (*endptr)
    {
	*ok = 0;
    }
    return val;
}
/*----------------------------------------------------------------------------*/
int FillAddress(char* s, struct sockaddr_in* addr)
{
    /* Looking for something like [:]port */

    int ok;
    short int port;
    char* hoststring;
    char* portstring;
    unsigned int a1,a2,a3,a4;
    portstring = strchr(s,':');
    if(portstring)
    {
	if(portstring==s)
	{
	    /* Need at least some host if : used */
	    return 0;
	}
	*portstring = '\0';
	portstring++;
	hoststring = s;
    }
    else
    {
	/* assume all s is port */
	hoststring = "127.0.0.1";
	portstring = s;
    }

    ok = 1;
    port = ParseInt(portstring,&ok);
    if(!ok)
    {
	return 0;
    }

    memset(addr, 0, sizeof(struct sockaddr_in));
    addr->sin_family = AF_INET;
    addr->sin_port = htons(port);

    if(4 != sscanf(hoststring,"%d.%d.%d.%d",&a1,&a2,&a3,&a4))
    {
	return 0;
    }
    addr->sin_addr.s_addr = htonl((((a1*256)+a2)*256+a3)*256+a4);
    return 1;
}
/*----------------------------------------------------------------------------*/
int Recv(int s, unsigned char* buf, size_t len, int flags)
{
    /* recv with a loop so that all requested data is retrieved */
    int readsofar = 0;
    while(readsofar < len)
    {
	int amount = recv(s,buf,len-readsofar,flags);
	if(amount==0)
	{
	    break;
	}
	else if(amount < 0)
	{
	    return amount;
	}
	buf += amount;
	readsofar += amount;
    }
    return readsofar;
}
/*----------------------------------------------------------------------------*/
#if defined(EMBEDDED)
int poly_main(int argc, char *argv[])
#else
int main(int argc, char *argv[])
#endif
{
    int       list_s;
    int       sock;
    short int port;
    struct    sockaddr_in servaddr;
    int maxBuffer = PHS_GetRequestBufferLength();
    unsigned char* request;
    unsigned int requestLen;
    unsigned int responseType;
    int res;
    unsigned char responseHeader[4];
    unsigned char* response;
    unsigned int responseLength;
    char** cursor;
    int ok;
    int repeat;

#if defined(WIN32)
    WSADATA data;
    if(WSAStartup(MAKEWORD(2, 2), &data))
    {
	printf("WSAStartup failed\n");
	exit(1);
    }
#endif

    request = malloc(maxBuffer);

    if(argc < 3)
    {
	printf("Usage %s [ip4address:]port request ...\n",argv[0]);
	printf("where request is one of\n");
	printf("  status logid\n");
	printf("  fetch logid blockid\n");
	printf("  stream logid latency buffersize\n");
	exit(1);
    }

    /* Set up server address */
    if(!FillAddress(argv[1],&servaddr))
    {
	printf( "%s: Invalid server address %s\n",argv[0], argv[1]);
	exit(1);
    }
    cursor = argv+2;
    argc-=2;

    /*  Create the socket  */
    if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
    {
      printf( "Error creating socket %d.\n",sock);
	perror("Error");
	exit(1);
    }

    if(connect(sock, (struct sockaddr *) &servaddr, sizeof(servaddr))<0)
    {
	printf("Error calling connect()\n");
	exit(1);
    }

    /* Loop round all requests on the command line */
    ok = 1;
    while(argc)
    {
	/* Create a request */
	if(!strcmp("status",cursor[0]))
	{
	    int logid;
	    if(argc<2)
	    {
		printf("Usage: status logid\n");
		exit(1);
	    }
	    logid = ParseInt(cursor[1],&ok);
	    if(!ok)
	    {
		printf("Invalid logid\n");
		exit(1);
	    }
	    requestLen = PHS_MakeStatusRequest(request,maxBuffer,&responseType,logid);
	    printf("Sending Status Request logid %d\n",logid);
	    cursor += 2;
	    argc -= 2;
	}
	else if(!strcmp("fetch",cursor[0]))
	{
	    int logid, blockid;
	    if(argc<3)
	    {
		printf("Usage: fetch logid blockid\n");
		exit(1);
	    }
	    logid = ParseInt(cursor[1],&ok);
	    if(!ok)
	    {
		printf("Invalid logid\n");
		exit(1);
	    }
	    blockid = ParseInt(cursor[2],&ok);
	    if(!ok)
	    {
		printf("Invalid blockid\n");
		exit(1);
	    }
	    requestLen = PHS_MakeFetchRequest(request,maxBuffer,&responseType,
					      logid,blockid);
	    printf("Sending Fetch Request logid %d blockid %d\n",
		   logid,blockid);
	    cursor += 3;
	    argc -= 3;
	}
	else if(!strcmp("stream",cursor[0]))
	{
	    int logid, latency, buffersize, tag;
	    if(argc<5)
	    {
		printf("Usage: stream logid latency buffersize highesttag\n");
		exit(1);
	    }
	    logid = ParseInt(cursor[1],&ok);
	    if(!ok)
	    {
		printf("Invalid logid\n");
		exit(1);
	    }
	    latency = ParseInt(cursor[2],&ok);
	    if(!ok)
	    {
		printf("Invalid latency\n");
		exit(1);
	    }
	    buffersize = ParseInt(cursor[3],&ok);
	    if(!ok)
	    {
		printf("Invalid buffersize\n");
		exit(1);
	    }
	    tag = ParseInt(cursor[4],&ok);
	    if(!ok)
	    {
		printf("Invalid highesttag\n");
		exit(1);
	    }
	    requestLen = PHS_MakeStreamRequest(request,maxBuffer,&responseType,
					       logid,latency,buffersize,tag);
	    printf("Sending Stream Request logid %d latency %d buffersize %d tag %d\n",
		   logid,latency,buffersize,tag);
	    cursor += 5;
	    argc -= 5;
	}
	else
	{
	    printf("Request %s is not understood\n",cursor[0]);
	    exit(1);
	}

	/* Send request out */
	res = send(sock,request,requestLen,0);
	if(res != requestLen)
	{
	    printf("Expected to write %d but only wrote %d\n",requestLen,res);
	}

	repeat = 1;
	while(repeat)
	{
	    /* Read the length back */
	    res = Recv(sock,responseHeader,4,0);
	    if(res != 4)
	    {
		printf("Could not read response header\n");
		exit(1);
	    }

	    /* Make space for the response */
	    responseLength=PHS_GetResponseRemaining(responseHeader);
	    response = malloc(responseLength);

	    /* Read the rest of the response */
	    res = Recv(sock,response,responseLength,0);
	    if(res != responseLength)
	    {
		printf("Could not read response body\n");
		exit(1);
	    }

	    printf("Read %d bytes in body\n",responseLength);

	    /* Check that response is valid or in error */
	    res = PHS_GetResponseError(response,responseLength,responseType);
	    if(res)
	    {
		printf("Response has error %d\n",res);
		exit(1);
	    }

	    switch(responseType)
	    {
	    case PHS_RQ_STATUS:
		ProcessStatus(response);
		repeat = 0;
		break;
	    case PHS_RQ_FETCH:
		ProcessFetch(response);
		repeat = 0;
		break;
	    case PHS_RQ_STREAM:
		ProcessStream(response);
		break;
	    default:
		printf("Cannot handle response type %d\n",responseType);
		break;
	    }
	    free(response);
	}
    }
    return 0;
}

/*------------------------------------------------------------------------------
-- End of file
------------------------------------------------------------------------------*/

