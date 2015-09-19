#! usr/bin/env python

##########################################################################
# Test script to compare the descriptors of 2 images.
# Returns a match_success based on Lowe's ratio test.
# Uses BFMatcher and FLANN matching.
#
# Input image folder: home/pi/Desktop/Object Detection/Testbench/Images/
#
# Date: 29/03/2015 
# Version: 1.0
##########################################################################

import cv2
import numpy as np
import sys

print "Reading the images"
image1 = cv2.imread('../Library/Hexagon.png') 
image2 = cv2.imread('Images/Test1/Hexagon.png')

# check input images
if ((image1 is None) or (image2 is None)):
   print "Error: Image not found. Exiting."
   sys.exit(-1)

################################################################################

# find the edges in the images using the Canny algorithm
print 'Applying the Canny Edge Detector to the images'
image1 = cv2.Canny(image1,1200,100)
image2 = cv2.Canny(image2,1200,100)

# apply opening (erosion followed by dilation) to the images.
print 'Applying Opening to the images'
kernel = np.ones((5,5),np.uint8)
image1 = cv2.morphologyEx(image1,cv2.MORPH_GRADIENT,kernel)
image2 = cv2.morphologyEx(image2,cv2.MORPH_GRADIENT,kernel)

# apply a threshold to the images (INVERSE BINARY)
print 'Applying a threshold to the images'
ret,image1 = cv2.threshold(image1,0,255,cv2.THRESH_BINARY_INV)
ret,image2 = cv2.threshold(image2,0,255,cv2.THRESH_BINARY_INV)

##########################################################################
# find the keypoints and descriptors with SURF

surf = cv2.SURF()

print "Finding keypoints for image1"
(keypoints1, descriptors1) = surf.detectAndCompute(image1,None)

print "Finding keypoints for image2"
(keypoints2, descriptors2) = surf.detectAndCompute(image2,None)

###################################################################

# BFMatcher with default parameters

bfmatcher = cv2.BFMatcher()

print "Matching the descriptors with Brute-Force matching"
matches = bfmatcher.knnMatch(descriptors1, descriptors2, k=2)

good_matches  = 0
total_matches = 0
match_rate    = 0

# Apply ratio test
for m,n in matches:
   total_matches += 1
   if m.distance < 0.75*n.distance:
      good_matches += 1
      
match_rate = round(((float(good_matches) / total_matches) * 100),2)

print "Match Rate BFmatcher = {0} %".format(match_rate)
###################################################################

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm= FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params,search_params)

print "Matching the descriptors with FLANN matching"
matches_flann = flann.knnMatch(descriptors1, descriptors2, k=2);

good_matches  = 0
total_matches = 0
match_rate    = 0

# Apply ratio test
for m,n in matches_flann:
   total_matches += 1
   if m.distance < 0.7*n.distance:
      good_matches += 1
   
match_rate = round(((float(good_matches) / total_matches) * 100),2)

print "Match Rate FLANN = {0} %".format(match_rate)


