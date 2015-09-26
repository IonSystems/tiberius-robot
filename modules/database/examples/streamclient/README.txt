-------------------------------------------------------------------------------
--                       P O L Y H E D R A
--                   Copyright (C) 2006-2014 by Enea Software AB
-------------------------------------------------------------------------------
--    Filename      : README.txt
--    Description   : The Historian Streaming Example Client.
--
--    CVSID         : $Id: README.txt,v 1.11 2014/01/06 14:49:02 andy Exp $
--
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------

OVERVIEW
--------

This directory contains a simple historian streaming client. The client
illustrates how to format a request, send it, retrieve a response and
interpret the response.

USAGE
-----

The client uses command line arguments to connect to an RTRDB and execute
one or more requests, e.g.

streamclient 10000 status 1

Send stream status request for stream 1 to port 10000.
	
streamclient 10000 fetch 1 27

Send block fetch request for block 27 on stream 1 to port 20000.

streamclient 10000 stream 1 1000 20000 25

Send stream request for stream 1 with latency 1000ms and buffer size
20000 to port 10000  with the highest known object Id of 25.

streamclient 10000 status 1 fetch 1 27

Send stream status request for stream 1, followed by fetch request for
block 27 to port 10000.


BUILD INSTRUCTIONS
------------------

The example client has been built on the following platforms:

Linux:

gcc -o streamclient streamclient.c -I ../../include ../../linux/i386/gcc/lib/libpolyhiststream.a

Solaris:

gcc -o streamclient streamclient.c -I ../../include ../../solaris/i386/gcc/lib/libpolyhiststream.a -lsocket

Win32 (MSVC):

cl -c -DWIN32 -I ..\..\include /Fostreamclient.o -MT streamclient.c
link -subsystem:console streamclient.o ..\..\win32\i386\msvc\lib\polyhiststream.lib ws2_32.lib

(note that the Windows API library is a DLL, so will need to be in the path)

-------------------------------------------------------------------------------
--                        E n d   o f   f i l e
-------------------------------------------------------------------------------
