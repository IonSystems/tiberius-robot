/*
//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2015 by Enea Software AB
//		All Rights Reserved
// Author:	
// Description:	
//------------------------------------------------------------------------------
*/

/*
-------------------------------------------------------------------------------
-- NOTE: this is ILLUSTRATIVE CODE, provided on an 'as is' basis to help
-- demonstrate one or more features of the Polyhedra product.
-- It may well need adaption for use in a live installation, and
-- Enea Software AB and its agents and distributors do not warrant this code.
-------------------------------------------------------------------------------
*/

/* ========================================================================= */
/*                     * * *   W A R N I N G !   * * *                       */
/* ========================================================================= */
/* (this file contains the sample arbitration code given in the appendix     */
/* to the Polyhedra evaluation guide; please read that appendix before using */
/* or adapting this code, as it describes the assumptions and limitations    */
/* implicit in this code.)                                                   */
/* ========================================================================= */

#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

/* ------------------------------------------------------------------------- */
/*                      C h e c k I f A c t i v e                            */
/*                      -------------------------                            */
/* define a function that will return information about the board mode;      */
/* in this simple example code, we check whether the last character of the   */
/* string supplied by the rtrdb in its heartbeat matches the global constant */
/* board_mode. In a REAL implementation, we would call a system function to  */
/* determine the mode, ignoring the string supplied by the rtrdb.            */
/*                                                                           */
/*           REPLACE THIS DEFINITION on a real implementation.               */
/* ------------------------------------------------------------------------- */

unsigned char board_mode;

int CheckIfMaster (unsigned char c)
{ return (c == board_mode);
}

/* ------------------------------------------------------------------------- */
/*                           s t r e a m h a n d l e                         */
/*                           -----------------------                         */
/* define a structure for recording connection info, and a function to send  */
/* a message to a nominated connection to tell it what mode it should be in. */
/* ------------------------------------------------------------------------- */

struct streamhandle
{ int                  id;
  char                 letter;
  int                  tnum;
  struct streamhandle* next; 
};

void BuildAndSendMessage (struct streamhandle* sh)
{
  unsigned char buf[13];

  buf[0] = 'A';

  /* mode */

  if (CheckIfMaster (sh->letter))
    { buf[1] = 1;
      buf[2] = 0;
      buf[3] = 0;
      buf[4] = 0;
    }
  else
    { buf[1] = 2;
      buf[2] = 0;
      buf[3] = 0;
      buf[4] = 0;
    }

  /* transaction number - let's make byte ordering explicit! */

  buf[5] = (sh->tnum      ) & 255;
  buf[6] = (sh->tnum >>  8) & 255;
  buf[7] = (sh->tnum >> 16) & 255;
  buf[8] = (sh->tnum >> 24)      ;

  /* heartbeat 
     here, 1 second (1,000,000 microseconds, hex 0F4240)
  */

  buf[ 9] = 0x40;
  buf[10] = 0x42;
  buf[11] = 0x0F;
  buf[12] = 0x00;
    
  write(sh->id, buf, 13);
}

/* ------------------------------------------------------------------------- */
/*                              m a i n                                      */
/*                              -------                                      */
/* on embedded platforms, do NOT define main in this program!                */
/* ------------------------------------------------------------------------- */

#ifndef VXWORKS
int main (int argc, char* argv [])
{ return arbitrator (argc, argv);
}
#endif

/* ------------------------------------------------------------------------- */
/*                          a r b i t r a t o r                              */
/*                          -------------------                              */
/* define the main work routine of this program, which prepares to listen    */
/* for connections, and then waits for connection attempts, disconnections   */
/* and messages.                                                             */
/* ------------------------------------------------------------------------- */

int arbitrator (int argc, char* argv [])
{
  int                  s;           /* connection socket  */
  short                p;           /* port number to use */
  struct sockaddr_in   sa;
  struct servent       *sp;
  struct hostent       *hp;
  fd_set               rd_fds;
  struct streamhandle* streamchain = 0;

  if (argc != 3)
    { fprintf (stderr, 
               "please give %s two arguments, a port and 0/1.\n", 
               argv[0]
              );
      return 10;
    }

  board_mode = (argv[2])[0];

  /* find out info about the socket I am supposed to claim. */

  if ((sp = getservbyname(argv[1],"tcp")) == NULL)
    { p = htons (atoi (argv[1]));
      if (p == 0)
        { fprintf(stderr, "service '%s' not registered on this machine\n", 
                  argv[1]);
          return 10;
        }
    }
  else
    { p = sp->s_port;
    }

  /* port OK, so claim it and listen for connections. */

  if ((hp = gethostbyname("127.0.0.1")) == NULL)
    { fprintf(stderr, "can't get local host info\n");
      return 10;
    }
  sa.sin_addr.s_addr = INADDR_ANY;
  sa.sin_port        = p;
  sa.sin_family      = hp->h_addrtype;
    
  if ((s = socket(hp->h_addrtype, SOCK_STREAM, 0)) < 0)
    {       /* failed to create socket. Give up. */
      perror("Socket");
      return 10;
    }
  if (bind(s, &sa, sizeof sa) < 0)
    { /* failed to bind the port to the socket; give up, leaving O/S to
         tidy up the socket (lazy, but OK on UNIX, Windows).
      */
      perror("Bind");
      return 10;
    }

  listen (s, 5);

  /*          -----------------
              M A I N   L O O P
              -----------------
     reacting both to connection attempts and
     also to traffic over open connections.
  */

  while (1)
    {
      int                  n;
      char*                c;
      int                  dbg = 0;
      struct sockaddr_in   isa;
      int                  i = sizeof isa;
      unsigned char        buf[1000];
      struct streamhandle* sh = streamchain;

      /*            -------
                    W A I T
                    -------
         wait for something to happen; on return 
         from the select, rd_fds will indicate 
         which stream(s) something happened on.
      */

      FD_ZERO(&rd_fds);
      FD_SET(s, &rd_fds);
      
      while (sh != 0)
        { FD_SET(sh->id, &rd_fds);
          sh = sh->next;
        }
      n = select(FD_SETSIZE, &rd_fds, NULL, NULL, NULL);

      /* is there an incoming connection or message (or is a stream closing)? */

      sh = streamchain;
      while (sh != 0)
        { if (FD_ISSET(sh->id, &rd_fds))
            { n = read(sh->id, buf, 1000);
              if (n <= 0)
                { /* we were told there was something on this stream - but it 
                     is empty, so it must have been closed by the far end, 
                     or broken. Close our end of the connection.
                  */
                      
                  close(sh->id);
                  if (streamchain==sh)
                    streamchain = sh->next;
                  else
                    { /* find the streamhandle that points at sh, and 
                         make its 'next' pointer skip over sh
                      */
                      struct streamhandle* sh2 = streamchain;
                      while (sh2->next != sh)
                        sh2 = sh2->next;
                      sh2->next = sh->next;
                    }
                  free (sh);
                  break;
                }
              else if (buf[0] == 'J')
                { unsigned char* str = buf+9;
                  sh->letter = str[strlen(str)-1];
                  sh->tnum   = ((buf[8] << 24) |
                                (buf[7] << 16) | 
                                (buf[6] <<  8) | 
                                (buf[5]      ));
                  
                  /* build up the response to the RTRDB, calling the
                     function CheckIfMaster to determine if the
                     rtrdb is to be told master or standby.
                  */

                  BuildAndSendMessage (sh);
                }
              else
                { /* to assist debugging and to allow mode swapping,
                     allow for a connection asking me to swap mode.
                     Thus one can connect in via, say telnet (by a 
                     command such as 'telnet localhost 7200') and
                     the first letter of a line is significant
                  */
                  struct streamhandle* sh2 = streamchain;
                  board_mode =  buf[0];

                  /* tell all RTRDBS about the changed mode */

                  while (sh2 != 0)
                    { if (sh2->letter != 0)
                        BuildAndSendMessage (sh2);
                      sh2 = sh2->next;
                    }
                }
            }

          /* move onto the next streamhandle, to check for input */
          sh = sh->next;
        }
      
      /* is someone trying to connect? */

      if (FD_ISSET(s, &rd_fds))
        { int v;
          if ((v = accept(s, &isa, &i)) < 0)
            { perror("Accept");
              return 10;
            }
          sh = (struct streamhandle *) malloc (sizeof (struct streamhandle));
          sh->id      = v;
          sh->letter  = 0;
          sh->next    = streamchain;
          streamchain = sh;
        }
    }
}

