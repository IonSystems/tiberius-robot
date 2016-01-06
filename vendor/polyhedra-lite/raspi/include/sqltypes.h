/*-+-----------------------------------------------------------------------+-//
//									     //
//			      P O L Y H E D R A				     //
//									     //
//                Copyright (C) 1994-2015 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------*/

#ifndef __SQLTYPES
#define __SQLTYPES

#ifdef __cplusplus
extern "C" { /* Assume C declarations for C++ */
#endif /* __cplusplus */

#if defined(WIN32) && !defined(OSE_DELTA)
#define SQL_API  __stdcall
#else
#define SQL_API
#endif

/* API declaration data types */
typedef unsigned char		SQLCHAR;
typedef signed char		SQLSCHAR;
typedef unsigned char		SQLDATE;
typedef unsigned char		SQLDECIMAL;
typedef double			SQLDOUBLE;
typedef double			SQLFLOAT;
#if defined(SIXTYFOURBIT)
typedef int			SQLINTEGER;
typedef unsigned int		SQLUINTEGER;
#if defined(WIN32)
typedef unsigned long long	SQLSETPOSIROW;
#else
typedef unsigned long		SQLSETPOSIROW;
#endif
#else
typedef long			SQLINTEGER;
typedef unsigned long		SQLUINTEGER;
typedef unsigned short		SQLSETPOSIROW;
#endif
#if defined(SIXTYFOURBIT) && defined(WIN32)
typedef long long		SQLLEN;
typedef unsigned long long	SQLULEN;
#else
typedef long			SQLLEN;
typedef unsigned long		SQLULEN;
#endif
typedef unsigned char		SQLNUMERIC;
typedef void *			SQLPOINTER;
typedef float			SQLREAL;
typedef short			SQLSMALLINT;
typedef unsigned short		SQLUSMALLINT;
typedef unsigned char		SQLTIME;
typedef unsigned char		SQLTIMESTAMP;
typedef unsigned char		SQLVARCHAR;

/* function return type */
typedef SQLSMALLINT		SQLRETURN;

/* generic data structures */
typedef void *			SQLHANDLE;
typedef SQLHANDLE		SQLHENV;
typedef SQLHANDLE		SQLHDBC;
typedef SQLHANDLE		SQLHSTMT;
typedef SQLHANDLE		SQLHDESC;

/* SQL portable types for C */
#if !defined(VXWORKS)
typedef unsigned char		UCHAR;
#endif
typedef signed char		SCHAR;
typedef long int		SDWORD;
typedef short int		SWORD;
typedef unsigned long int	UDWORD;
typedef unsigned short int	UWORD;

typedef signed long		SLONG;
typedef signed short		SSHORT;
#if !defined(VXWORKS)
typedef unsigned long		ULONG;
typedef unsigned short		USHORT;
#endif
typedef double			SDOUBLE;
typedef double			LDOUBLE; 
typedef float			SFLOAT;

typedef void *			PTR;

typedef void *			HENV;
typedef void *			HDBC;
typedef void *			HSTMT;

typedef signed short		RETCODE;

#if defined(WIN32) && !defined(OSE_DELTA)
typedef HWND			SQLHWND;
#elif defined(UNIX)
typedef Widget			SQLHWND;
#else
/* placehold for future O/S GUI window handle definition */
typedef SQLPOINTER		SQLHWND;
#endif

#ifndef	__SQLDATE
#define	__SQLDATE
/* transfer types for DATE, TIME, TIMESTAMP */
typedef struct tagDATE_STRUCT
{
    SQLSMALLINT		year;
    SQLUSMALLINT	month;
    SQLUSMALLINT	day;
} SQL_DATE_STRUCT;

typedef struct tagTIME_STRUCT
{
    SQLUSMALLINT	hour;
    SQLUSMALLINT	minute;
    SQLUSMALLINT	second;
} SQL_TIME_STRUCT;

typedef struct tagTIMESTAMP_STRUCT
{
    SQLSMALLINT		year;
    SQLUSMALLINT	month;
    SQLUSMALLINT	day;
    SQLUSMALLINT	hour;
    SQLUSMALLINT	minute;
    SQLUSMALLINT	second;
    SQLUINTEGER		fraction;
} SQL_TIMESTAMP_STRUCT;

/*
 * enumerations for DATETIME_INTERVAL_SUBCODE values for interval data types
 * these values are from SQL-92
 */

typedef enum 
{
    SQL_IS_YEAR			= 1,
    SQL_IS_MONTH		= 2,
    SQL_IS_DAY			= 3,
    SQL_IS_HOUR			= 4,
    SQL_IS_MINUTE		= 5,
    SQL_IS_SECOND		= 6,
    SQL_IS_YEAR_TO_MONTH	= 7,
    SQL_IS_DAY_TO_HOUR		= 8,
    SQL_IS_DAY_TO_MINUTE	= 9,
    SQL_IS_DAY_TO_SECOND	= 10,
    SQL_IS_HOUR_TO_MINUTE	= 11,
    SQL_IS_HOUR_TO_SECOND	= 12,
    SQL_IS_MINUTE_TO_SECOND	= 13
} SQLINTERVAL;

typedef struct tagSQL_YEAR_MONTH
{
    SQLUINTEGER		year;
    SQLUINTEGER		month;
} SQL_YEAR_MONTH_STRUCT;

typedef struct tagSQL_DAY_SECOND
{
    SQLUINTEGER		day;
    SQLUINTEGER		hour;
    SQLUINTEGER		minute;
    SQLUINTEGER		second;
    SQLUINTEGER		fraction;
} SQL_DAY_SECOND_STRUCT;

typedef struct tagSQL_INTERVAL_STRUCT
{
    SQLINTERVAL		interval_type;
    SQLSMALLINT		interval_sign;
    union
    {
	SQL_YEAR_MONTH_STRUCT	year_month;
	SQL_DAY_SECOND_STRUCT	day_second;
    } intval;
} SQL_INTERVAL_STRUCT;

#endif/* __SQLDATE */

/* the ODBC C types for SQL_C_SBIGINT and SQL_C_UBIGINT */
#ifndef ODBCINT64
#define ODBCINT64	long long
#endif

/* If using other compilers, define ODBCINT64 to the 
	approriate 64 bit integer type */
#ifdef ODBCINT64
typedef ODBCINT64		SQLBIGINT;
typedef unsigned ODBCINT64	SQLUBIGINT;
#endif

/* internal representation of numeric data type */
#define SQL_MAX_NUMERIC_LEN		16

typedef struct tagSQL_NUMERIC_STRUCT
{
    SQLCHAR		precision;
    SQLSCHAR		scale;
    SQLCHAR		sign; /* 1 if positive, 0 if negative */
    SQLCHAR		val[SQL_MAX_NUMERIC_LEN];
} SQL_NUMERIC_STRUCT;

#ifdef NEVER
#ifdef GUID_DEFINED
typedef GUID		SQLGUID;
#else
/* size is 16 */
typedef struct  tagSQLGUID
{
    DWORD		Data1;
    WORD		Data2;
    WORD		Data3;
    BYTE		Data4[ 8 ];
} SQLGUID;
#endif  /* GUID_DEFINED */
#endif

typedef SQLULEN			BOOKMARK;

#if defined(UNIXODBC_SQLWCHAR)
/* unixODBC defines a 2 byte wide char to be compatible with Windows */
typedef unsigned short		SQLWCHAR;

#else

#if defined(_WCHAR_T) || defined(_WCHAR_T_DEFINED)
typedef wchar_t SQLWCHAR;
#elif (defined(WIN32) && !defined(OSE_DELTA)) || defined(VXWORKS) || (defined(OSE_DELTA) && defined(__arm__))
typedef unsigned short		SQLWCHAR;
#else
typedef unsigned int		SQLWCHAR;
#endif

#endif

#ifdef UNICODE
typedef SQLWCHAR		SQLTCHAR;
#else
typedef SQLCHAR			SQLTCHAR;
#endif  /* UNICODE */

#ifdef __cplusplus
} /* End of extern "C" { */
#endif /* __cplusplus */
#endif /* #ifndef __SQLTYPES */

/*-+----------------------------- End of File -----------------------------+-//
//									     //
//                Copyright (C) 1994-2015 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//-+-----------------------------------------------------------------------+-*/
