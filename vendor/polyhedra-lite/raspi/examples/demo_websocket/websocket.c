//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2015 by Enea Software AB
//		All Rights Reserved
// Description:	Example Websocket Middleware.
//
// This file is an example implementation of a middleware component that
// provides data from a Polyhedra RTRDB database to a websocket client.
// When a websocket client requests it, the server executes an active query
// on the RTRDB. The initial results are forwarded to the client. When the
// server is informed of changes to the results of the active query, the
// changes are again forwarded to the client. There is no polling of the
// websocket server or RTRDB. The active query mechanism pushes changes to
// the websocket server and the websocket protocol pushes the changes to the
// websocket client.
//
//----------------------------------------------------------------------------*/

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

/*
------------------------------------------------------------------------------
-- Includes
------------------------------------------------------------------------------
*/

// Define WIN32 to compile this file on Windows.
#if defined(WIN32)
#include <winsock2.h>
typedef int socklen_t;
#else
#include <unistd.h>
#include <sys/socket.h>
#include <wait.h>
#include <netinet/in.h>
#include <stdint.h>
#endif

/* Include standard header files */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/* Include the ODBC header files */
/* Define SIXTYFOURBIT if client is 64-bit */
//#define SIXTYFOURBIT

#include "sql.h"
#if !defined(ODBC_STD)
#include "sqlext.h"
#include "sqlpoly.h"
#endif

#include <sys/types.h>

#include <math.h>
#include <stdlib.h>


/*
----------------------------------------------------------------------------
-- Useful macros
----------------------------------------------------------------------------
*/

// The SHA1 implementation needs to know byte ordering. This works for
// gcc and Windows x86. Replace as appropriate
#if BYTE_ORDER == LITTLE_ENDIAN
#define SHA1_LITTLE_ENDIAN
#endif

// Maximum message size handled.
#define BUFLEN 10000

#define FALSE 0
#define TRUE 1

/* Longest column name we can handle */
#define MAX_COLUMN_NAME         256

/* Longest string value length we can handle */
#define MAX_STRING_LENGTH       256

/* Longest binary value length we can handle */
#define MAX_BINARY_LENGTH       256

/* Longest diagnostic message we can handle */
#define MAX_DIAG_MSG		256

/* Maximum number of currencies we want to deal with */
#define MAX_CURRENCIES		100

/*
----------------------------------------------------------------------------
-- Global variables
----------------------------------------------------------------------------
*/

/* Buffer for holding bookmark - know that 4 bytes is big enough */
SQLUINTEGER		Bookmark;

/* Array for holding row status */
SQLUSMALLINT		RowStatusArray[1];

/* Array for holding column status - number of columns in select + one for bookmark */
SQLUSMALLINT		ColumnStatusArray[5];

/*------------------------------------------------------------------------------
// SHA-1 Ported to C from 100% free public domain implementation of
// the SHA-1 algorithm by Dominik Reichl <Dominik.Reichl@tiscali.de>
//----------------------------------------------------------------------------*/

typedef union
{
    unsigned char c[64];
    unsigned int l[16];
} SHA1_WORKSPACE_BLOCK;

struct SHA1
{
    unsigned int m_state[5];
    unsigned int m_count[2];
    unsigned char m_buffer[64];
};

void SHA1_Init(struct SHA1* s)
{
    // SHA1 initialization constants
    s->m_state[0] = 0x67452301;
    s->m_state[1] = 0xEFCDAB89;
    s->m_state[2] = 0x98BADCFE;
    s->m_state[3] = 0x10325476;
    s->m_state[4] = 0xC3D2E1F0;

    s->m_count[0] = 0;
    s->m_count[1] = 0;
}

// Rotate x bits to the left
#define ROL32(value, bits) (((value)<<(bits))|((value)>>(32-(bits))))

#if defined(SHA1_LITTLE_ENDIAN)
  #define SHABLK0(i) (block->l[i] = (ROL32(block->l[i],24) & 0xFF00FF00) \
			| (ROL32(block->l[i],8) & 0x00FF00FF))
#else
  #define SHABLK0(i) (block->l[i])
#endif

#define SHABLK(i) (block->l[i&15] = ROL32(block->l[(i+13)&15] ^ block->l[(i+8)&15] \
		^ block->l[(i+2)&15] ^ block->l[i&15],1))

// SHA-1 rounds
#define SHAR0(v,w,x,y,z,i) { z+=((w&(x^y))^y)+SHABLK0(i)+0x5A827999+ROL32(v,5); w=ROL32(w,30); }
#define SHAR1(v,w,x,y,z,i) { z+=((w&(x^y))^y)+SHABLK(i)+0x5A827999+ROL32(v,5); w=ROL32(w,30); }
#define SHAR2(v,w,x,y,z,i) { z+=(w^x^y)+SHABLK(i)+0x6ED9EBA1+ROL32(v,5); w=ROL32(w,30); }
#define SHAR3(v,w,x,y,z,i) { z+=(((w|x)&y)|(w&x))+SHABLK(i)+0x8F1BBCDC+ROL32(v,5); w=ROL32(w,30); }
#define SHAR4(v,w,x,y,z,i) { z+=(w^x^y)+SHABLK(i)+0xCA62C1D6+ROL32(v,5); w=ROL32(w,30); }

static void SHA1_Transform(unsigned int* state, unsigned char* buffer)
{
    unsigned int a = 0, b = 0, c = 0, d = 0, e = 0;

    SHA1_WORKSPACE_BLOCK* block;
    unsigned char workspace[64];
    block = (SHA1_WORKSPACE_BLOCK *)workspace;
    memcpy(block, buffer, 64);

    // Copy state[] to working vars
    a = state[0];
    b = state[1];
    c = state[2];
    d = state[3];
    e = state[4];

    // 4 rounds of 20 operations each. Loop unrolled.
    SHAR0(a,b,c,d,e, 0); SHAR0(e,a,b,c,d, 1); SHAR0(d,e,a,b,c, 2); SHAR0(c,d,e,a,b, 3);
    SHAR0(b,c,d,e,a, 4); SHAR0(a,b,c,d,e, 5); SHAR0(e,a,b,c,d, 6); SHAR0(d,e,a,b,c, 7);
    SHAR0(c,d,e,a,b, 8); SHAR0(b,c,d,e,a, 9); SHAR0(a,b,c,d,e,10); SHAR0(e,a,b,c,d,11);
    SHAR0(d,e,a,b,c,12); SHAR0(c,d,e,a,b,13); SHAR0(b,c,d,e,a,14); SHAR0(a,b,c,d,e,15);
    SHAR1(e,a,b,c,d,16); SHAR1(d,e,a,b,c,17); SHAR1(c,d,e,a,b,18); SHAR1(b,c,d,e,a,19);
    SHAR2(a,b,c,d,e,20); SHAR2(e,a,b,c,d,21); SHAR2(d,e,a,b,c,22); SHAR2(c,d,e,a,b,23);
    SHAR2(b,c,d,e,a,24); SHAR2(a,b,c,d,e,25); SHAR2(e,a,b,c,d,26); SHAR2(d,e,a,b,c,27);
    SHAR2(c,d,e,a,b,28); SHAR2(b,c,d,e,a,29); SHAR2(a,b,c,d,e,30); SHAR2(e,a,b,c,d,31);
    SHAR2(d,e,a,b,c,32); SHAR2(c,d,e,a,b,33); SHAR2(b,c,d,e,a,34); SHAR2(a,b,c,d,e,35);
    SHAR2(e,a,b,c,d,36); SHAR2(d,e,a,b,c,37); SHAR2(c,d,e,a,b,38); SHAR2(b,c,d,e,a,39);
    SHAR3(a,b,c,d,e,40); SHAR3(e,a,b,c,d,41); SHAR3(d,e,a,b,c,42); SHAR3(c,d,e,a,b,43);
    SHAR3(b,c,d,e,a,44); SHAR3(a,b,c,d,e,45); SHAR3(e,a,b,c,d,46); SHAR3(d,e,a,b,c,47);
    SHAR3(c,d,e,a,b,48); SHAR3(b,c,d,e,a,49); SHAR3(a,b,c,d,e,50); SHAR3(e,a,b,c,d,51);
    SHAR3(d,e,a,b,c,52); SHAR3(c,d,e,a,b,53); SHAR3(b,c,d,e,a,54); SHAR3(a,b,c,d,e,55);
    SHAR3(e,a,b,c,d,56); SHAR3(d,e,a,b,c,57); SHAR3(c,d,e,a,b,58); SHAR3(b,c,d,e,a,59);
    SHAR4(a,b,c,d,e,60); SHAR4(e,a,b,c,d,61); SHAR4(d,e,a,b,c,62); SHAR4(c,d,e,a,b,63);
    SHAR4(b,c,d,e,a,64); SHAR4(a,b,c,d,e,65); SHAR4(e,a,b,c,d,66); SHAR4(d,e,a,b,c,67);
    SHAR4(c,d,e,a,b,68); SHAR4(b,c,d,e,a,69); SHAR4(a,b,c,d,e,70); SHAR4(e,a,b,c,d,71);
    SHAR4(d,e,a,b,c,72); SHAR4(c,d,e,a,b,73); SHAR4(b,c,d,e,a,74); SHAR4(a,b,c,d,e,75);
    SHAR4(e,a,b,c,d,76); SHAR4(d,e,a,b,c,77); SHAR4(c,d,e,a,b,78); SHAR4(b,c,d,e,a,79);

    // Add the working vars back into state[]
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;

    // Wipe variables
    a = 0; b = 0; c = 0; d = 0; e = 0;
}

void SHA1_Update(struct SHA1* s, unsigned char* data, unsigned int len)
{
    unsigned int i = 0, j = 0;

    j = (s->m_count[0] >> 3) & 63;
    if((s->m_count[0] += len << 3) < (len << 3)) s->m_count[1]++;
    s->m_count[1] += (len >> 29);

    if((j + len) > 63)
    {
	memcpy(&(s->m_buffer[j]), data, (i = 64 - j));
	SHA1_Transform(s->m_state, s->m_buffer);
	for (; i+63 < len; i += 64)
	{
	    SHA1_Transform(s->m_state, &data[i]);
	}
	j = 0;
    }
    else i = 0;
    memcpy(&(s->m_buffer[j]), &data[i], len - i);
}

void SHA1_Final(struct SHA1* s, unsigned char* digest)
{
    unsigned int i = 0;
    unsigned char finalcount[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };

    for (i = 0; i < 8; i++)
	finalcount[i] = (unsigned char)((s->m_count[(i >= 4 ? 0 : 1)]
					 >> ((3 - (i & 3)) * 8) ) & 255); // Endian independent
    SHA1_Update(s, (unsigned char *)"\200", 1);

    while ((s->m_count[0] & 504) != 448)
	SHA1_Update(s, (unsigned char *)"\0", 1);

    SHA1_Update(s, finalcount, 8); // Cause a SHA1_Transform()

    for (i = 0; i < 20; i++)
    {
	digest[i] = (unsigned char)((s->m_state[i >> 2] >> ((3 - (i & 3)) * 8) ) & 255);
    }
}

/*------------------------------------------------------------------------------
// Fatal error message.
//----------------------------------------------------------------------------*/

void error(const char *msg)
{
    perror(msg);
    exit(1);
}
/*------------------------------------------------------------------------------
// Non-fatal error message
//----------------------------------------------------------------------------*/

void warn(const char *msg)
{
    perror(msg);
}

/*------------------------------------------------------------------------------
// Base64 encode one byte
//----------------------------------------------------------------------------*/

static char encode_base64_char(unsigned char u)
{
    if(u < 26)
    {
	return 'A'+u;
    }
    if(u < 52)
    {
	return 'a'+u-26;
    }
    if(u < 62)
    {
	return '0'+u-52;
    }
    if(u == 62)
    {
	return '+';
    }  
    return '/';
}

/*------------------------------------------------------------------------------
// Base64 encode binary data.
//----------------------------------------------------------------------------*/

void encode_base64(int size, unsigned char *src, unsigned char* dest)
{
    int i;
    char *out, *p;
  
    out=(char*)dest;
    p=out;
    
    for(i=0; i<size; i+=3)
    {
	unsigned char b1=0, b2=0, b3=0, b4=0, b5=0, b6=0, b7=0;
	b1 = src[i];
	if(i+1<size)
	{
	    b2 = src[i+1];
	}
	if(i+2<size)
	{
	    b3 = src[i+2];
	}
	b4 = b1>>2;
	b5 = ((b1&0x3)<<4)|(b2>>4);
	b6 = ((b2&0xf)<<2)|(b3>>6);
	b7 = b3&0x3f;
	*p++= encode_base64_char(b4);
	*p++= encode_base64_char(b5);
	if(i+1<size)
	{
	    *p++= encode_base64_char(b6);
	}
	else
	{
	    *p++= '=';
	}
	if(i+2<size)
	{
	    *p++= encode_base64_char(b7);
	}
	else
	{
	    *(p++)= '=';
	}
    }
    *p = '\0';
}


/*------------------------------------------------------------------------------
// Get allocated copy of parameter from HTTP header.
//----------------------------------------------------------------------------*/

char* parameter(char* start, const char* key)
{
    char* param = NULL;
    char* value;
    int len;
    char* found = strstr(start,key);
    if(found)
    {
	value = found + strlen(key);
	found = (char*) strstr(value,"\r\n");
	if(found)
	{
	    len = found - value;
	    param = (char*) malloc(len + 1);
	    if(param)
	    {
		start = param;
		param[len] = 0;
		while(len > 0)
		{
		    *(start++) = *(value++);
		    len--;
		}
	    }
	}
    }
    return param;
}

/*------------------------------------------------------------------------------
// Read websocket message
//----------------------------------------------------------------------------*/

size_t read_message(int sock, unsigned char* dest, size_t dest_size)
{
    /* We assume for this example client that the entire message
       (only) is read in one go. */

    /* Read as much as possible into dest, translate and then move down */
    int final;
    int opcode;
    int masked;
    unsigned char* start;
    unsigned int len;
    unsigned char mask[4];
    unsigned int mi;
    unsigned int i;
    int n = recv(sock,dest,dest_size-1, 0);
    if(n == 0)
    {
	// Closed connection
	return 0;
    }
    else if (n < 0)
    {
	warn("ERROR reading from socket");
	return 0;
    }

    final = dest[0] >> 7;
    if(!final)
    {
	warn("Multiple frames not supported");
	return 0;
    }
    opcode = dest[0] & 0x0f;
    switch(opcode)
    {
    case 0:
	warn("Continuation frame not handled");
	return 0;
    case 1:
    case 2:
	// Text or Binary - OK
	break;
    case 8:
	warn("Closing connection. Should be sending close back");
	return 0;
    case 9:
    case 10:
	warn("Ping/pong not handled");
	return 0;
    default:
	warn("Opcode not supported");
	return 0;
    }

    // We have a single frame containing a message
    masked = dest[1] >> 7;
    if(!masked)
    {
	warn("Client message should be masked");
	return 0;
    }

    /* Decode the length */
    start = dest+2;
    len = dest[1] & 0x7f;
    if(len == 126)
    {
	len = *(start++);
	len = len * 256 + *(start++);
    }
    else if(len == 127)
    {
	len = *(start++);
	len = len * 256 + *(start++);
	len = len * 256 + *(start++);
	len = len * 256 + *(start++);
    }

    // Now copy mask and shuffle down the payload.
    mask[0] = *(start++);
    mask[1] = *(start++);
    mask[2] = *(start++);
    mask[3] = *(start++);

    mi = 0;
    for(i = 0;i<len;i++)
    {
	*(dest++) = *(start++) ^ mask[mi++];
	if(mi >= 4)
	{
	    mi = 0;
	}
    }

    // Its probably a string.
    *dest = '\0';
    return len;
}

/*------------------------------------------------------------------------------
// Write websocket message
//----------------------------------------------------------------------------*/

int send_message(int sock, const char* payload, size_t payload_length)
{
    // Send message in websocket format.
    unsigned char* start;
    unsigned char buf[BUFLEN];
    int n;

    // This will be a single non-fragmented message.
    buf[0] = 1 + (1 << 7);

    // No masking when we reply, but the length is variable length.
    start = buf+2;
    if(payload_length <= 125)
    {
	buf[1] = (unsigned char) payload_length;
    }
    else if(payload_length <= 65535)
    {
	// 2 length bytes
	buf[1] = 126;
	*(start++) = (payload_length & 0xff00) >> 8;
	*(start++) = (payload_length & 0xff);
    }
    else
    {
	// 4 length bytes
	buf[1] = 126;
	*(start++) = (payload_length & 0xff000000) >> 24;
	*(start++) = (payload_length & 0xff0000) >> 16;
	*(start++) = (payload_length & 0xff00) >> 8;
	*(start++) = (payload_length & 0xff);
    }
    
    memcpy(start,payload,payload_length);
    n = send(sock,buf,payload_length + start - buf,0);
    if (n < 0)
    {
	warn("ERROR writing to socket");
	return FALSE;
    }
    return TRUE;
}

/*------------------------------------------------------------------------------
// Convenience function for sending a zero-terminated string
//----------------------------------------------------------------------------*/

int send_string(int sock, const char* s)
{
    return send_message(sock,s,strlen(s));
}

/*------------------------------------------------------------------------------
// Error-check function called after any ODBC function to abort if it failed
//----------------------------------------------------------------------------*/

void check_success(
    int			ret, 
    SQLSMALLINT		handleType,
    SQLHANDLE		handle,
    const char *	errorMsg)
{
    if (ret != SQL_SUCCESS)
    {
	printf("%s\n", errorMsg);

	if (handle != SQL_NULL_HANDLE)
	{
	    SQLSMALLINT	recNumber = 1;
	    SQLINTEGER	nativeError=0;
	    SQLCHAR	sqlState[6];
	    SQLCHAR	msg[MAX_DIAG_MSG];
	    SQLSMALLINT	actualLen;

	    sqlState[5] = '\0';

	    /* Get the diagnostics for the error */
	    while (SQLGetDiagRec(handleType, handle, recNumber++, &sqlState[0],
			         &nativeError, &msg[0], MAX_DIAG_MSG, &actualLen) == SQL_SUCCESS)
	    {
		printf("ODBC error: %s: %s (%d)\n", sqlState, msg, (int)nativeError);
	    }
	}

	exit(1);
    }
}

/*------------------------------------------------------------------------------
// Send all data for a currency entry
//----------------------------------------------------------------------------*/
int send_currency(int sock, SQLHSTMT hstmt, const char* type)
{
    SQLRETURN		ret;
    SQLDOUBLE		usd;
    SQLLEN		length;
    SQLCHAR		code[MAX_STRING_LENGTH];
    SQLCHAR		name[MAX_STRING_LENGTH];
    SQLCHAR		country[MAX_STRING_LENGTH];
    char buf[4*MAX_STRING_LENGTH];

    /* Retrive the information from the currect row */
    ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column");

    ret = SQLGetData(hstmt, 2, SQL_C_DOUBLE, &usd, 0, &length);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of usd column");

    ret = SQLGetData(hstmt, 3, SQL_C_CHAR, &name, MAX_STRING_LENGTH, &length);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of name column");

    ret = SQLGetData(hstmt, 4, SQL_C_CHAR, &country, MAX_STRING_LENGTH, &length);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of country column");

    /* Format as JSON - in a production environment, encode the values appropriately */
    sprintf(buf,"{ \"type\" : \"%s\", \"code\" : \"%s\", \"usdollar\" : %.02lf, \"name\" : \"%s\", \"country\" : \"%s\"}", type, code, usd, name, country);
    return send_string(sock,buf);
    
}

/*------------------------------------------------------------------------------
// Fetch and send all rows for a statement
//----------------------------------------------------------------------------*/

void fetch_all_data(
		    SQLHSTMT            hstmt,
		    int sock)
{
    SQLRETURN		ret;
    SQLUINTEGER		bookmark;
    SQLLEN		length;

    /* We send one websocket message per row. A more efficient implementation would
       package all rows into a single message and then unpack on the client */
    
    /* Go to the first row in the result set. */
    ret = SQLFetchScroll(hstmt, SQL_FETCH_FIRST, 0);

    while (ret != SQL_NO_DATA)
    {
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row");

	/* If we wanted to store results in our own data structures, then we */
	/* could use the bookmarks as indexes on these structures, since when */
	/* deltas come through we can find the bookmarks of the rows that have */
	/* been added, deleted or altered. The following two lines show how we */
	/* can find the bookmark of the current row, if needed; in this demo,  */
	/* though, we do nothing with the value. */
	ret = SQLGetData(hstmt, 0, SQL_C_BOOKMARK, &bookmark, 0, &length);
	check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of bookmark column");

	/* Send the data on to the client */
	send_currency(sock, hstmt, "initial");

	/* Move onto the next undeleted row. If fetch_all_data is only called */
	/* after the active query is first set up, we will iterate through the */
	/* initial result set. If called at other times, we will iterate through */
	/* the current contents of the result set, skipping rows that hold a */
	/* representation of recently-deleted rows - such rows can only be visited */
	/* once, via their bookmark, and then the space is recovered. */
	ret = SQLFetchScroll(hstmt, SQL_FETCH_NEXT, 0);
    }
}

/*------------------------------------------------------------------------------
// Fetch and send on a single row for a statement
//----------------------------------------------------------------------------*/

int fetch_by_bookmark(
    SQLHSTMT            hstmt,
    int                 sock)
{
    SQLRETURN		ret;  
    SQLCHAR		code[MAX_STRING_LENGTH];
    SQLCHAR		name[MAX_STRING_LENGTH];
    SQLCHAR		country[MAX_STRING_LENGTH];
    SQLDOUBLE		usd;
    SQLLEN		length;
    char                buf[4*MAX_STRING_LENGTH];
    int                 send_result = TRUE;
    switch (RowStatusArray[0])
    {
    case SQL_ROW_ADDED:
	{
	    /* The row is a new one; retrieve the full data and send them. */
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row for insert");

	    send_result = send_currency(sock, hstmt, "insert");
	}
	break;

    case SQL_ROW_UPDATED:
	{
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row for update");

	    {
		/* A value changed - so report it. note that in a 'real' application, we */
		/* would have saved away previously-noted values in one of our own data */
		/* structures, indexed by the bookmark for quick access; here, though, we */
		/* can simply retrieve the data from the result set maintained by */
		/* the client library, and send the message */
		send_result = send_currency(sock, hstmt, "update");
	    }
	}
	break;

    case SQL_ROW_DELETED:
	{
	    /* The row has been deleted - but the space used in the client-side copy */
	    /* of the result set is not recovered until we have had a chance to visit */
	    /* and get back the previously-reported values. */
	    ret = SQLFetchScroll(hstmt, SQL_FETCH_BOOKMARK, 0);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to fetch row for delete");
	    ret = SQLGetData(hstmt, 1, SQL_C_CHAR, &code, MAX_STRING_LENGTH, &length);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get value of code column for deleted row");
	    // JSON format for a delete.
	    sprintf(buf,"{ \"type\" : \"delete\", \"code\" : \"%s\"}", code);
	    send_result = send_string(sock,buf);
	}
	break;
    }
    return send_result;
}

/*------------------------------------------------------------------------------
// Perform active query and handle replies.
//----------------------------------------------------------------------------*/

int get_currencies(int sock,
		   const char* service)
{
    SQLRETURN		ret;
    SQLHENV		henv;
    SQLHDBC		hdbc;
    SQLHSTMT		hstmt;
    int                 ok;
    /* Allocate an environment handle */
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate environment handle");

#if !defined(ODBC_STD)
    /* Set the ODBC version used */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    check_success (ret, SQL_HANDLE_ENV, henv, "Failed to set ODBC version");
#endif

    /* Enable async events */
    ret = SQLSetEnvAttr(henv, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to enable async events");

    /* Allocate a conection handle */
    ret = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to allocate connection handle");

    printf("Connecting to %s...\n", service);

    /* Connect to the database */
    ret = SQLConnect(hdbc, (SQLCHAR *)service, SQL_NTS, 0, SQL_NTS, 0, SQL_NTS);
    if(ret != SQL_SUCCESS)
    {
	printf("Failed to connect to the database\n");
	return FALSE;
    }

    printf("Connected, now launch active query...\n");

    /* Allocate a statement handle */
    ret = SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to allocate a statement handle");

    /* Use dynamic cursor */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_CURSOR_TYPE, (SQLPOINTER)SQL_CURSOR_DYNAMIC, 0);
    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to set dynamic cursor");

    /* Enable async statement events */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE, (SQLPOINTER)SQL_POLY_ASYNC_EVENTS_ENABLE_ON, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to enable async events");

    /* A little trick - set maximum rows to MAX_CURRENCIES */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_MAX_ROWS, (SQLPOINTER)MAX_CURRENCIES, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set maximum rows");

    /* Execute the query */
    ret = SQLExecDirect(hstmt, (SQLCHAR *)"select code,usdollar, country, name from currency", SQL_NTS);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to execute statement");

    /* Set the row status array */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_ROW_STATUS_PTR, RowStatusArray, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set row status ptr");

    /* Set the column status array */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_POLY_COLUMN_STATUS_PTR, ColumnStatusArray, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set column status ptr");

    /* Use bookmarks */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_USE_BOOKMARKS, (SQLPOINTER)SQL_UB_VARIABLE, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set variable-length bookmarks");

    /* Set fetch bookmark pointer */
    ret = SQLSetStmtAttr(hstmt, SQL_ATTR_FETCH_BOOKMARK_PTR, &Bookmark, 0);
    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to set fetch bookmark ptr");

    /* Fetch and display initial result set */
    fetch_all_data(hstmt,sock);
    printf("Delta complete - success.\n\n");

    /* Loop handling events */
    for (;;)
    {
	SQLUSMALLINT	functionId;
	SQLSMALLINT	handleType;
	SQLHANDLE	handle;

	/* Get the next event */
	ok = TRUE;
	while (ok && SQLGetAsyncEvent(henv, &functionId, &handleType, &handle) == SQL_SUCCESS)
	{
	    switch (functionId)
	    {
	    case SQL_API_SQLDISCONNECT:
		/* The database connection is going away */
		ok = FALSE;
		break;

	    case SQL_API_SQLFETCH:
		/* Data has changed - fetch and display modified result set */
		while (SQLGetAsyncStmtEvent(hstmt) == SQL_SUCCESS)
		{
		    if(!fetch_by_bookmark(hstmt,sock))
		    {
			// Comms has failed so we stop handling client.
			ok = FALSE;
			break;
		    }
		}

		printf("Delta complete - success.\n\n");
		break;

	    case SQL_API_SQLGETCONNECTATTR:
		/* Connection attribute has changed */
		{
		    SQLCHAR name[256];
		    SQLUINTEGER mode;

		    /* Get the service name being used */
		    ret = SQLGetConnectAttr(hdbc, SQL_ATTR_POLY_CONNECTION_NAME, (SQLPOINTER)name, sizeof(name), 0);
		    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get connection name");


		    /* If name is blank, connection is reconnecting */
		    if (name[0] == '\0')
		    {
			printf("Reconnecting\n");
			break;
		    }

		    /* Get the FT mode */
		    ret = SQLGetConnectAttr(hdbc, SQL_ATTR_POLY_FT_MODE, &mode, 0, 0);
		    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to get FT mode");

		    printf("Connection: %s, mode: %d\n", name, (int)mode);
		}
		break;

	    default:
		fprintf(stderr, "Event %d not handled\n", functionId);
		return TRUE;
	    }
	}

	if(!ok)
	{
	    /* The connection is closing so tidy up the database end */
	    /* Free the statement handle */
	    ret = SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	    check_success(ret, SQL_HANDLE_STMT, hstmt, "Failed to free statement handle");

	    /* Disconnect from database */
	    ret = SQLDisconnect(hdbc);
	    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to disconnect from the database");

	    /* Free the connection handle */
	    ret = SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
	    check_success(ret, SQL_HANDLE_DBC, hdbc, "Failed to free connection handle");

	    /* Free the environment handle */
	    ret = SQLFreeHandle(SQL_HANDLE_ENV, henv);
	    check_success(ret, SQL_HANDLE_ENV, henv, "Failed to free environment handle");

	    return TRUE;

	}
	/* Generic function to wait for a Polyhedra message */
	/* This can be replaced by OS specific main loop */
	ret = SQLHandleMsg(henv);
	check_success(ret, SQL_HANDLE_ENV, henv, "Failed to handle message");
    }

    return TRUE;
}

/*------------------------------------------------------------------------------
// Handle websocket protocol and perform requested work.
//----------------------------------------------------------------------------*/

void handle_connection(int sock, const char* service)
{
    // This implementation of the Websocket protocol supports the minimum features of
    // version 8 and 13 that will support the application. In particular keepalives
    // and message fragmentation are not implemented.
    // http://tools.ietf.org/html/draft-ietf-hybi-thewebsocketprotocol-17

    char buffer[BUFLEN];
    int n;
    char* version = NULL;
    char* key = NULL;
    struct SHA1 ctx;
    unsigned char digest[20];
    size_t acceptlen = 0;
    char acceptvalue[50];
    size_t length;

    n = recv(sock,buffer,BUFLEN-1,0);
    if (n == 0)
    {
	return;
    }
    else if (n < 0)
    {
	warn("ERROR reading initial data from Websocket socket");
	return;
    }
    buffer[n] = '\0';

    key = parameter(buffer,"Sec-WebSocket-Key: ");
    if(!key)
    {
	warn("No Sec-WebSocket-Key");
	return;
    }
     
    version = parameter(buffer,"Sec-WebSocket-Version: ");
    if(!version)
    {
	free(key);
	warn("No Sec-WebSocket-version");
	return;
    }

    if(strcmp(version,"8") && strcmp(version,"13"))
    {
	warn("This server understands version 8 or 13 of the Websocket protocol");
	free(key);
	free(version);
	return;
    }
    free(version);

#define GUID "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    /* Constructing response */
    SHA1_Init(&ctx);
    SHA1_Update(&ctx,(unsigned char*) key,strlen(key));
    SHA1_Update(&ctx,(unsigned char*) GUID,strlen(GUID));
    SHA1_Final(&ctx,digest);
    free(key);

    encode_base64(20,digest,(unsigned char*) acceptvalue);

    /* Reuse buffer */
    strcpy(buffer, "HTTP/1.1 101 Switching Protocols\r\n");
    strcat(buffer, "Upgrade: websocket\r\n");
    strcat(buffer, "Connection: Upgrade\r\n");
    strcat(buffer, "Sec-WebSocket-Accept: ");
    strcat(buffer, acceptvalue);
    strcat(buffer, "\r\n");
    strcat(buffer, "\r\n");
     
    n = send(sock,buffer,strlen(buffer),0);
    if (n < 0)
    {
	warn("ERROR writing Websocket handshake to socket");
	return;
    }

    // This server responds to a message with "currency" only.
    // Add in other request types here.

    length = read_message(sock, buffer,BUFLEN);
    if(length == 0)
    {
	// Connection closed
    }
    else if(length == 8 && !strncmp("currency",buffer,8))
    {
	// Respond to correct request until either connection closes.
	if(!get_currencies(sock,service))
	{
	    send_string(sock,"Could not connect to the database");
	}
    }
    else
    {
	send_string(sock,"This server responds to the 'currency' request only");
    }
}

/*------------------------------------------------------------------------------
// Set up listening socket and handle connections.
//----------------------------------------------------------------------------*/

#if defined(EMBEDDED)
int poly_main(int argc, char *argv[])
#else
int main(
#endif
{
    int on = 1;
    const char * service = "8001";
    int portno  = 3400;
    int sockfd, newsockfd;
    int n;
    int childpid;
    int dummy;
    socklen_t clilen;
    struct sockaddr_in serv_addr, cli_addr;

    /* Check we have the correct number of arguments */
    if (argc > 3)
    {
	fprintf(stderr, "usage: %s [<websocket port> [<data service>]]\n", argv[0]);
	return 1;
    }

    if (argc > 1)
    {
	portno = atoi(argv[1]);
    }

    /* Check we have a service argument */
    if (argc > 2)
    {
	service = argv[2];
    }
     
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
	error("ERROR opening socket");
    memset((char *) &serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    setsockopt(sockfd,SOL_SOCKET,SO_REUSEADDR,(char*) &on,sizeof(on));
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
	     sizeof(serv_addr)) < 0)
    {
	error("ERROR on binding");
    }

    printf("Polyhedra Websocket Server listening on port %d connecting to RTRDB on %s\n",
	   portno, service);
    listen(sockfd,5);
    while(1)
    {
	clilen = sizeof(cli_addr);
	newsockfd = accept(sockfd, 
			   (struct sockaddr *) &cli_addr, 
			   &clilen);
	if (newsockfd < 0) 
	    error("ERROR on accept");

#ifdef WIN32
	// The Windows version handles only one simultaneous connection.
	handle_connection(newsockfd, service);
	closesocket(newsockfd);
#else
	// The POSIX version forks off a process for each connection and so
	// can handle multiple simultaneous connections.
	switch(childpid = fork())
	{
	case -1:
	    error("Failed to fork");
	   
	case 0:
	    // In child.
	    close(sockfd);
	    handle_connection(newsockfd, service);
	    exit(0);

	default:
	    // Still in server
	    close(newsockfd);
	}

	// Tidy up any zombie children
	while(waitpid(-1, &dummy, WNOHANG) > 0);
#endif
    }
}

/*------------------------------------------------------------------------------
// End of file
//----------------------------------------------------------------------------*/

