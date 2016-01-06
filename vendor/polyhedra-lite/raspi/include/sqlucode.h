/*-+-----------------------------------------------------------------------+-//
//									     //
//			      P O L Y H E D R A				     //
//									     //
//                Copyright (C) 1994-2015 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//---------------------------------------------------------------------------*/

#ifndef __SQLUCODE
#define __SQLUCODE

#ifdef __cplusplus
extern "C" { /* Assume C declarations for C++ */
#endif /* __cplusplus */

#ifndef __SQLEXT
#include "sqlext.h"
#endif

#define SQL_WCHAR		(-8)
#define SQL_WVARCHAR		(-9)
#define SQL_WLONGVARCHAR	(-10)
#define SQL_C_WCHAR		SQL_WCHAR

#ifdef UNICODE
#define SQL_C_TCHAR		SQL_C_WCHAR
#else
#define SQL_C_TCHAR		SQL_C_CHAR
#endif 

#define SQL_SQLSTATE_SIZEW	10	/* size of SQLSTATE for unicode */

#ifdef __cplusplus
} /* End of extern "C" { */
#endif /* __cplusplus */

#endif /* #ifndef __SQLUCODE */

/*-+----------------------------- End of File -----------------------------+-//
//									     //
//                Copyright (C) 1994-2015 by Enea Software AB                //
//			     All Rights Reserved			     //
//									     //
//-+-----------------------------------------------------------------------+-*/
