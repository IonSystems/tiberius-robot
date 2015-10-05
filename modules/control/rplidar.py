#!/usr/bin/python

import csv
import math
import cmath
import cmps11
import subprocess
import cv2
import csv
import numpy as n

class RoboPeakLidar:
	'''
		Provides methods of getting data from teh LIDAR.
		TODO: Do something about the readLidar executable, I am thinking just replace the cpp with python.
	'''
	#calls an executable file 'readlidar', which takes a 360 degrees sweep of data from lidar,
	#filters it to only use objects detected in the distance range from 500mm to 7000mm and
	#stores the data in 'lidardata.csv' file
	def getdots(self):
		args = ("/home/pi/Desktop/Autonomy/readlidar/readlidar")
		popen = subprocess.Popen(args)
		popen.wait()

	#a function, which returns a distance between two dots, which are represented in
	#cartesian coordinates
	def dist(self, x1,y1,x2,y2):
		dist = cmath.sqrt(pow((x2-x1),2) + pow((y2-y1),2))
		return dist.real


	#takes rplidar data, which is represented by a number of dots in polar coordinates, processes them into lines by linking dots
	#based on 'gap' and 'curvfront' parameters and returns lines, represented by 2 polar coordinates (line start, line end)
	def getlines(self):   
		dots = []     #used to store data from 'lidardata.csv' file
		lines = []    #stores detected lines in cartesian coordinates
		linespol = [] #stores detected lines in polar coordinates
		dotsnumb = 0
		lines.append([0,0,0,0]) #creates an empty line
		lncnt = 0
		dtcnt = 0
		gap = 20.0    #parameter(cm), identifies the max distance between two dots for them to be considered to be in the same line
		#curvrear = 4.0
		curvfront = 40.0 #parameter(degrees), identifies the angle deviation from the line to create an area, where if a dot is found
						 #in that area it is considered to be a part of the line
		anglest = 0
		anglend = 0
		fx = 0

		getdots()
		cmpshd = cmps11.heading() #gets a current heading from compass


		#converts lidar data from polar to rectangular coordinates and stores in 'dots' list
		with open('/home/pi/Desktop/Autonomy/lidardata.csv', 'rb') as lidar:
			readldr = csv.reader(lidar)
			for row in readldr:
				r = row[1]
				ph = row[0]
				dotsnumb = dotsnumb+1
				z = cmath.rect(float(r)/10,float(ph)/180*cmath.pi) #note that length is converted from mm to cm
				dots.append([z.real,z.imag])
				
		#loops through a list of dots and groups them into lines based on 'gap' and 'curvfront' parameters
		for x in xrange(dotsnumb-1):
			#if a current row in 'lines' is empty
			if (lines[lncnt][0]==0):
				if (dist(dots[dtcnt][0],dots[dtcnt][1],dots[dtcnt+1][0],dots[dtcnt+1][1])<gap):
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
				#creates a vector using the current dot, which is also a end of the current line, and previous dot, which is
				#a part of the current line. 
				vect = ([dots[dtcnt][0]-dots[dtcnt-1][0],dots[dtcnt][1]-dots[dtcnt-1][1]])
				unitvct = ([vect[0]/dist(0,0,vect[0],vect[1]),vect[1]/dist(0,0,vect[0],vect[1])])
				#creates a vector with the length equal to 'gap' parameter
				gapvct = ([unitvct[0]*gap,unitvct[1]*gap])
				gapvctpol = cmath.polar(gapvct[0]+gapvct[1]*1j)
				#creates two vectors of the same length as gapvctpol, which are spread from it by +-'curvfront' degrees
				zboundhigh = cmath.rect(gapvctpol[0],(gapvctpol[1]+curvfront/180*cmath.pi))
				zboundlow = cmath.rect(gapvctpol[0],(gapvctpol[1]-curvfront/180*cmath.pi))
				#move vectors to current line end coordinates, which can be viewed as two lines starting from the current line end
				#and terminating at boundhigh and boundlow, creating an angle of (2*curvfront)
				boundhigh = ([zboundhigh.real+dots[dtcnt][0],zboundhigh.imag+dots[dtcnt][1]])
				boundlow = ([zboundlow.real+dots[dtcnt][0],zboundlow.imag+dots[dtcnt][1]])
				
				#check if the next dot is in the area created by the above described lines using the formula:
				#d = (x-x1)(y2-y1)-(y-y1)(x2-x1), where (x,y) is a dot and (x1,y1,x2,y2) is a line and d shows on which side
				#of the line the dot is
				linehigh = (dots[dtcnt+1][0]-dots[dtcnt][0])*(boundhigh[1]-dots[dtcnt][1])-\
						  (dots[dtcnt+1][1]-dots[dtcnt][1])*(boundhigh[0]-dots[dtcnt][0])
				linelow = (dots[dtcnt+1][0]-dots[dtcnt][0])*(boundlow[1]-dots[dtcnt][1])-\
						  (dots[dtcnt+1][1]-dots[dtcnt][1])*(boundlow[0]-dots[dtcnt][0])

				#here the code can be added which introduces the use of 'curvrear' parameter
				
				#if the next dot is in the above described area then the current line end's coordinates are replaced by
				#the next dote coordinates, so the next dot becomes the end of the current line
				if ((((linehigh<0 and linelow>0) or (linehigh>0 and linelow<0)) and\
					dist(dots[dtcnt][0],dots[dtcnt][1],dots[dtcnt+1][0],dots[dtcnt+1][1])<gap) or\
					dist(dots[dtcnt][0],dots[dtcnt][1],dots[dtcnt+1][0],dots[dtcnt+1][1])<2):
					lines[lncnt][2] = dots[dtcnt+1][0]
					lines[lncnt][3] = dots[dtcnt+1][1]
					dtcnt = dtcnt+1
				#otherwise the current line stays as it is, and a new empty line is created
				else:
					lines.append([0,0,0,0])
					lncnt = lncnt+1
					dtcnt = dtcnt+1

		#checks if the first and the last lines are in the same line and links them if true, in which case the last line
		#is discarded when lines are converted to linespol by using 'fx' parameter
		#also checks if the last line is empty, ignors it if true and checks if the first line and
		#the line before the empty line are in the same line, links them if true, in which case the last two lines are
		#discarded, if false then only empty line is discarded
		if (lines[len(lines)-1][0]!=0):
			#check if the last line is not a dot, since vector of a dot is 0, then apply the same process as above
			if (lines[len(lines)-1][2]!=lines[len(lines)-1][0] and lines[len(lines)-1][3]!=lines[len(lines)-1][1]):
				vect = ([lines[len(lines)-1][2]-lines[len(lines)-1][0],\
						 lines[len(lines)-1][3]-lines[len(lines)-1][1]])
				unitvct = ([vect[0]/dist(0,0,vect[0],vect[1]),vect[1]/dist(0,0,vect[0],vect[1])])
				gapvct = ([unitvct[0]*gap,unitvct[1]*gap])
				gapvctpol = cmath.polar(gapvct[0]+gapvct[1]*1j)
				zboundhigh = cmath.rect(gapvctpol[0],(gapvctpol[1]+curvfront/180*cmath.pi))
				zboundlow = cmath.rect(gapvctpol[0],(gapvctpol[1]-curvfront/180*cmath.pi))
				boundhigh = ([zboundhigh.real+lines[len(lines)-1][2],zboundhigh.imag+lines[len(lines)-1][3]])
				boundlow = ([zboundlow.real+lines[len(lines)-1][2],zboundlow.imag+lines[len(lines)-1][3]])
				
				linehigh = (lines[0][0]-lines[len(lines)-1][2])*(boundhigh[1]-lines[len(lines)-1][3])-\
						  (lines[0][1]-lines[len(lines)-1][3])*(boundhigh[0]-lines[len(lines)-1][2])
				linelow = (lines[0][0]-lines[len(lines)-1][2])*(boundlow[1]-lines[len(lines)-1][3])-\
						  (lines[0][1]-lines[len(lines)-1][3])*(boundlow[0]-lines[len(lines)-1][2])

				if ((((linehigh<0 and linelow>0) or (linehigh>0 and linelow<0)) and\
					dist(lines[len(lines)-1][2],lines[len(lines)-1][3],lines[0][0],lines[0][1])<gap) or\
					dist(lines[len(lines)-1][2],lines[len(lines)-1][3],lines[0][0],lines[0][1])<2):
					lines[0][0] = lines[len(lines)-1][0]
					lines[0][1] = lines[len(lines)-1][1]
					fx = 1
				else:
					fx = 0
				cntt=0

		#the last line is empty        
		else:
			if (lines[len(lines)-2][2]!=lines[len(lines)-2][0] and lines[len(lines)-2][3]!=lines[len(lines)-2][1]):
				vect = ([lines[len(lines)-2][2]-lines[len(lines)-2][0],\
						 lines[len(lines)-2][3]-lines[len(lines)-2][1]])
				unitvct = ([vect[0]/dist(0,0,vect[0],vect[1]),vect[1]/dist(0,0,vect[0],vect[1])])
				gapvct = ([unitvct[0]*gap,unitvct[1]*gap])
				gapvctpol = cmath.polar(gapvct[0]+gapvct[1]*1j)
				zboundhigh = cmath.rect(gapvctpol[0],(gapvctpol[1]+curvfront/180*cmath.pi))
				zboundlow = cmath.rect(gapvctpol[0],(gapvctpol[1]-curvfront/180*cmath.pi))
				boundhigh = ([zboundhigh.real+lines[len(lines)-2][2],zboundhigh.imag+lines[len(lines)-2][3]])
				boundlow = ([zboundlow.real+lines[len(lines)-2][2],zboundlow.imag+lines[len(lines)-2][3]])
				
				linehigh = (lines[0][0]-lines[len(lines)-2][2])*(boundhigh[1]-lines[len(lines)-2][3])-\
						  (lines[0][1]-lines[len(lines)-2][3])*(boundhigh[0]-lines[len(lines)-2][2])
				linelow = (lines[0][0]-lines[len(lines)-2][2])*(boundlow[1]-lines[len(lines)-2][3])-\
						  (lines[0][1]-lines[len(lines)-2][3])*(boundlow[0]-lines[len(lines)-2][2])

				if ((((linehigh<0 and linelow>0) or (linehigh>0 and linelow<0)) and\
					dist(lines[len(lines)-2][2],lines[len(lines)-2][3],lines[0][0],lines[0][1])<gap) or\
					dist(lines[len(lines)-2][2],lines[len(lines)-2][3],lines[0][0],lines[0][1])<2):
					lines[0][0] = lines[len(lines)-2][0]
					lines[0][1] = lines[len(lines)-2][1]
					fx = 2
				else:
					fx = 1
			else:
				fx = 1
				
		#converts from cartesian (lines) to polar (linespol) coordinates
		for row in xrange(len(lines)-fx):
					polstart = cmath.polar(lines[row][0]+lines[row][1]*1j)
					polend = cmath.polar(lines[row][2]+lines[row][3]*1j)
					startth = polstart[1]
					endth = polend[1]
					#check if line's start and end angles are not inside the 0-360 degrees range
					#adjust it to that range and add compass heading to put the linespol in compass domain
					if (startth/math.pi*180<0):
						startth = startth+math.pi*2
					if (startth/math.pi*180+cmpshd>=360):
						anglest = startth/math.pi*180+cmpshd-360
					else:
						anglest = startth/math.pi*180+cmpshd
					if (endth/math.pi*180<0):
						endth = polend[1]+math.pi*2
					if (endth/math.pi*180+cmpshd>=360):
						anglend = endth/math.pi*180+cmpshd-360
					else:
						anglend = endth/math.pi*180+cmpshd
					linespol.append([round(anglest,4),round(polstart[0],4),\
									 round(anglend,4),round(polend[0],4)])
		print 'len(lines): ', len(lines)
		print 'len(linespol): ', len(linespol)
		#drawing the lines obtained
		#img = cv2.imread('lidarimg.jpg')  
		#for x1,y1,x2,y2 in lines:
		#    cv2.line(img,(int(x1)+700,int(y1)+700),(int(x2)+700,int(y2)+700),(0,0,255),1)
		#cv2.imwrite('myfunctimg.jpg',img)
		return linespol
		
		
		'''
			Image methods
		'''
	def createimg(self, height, width, grayclr):
		"""Create new numpy array for a grayscale image(def white)"""
		array = np.zeros((height, width, 1), np.uint8)
		
		#make the image white
		array[:] = grayclr
		
		return array

	#creating a white blank image
	height, width = 1400, 1400
	color = 255

	image = createimg(height, width, color)


	#reading lidar data from the file
	xycoord = []
	with open('lidardata.csv', 'rb') as lidar:
		readldr = csv.reader(lidar)
		for row in readldr:
			r = row[1]
			ph = row[0]
			#converting lidar data from polar to rectangular coordinates
			z = cmath.rect(float(r)/10,float(ph)/180*cmath.pi)
			#print int(round(z.real)), int(round(z.imag))
			#filling the image with lidar data
			image[int(round(z.imag))+700, int(round(z.real))+700] = 0
			xycoord.append([int(round(z.real)), int(round(z.imag))])
	cv2.imwrite('lidarimg.jpg', image)

	with open('lidarxy.csv','wb') as f:
		lid = csv.writer(f)
		lid.writerows(xycoord)