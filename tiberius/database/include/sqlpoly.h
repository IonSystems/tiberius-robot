/*-+-----------------------------------------------------------------------+-//
//									     //
//			      P O L Y H E D R A				     //
//									     //
//                Copyright (C) 1994-2014 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------*/

#ifndef __SQLPOLY
#define __SQLPOLY

#ifdef __cplusplus
extern "C" { /* Assume C declarations for C++ */
#endif /* __cplusplus */

/* Polyhedra specific attributes */
#define SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE	20000
#define SQL_ATTR_POLY_FT_ENABLE			20001
#define SQL_ATTR_POLY_FT_HEALTHCHECK_INTERVAL	20002
#define SQL_ATTR_POLY_FT_HEALTHCHECK_TIMEOUT	20003
#define SQL_ATTR_POLY_FT_KEEP_COPY		20004
#define SQL_ATTR_POLY_FT_MAP_ROWIDS		20005
#define SQL_ATTR_POLY_FT_RECONNECTION_INTERVAL	20006
#define SQL_ATTR_POLY_FT_RECONNECTION_RETRIES	20007
#define SQL_ATTR_POLY_FT_RECONNECTION_TIMEOUT	20008
#define SQL_ATTR_POLY_FT_REEXECUTE_TRANSACTIONS	20009
#define SQL_ATTR_POLY_FT_SAFE_COMMIT_ENABLE	20010
#define SQL_ATTR_POLY_COLUMN_STATUS_PTR		20011
#define SQL_ATTR_POLY_PRIMARY			20012
#define SQL_DESC_POLY_PRIMARY			SQL_ATTR_POLY_PRIMARY
#define SQL_ATTR_POLY_ALLOCATE_BOOKMARK		20013
#define SQL_ATTR_POLY_MINIMUM_DELTA_INTERVAL	20014
#define SQL_ATTR_POLY_EXTRA			20015
#define SQL_ATTR_POLY_EVENT_TIMEOUT		20017
#define SQL_ATTR_POLY_FT_MODE			20018
#define SQL_ATTR_POLY_CONNECTION_NAME		20019
#define SQL_ATTR_POLY_CHARSET			20020
#define SQL_ATTR_POLY_MEMORY_HWM		20021 /* Unsupported - NO NOT USE */
#define SQL_ATTR_POLY_LINX_ENDPOINT             20022
#define SQL_ATTR_POLY_EXCLUDE_HIDDEN		20023 /* Only supported for QP */
#define SQL_ATTR_POLY_BYTES_RECEIVED		20024 /* Unsupported - NO NOT USE */

#if defined(WIN32)
#define SQL_ATTR_POLY_HWND			20016
#define WM_POLY_ASYNCH_EVENT			WM_USER + 2
#endif

/* Values for SQL_ATTR_POLY_ASYNC_EVENTS_ENABLE */
#define SQL_POLY_ASYNC_EVENTS_ENABLE_OFF	0
#define SQL_POLY_ASYNC_EVENTS_ENABLE_ON		1

/* Values for SQL_ATTR_POLY_FT_ENABLE attribute */
#define SQL_POLY_FT_ENABLE_OFF			0
#define SQL_POLY_FT_ENABLE_ON			1

/* Values for SQL_ATTR_POLY_FT_KEEP_COPY attribute */
#define	SQL_POLY_FT_KEEP_COPY_OFF		0
#define	SQL_POLY_FT_KEEP_COPY_ON		1

/* Values for SQL_ATTR_POLY_FT_MAP_ROWIDS attribute */
#define SQL_POLY_FT_MAP_ROWIDS_OFF		0
#define SQL_POLY_FT_MAP_ROWIDS_ON		1

/* Value for SQL_ATTR_POLY_FT_MODE attribute */
#define SQL_POLY_FT_MODE_STANDALONE		0
#define SQL_POLY_FT_MODE_MASTER			1
#define SQL_POLY_FT_MODE_STANDBY		2
#define SQL_POLY_FT_MODE_REPLICA		3

/* Values for SQL_ATTR_POLY_FT_REEXECUTE_TRANSACTIONS attribute */
#define SQL_POLY_FT_REEXECUTE_TRANSACTIONS_OFF	0
#define SQL_POLY_FT_REEXECUTE_TRANSACTIONS_ON	1

/* Values for SQL_ATTR_POLY_FT_SAFE_COMMIT_ENABLE attribute */
#define SQL_POLY_FT_SAFE_COMMIT_ENABLE_OFF	0
#define SQL_POLY_FT_SAFE_COMMIT_ENABLE_ON	1

/* Values for SQL_ATTR_POLY_PRIMARY attribute */
#define SQL_ATTR_POLY_PRIMARY_UNKNOWN		0
#define SQL_ATTR_POLY_IS_PRIMARY		1
#define SQL_ATTR_POLY_NOT_PRIMARY		2

/* Values for additional row status (events) */
#define SQL_ROWS_REORDERED			100

/* Values for column status array */
#define SQL_COLUMN_UNCHANGED			SQL_ROW_SUCCESS
#define SQL_COLUMN_UPDATED			SQL_ROW_UPDATED

/* Extensions for SQLBulkOperations */
#define SQL_ADD_BY_BOOKMARK			10

/* Values for SQL_ATTR_POLY_CHARSET attribute */
#define SQL_POLY_CHARSET_ASCII			0
#define SQL_POLY_CHARSET_UTF8			1

/* Values for SQL_ATTR_POLY_EXCLUDE_HIDDEN attribute */
#define SQL_POLY_EXCLUDE_HIDDEN_OFF		0
#define SQL_POLY_EXCLUDE_HIDDEN_ON		1

/* Polyhedra specific functions */
SQLRETURN SQL_API SQLHandleMsg(
    SQLHENV		environmentHandle);

#if defined(OSE) || defined(OSE_DELTA)
union SIGNAL; /* Forward declaration. */

SQLRETURN SQL_API SQLHandleOSESignal(
    SQLHENV		environmentHandle,
    union SIGNAL **	sigPtrPtr);
#endif

union LINX_SIGNAL; /* Forward declaration. */

SQLRETURN SQL_API SQLHandleLINXSignal(
    SQLHENV		environmentHandle,
    union LINX_SIGNAL **sigPtrPtr);

SQLRETURN SQL_API SQLGetAsyncEvent(
    SQLHENV		environmentHandle,
    SQLUSMALLINT *	functionIdPtr,
    SQLSMALLINT *	handleTypePtr,
    SQLHANDLE *		handlePtr);

SQLRETURN SQL_API SQLGetAsyncStmtEvent(
    SQLHSTMT		statementHandle);

SQLRETURN SQL_API SQLEncryptPassword(
    SQLHDBC		connectionHandle,
    SQLCHAR *		password,
    SQLINTEGER		passwordLength,
    SQLCHAR *		bufferPtr,
    SQLINTEGER		bufferLength,
    SQLINTEGER *	bufferLengthPtr);

#ifdef __cplusplus
} /* End of extern "C" { */
#endif /* __cplusplus */
#endif /* #ifndef __SQLPOLY */

/*-+----------------------------- End of File -----------------------------+-//
//									     //
//                Copyright (C) 1994-2014 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//-+-----------------------------------------------------------------------+-*/
