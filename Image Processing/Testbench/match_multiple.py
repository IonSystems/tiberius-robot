#! usr/bin/env python

##################################################################################################
# Test script to compare the descriptors of multiple library images with an input test image.
# Returns a match_success based on Lowe's ratio test using BFMatcher.
#
# Input image folder: pi/Desktop/tiberius/Image Processing/Testbench/Images/
#
# Date: 25/02/2015 
# Version: 0.0
##################################################################################################

import cv2
import numpy as np
import sys

MATCH_LIMIT_PERCENT = 10

##################################################################################################

print "\n\nReading the library images"

# read the library images (0: return a GRAYSCALE image)
img_cube = cv2.imread('Images/Library/Cube.jpg',0) 
img_hexagon = cv2.imread('Images/Library/Hexagon.jpg',0)
img_star = cv2.imread('Images/Library/Star.jpg',0)

print "Reading the test image"
img_test = cv2.imread('Images/Test1/Cube.jpg',0)

# INPUT ERROR CATCHING
if ((img_cube is None) or (img_hexagon is None) or (img_star is None)):
   print "Error: A library image was not found. Exiting."
   sys.exit(-1)

if (img_test is None):
   print "Error: The test image was not found. Exiting."
   sys.exit(-1)

##################################################################################################

# RESIZING
print "Resizing the library images"
img_cube    = cv2.resize(img_cube, (1136,640))
img_hexagon = cv2.resize(img_hexagon, (1136,640))
img_star    = cv2.resize(img_star, (1136,640))

print "Resizing the test image"
img_test = cv2.resize(img_test, (1136,640))

# CANNY EDGE ALGORITHM
print "Applying the Canny Edge Detector to the library images"
img_cube    = cv2.Canny(img_cube,400,20)
img_hexagon = cv2.Canny(img_hexagon,400,20)
img_star    = cv2.Canny(img_star,400,20)

print "Applying the Canny Edge Detector to the test image"
img_test = cv2.Canny(img_test,400,20)

# OPENING (EROSION FOLLOWED BY DILATION)
kernel = np.ones((5,5),np.uint8)

print 'Applying Opening to the library images'
img_cube    = cv2.morphologyEx(img_cube,cv2.MORPH_GRADIENT,kernel)
img_hexagon = cv2.morphologyEx(img_hexagon,cv2.MORPH_GRADIENT,kernel)
img_star    = cv2.morphologyEx(img_star,cv2.MORPH_GRADIENT,kernel)

print 'Applying Opening to the test image'
img_test = cv2.morphologyEx(img_test,cv2.MORPH_GRADIENT,kernel)

# THRESHOLD (INVERSE BINARY)
print 'Applying a threshold to the library images'
ret,img_cube    = cv2.threshold(img_cube,0,255,cv2.THRESH_BINARY_INV)
ret,img_hexagon = cv2.threshold(img_hexagon,0,255,cv2.THRESH_BINARY_INV)
ret,img_star    = cv2.threshold(img_star,0,255,cv2.THRESH_BINARY_INV)

print 'Applying a threshold to the test image'
ret,img_test = cv2.threshold(img_test,0,255,cv2.THRESH_BINARY_INV)

##################################################################################################

# find the keypoints and descriptors with SURF
surf = cv2.SURF()

print "Finding the keypoints and descriptors for Cube"
(cube_kpts, cube_dpts) = surf.detectAndCompute(img_cube,None)

print "Finding the keypoints and descriptors for Hexagon"
(hexagon_kpts, hexagon_dpts) = surf.detectAndCompute(img_hexagon,None)

print "Finding the keypoints and descriptors for Star"
(star_kpts, star_dpts) = surf.detectAndCompute(img_star,None)

print "Finding the keypoints and descriptors for the test image"
(test_kpts, test_dpts) = surf.detectAndCompute(img_test,None)

##################################################################################################

# create a dictionary to hold the library images and their descriptors  

libr_imgs = {'cube':cube_dpts, 'hexagon':hexagon_dpts, 'star':star_dpts}

##################################################################################################

# BFMatcher with default parameters
bfmatcher = cv2.BFMatcher()

# initialise matching results
img_matched  = ''
cube_rate    = 0
hexagon_rate = 0
star_rate    = 0

# Iterate through all library images
for image, descriptor in libr_imgs.iteritems():

   print 'Matching the descriptors for {0}:'.format(image)  
   matches = bfmatcher.knnMatch(descriptor, test_dpts, k=2)

   good_matches  = 0
   total_matches = 0
   match_rate    = 0

   # Apply ratio test
   for dmatch_1,dmatch_2 in matches:
      total_matches += 1
      if dmatch_1.distance < 0.75 * dmatch_2.distance:
         good_matches += 1

   match_rate = round(((float(good_matches) / total_matches) * 100),2)

   print 'Match Rate for {0} = {1}%'.format(image,match_rate)

   if   (image == 'cube'):    cube_rate    = match_rate
   elif (image == 'hexagon'): hexagon_rate = match_rate
   elif (image == 'star'):    star_rate    = match_rate

##################################################################################################

# CHECK RESULTS
if   ((cube_rate > hexagon_rate) and (cube_rate > star_rate) and (cube_rate > MATCH_LIMIT_PERCENT)):
   img_matched = 'cube'
elif ((star_rate > hexagon_rate) and (star_rate > MATCH_LIMIT_PERCENT)):
   img_matched = 'star'
elif (hexagon_rate > MATCH_LIMIT_PERCENT):
   img_matched = 'hexagon'


# DISPLAY RESULTS
if (img_matched != None): print '\n\nTest image matched to "{0}"'.format(img_matched)
else:                     print '\n\nImage not matched'









