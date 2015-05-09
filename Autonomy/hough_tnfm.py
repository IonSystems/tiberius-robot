#!/usr/bin/python

import cv2
import numpy as np

linesnum = 0
#creating an inverse-binary image
img = cv2.imread('lidarimg.jpg')
grimg = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(grimg,50,150,apertureSize = 3)
#bwimg = np.zeros((1200,1200,1), np.uint8)
ret,bwimg = cv2.threshold(grimg,120,255,cv2.THRESH_BINARY_INV)

#dilation,erosion
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(bwimg,kernel,iterations = 4)
erosion = cv2.erode(dilation,kernel,iterations = 3)

#Hough transform parameters
rho = 1 #distance resolution of the accumulator in pixels
theta = np.pi/180 #angle resolution of the accumulator in radians
threshold = 70 #accumulator threshold parameter. lines returned with votes >threshold
minlinelength = 30 #line segments shorter than that are rejected
maxlinegap = 50 #max allowed gap between points of the same line to link them


lines = cv2.HoughLinesP(erosion,rho,theta,threshold,minlinelength,maxlinegap)

try:    
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
        linesnum = linesnum+1
except:
    print 'No lines'
print 'Lines number is', linesnum

cv2.imwrite('dilation.jpg',dilation)
cv2.imwrite('erosion.jpg',erosion)
cv2.imwrite('Houghimg.jpg',img)

