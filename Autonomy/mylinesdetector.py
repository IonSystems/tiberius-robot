#!/usr/bin/python

import cv2
import csv
import cmath
import numpy as np

#a function to calculate a distance between two dots
def dist(x1,y1,x2,y2):
    dist = cmath.sqrt(pow((x2-x1),2) + pow((y2-y1),2))
    return dist.real


#def linesdet(gap, curv):
dots = []
lines = []
lines.append([0,0,0,0]) #creates an empty line
lncnt = 0
dtcnt = 0
gap = 20.0
curvrear = 4.0
curvfront = 40.0


#converts lidar data from polar to rectangular and stores in 'dots' array
with open('/home/pi/Desktop/test.csv', 'rb') as lidar:
    readldr = csv.reader(lidar)
    for row in readldr:
        r = row[1]
        ph = row[0]
        z = cmath.rect(float(r)/10,float(ph)/180*cmath.pi)
        dots.append([z.real,z.imag])
        
#loops through a list of dots and groups them into lines based on 'gap' and 'curv' parameters
for x in xrange(0,362):
    if lines[lncnt][0] == 0: #if a current row in 'lines' is empty
        if dist(dots[dtcnt][0],dots[dtcnt][1],dots[dtcnt+1][0],dots[dtcnt+1][1])<gap:
            #starts a new line with a fixed start which is the current dot and end is the next dot,
            #which may or may not be changed later based on the next dots (not)being in the same line
            lines[lncnt][0] = dots[dtcnt][0]
            lines[lncnt][1] = dots[dtcnt][1]
            lines[lncnt][2] = dots[dtcnt+1][0]
            lines[lncnt][3] = dots[dtcnt+1][1]
            dtcnt = dtcnt+1
        else:
            #creates a line, which consists of a single dot
            #creates a new empty row in 'lines'
            lines[lncnt][0] = dots[dtcnt][0]
            lines[lncnt][1] = dots[dtcnt][1]
            lines[lncnt][2] = dots[dtcnt][0]
            lines[lncnt][3] = dots[dtcnt][1]
            lines.append([0,0,0,0])
            lncnt = lncnt+1
            dtcnt = dtcnt+1
    else:
        vect = ([dots[dtcnt][0]-dots[dtcnt-1][0],dots[dtcnt][1]-dots[dtcnt-1][1]])
        unitvct = ([vect[0]/dist(0,0,vect[0],vect[1]),vect[1]/dist(0,0,vect[0],vect[1])])
        gapvct = ([unitvct[0]*gap,unitvct[1]*gap])
        gapvctpol = cmath.polar(gapvct[0]+gapvct[1]*1j)
        zboundhigh = cmath.rect(gapvctpol[0],(gapvctpol[1]+curvfront/180*cmath.pi))
        zboundlow = cmath.rect(gapvctpol[0],(gapvctpol[1]-curvfront/180*cmath.pi))
        boundhigh = ([zboundhigh.real+dots[dtcnt][0],zboundhigh.imag+dots[dtcnt][1]])
        boundlow = ([zboundlow.real+dots[dtcnt][0],zboundlow.imag+dots[dtcnt][1]])
        #print dots[dtcnt-1], dots[dtcnt], vect, unitvct, gapvct, gapvctpol, \
        #      zboundhigh, zboundlow, boundhigh, boundlow
        
        linehigh = (dots[dtcnt+1][0]-dots[dtcnt][0])*(boundhigh[1]-dots[dtcnt][1])-\
                  (dots[dtcnt+1][1]-dots[dtcnt][1])*(boundhigh[0]-dots[dtcnt][0])
        linelow = (dots[dtcnt+1][0]-dots[dtcnt][0])*(boundlow[1]-dots[dtcnt][1])-\
                  (dots[dtcnt+1][1]-dots[dtcnt][1])*(boundlow[0]-dots[dtcnt][0])
        
        linerear = (dots[dtcnt+1][0]-dots[dtcnt][0])*(dots[dtcnt][1]-curvrear-dots[dtcnt][1]+curvrear)-\
                  (dots[dtcnt+1][1]-dots[dtcnt][1]+curvrear)*(dots[dtcnt][0]-dots[dtcnt][0])
        linefront = (dots[dtcnt+1][0]-gapvct[0])*(dots[dtcnt][1]-curvfront-dots[dtcnt][1]+curvfront)-\
                  (dots[dtcnt+1][1]-dots[dtcnt][1]+curvfront)*(gapvct[0]-gapvct[0])
        
        if (((linehigh<0 and linelow>0) or (linehigh>0 and linelow<0)) and\
            dist(dots[dtcnt][0],dots[dtcnt][1],dots[dtcnt+1][0],dots[dtcnt+1][1])<gap):
            lines[lncnt][2] = dots[dtcnt+1][0]
            lines[lncnt][3] = dots[dtcnt+1][1]
            dtcnt = dtcnt+1
        else:
            lines.append([0,0,0,0])
            lncnt = lncnt+1
            dtcnt = dtcnt+1
    


img = cv2.imread('lidarimg.jpg')  
for x1,y1,x2,y2 in lines:
    cv2.line(img,(int(x1)+600,int(y1)+600),(int(x2)+600,int(y2)+600),(0,0,255),1)

cv2.imwrite('myfunctimg.jpg',img)


numb=0                    
for row in lines:
    numb = numb+1
    #print row
print numb
#print lines[0][0]
#lines.append([1,1])
#print lines[1][0]
