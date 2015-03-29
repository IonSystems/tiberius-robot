#! usr/bin/env python

##################################################################################################
# Test script to compare the descriptors of multiple library images with an input test image.
# Returns a match_success based on Lowe's ratio test using BFMatcher.
#
# Input image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
#
# Date: 29/03/2015  
# Version: 1.0
##################################################################################################

import cv2
import numpy as np
import sys

# An object is matched, if its match percentage is more than the set limit 
# and the number of colored pixels detected in the image exceeds the set threshold for each object.
MATCH_LIMIT_PERCENT = 10
RED_THRESHOLD       = 5000
GREEN_THRESHOLD     = 20000
BLUE_THRESHOLD      = 50000

# If the number of colored pixels is less than the below threshold, don't proceed with the testing - not enough data present.
PIXEL_THRESHOLD = 5000

RED_PIXELS          = 0 # STAR
GREEN_PIXELS        = 0 # CUBE
BLUE_PIXELS         = 0 # HEXAGON

#####################################################################
# Change the color of the pixel based on the desired object's color.
#####################################################################
def adjust_pixel(search_object,image,x_pos,y_pos):
    global RED_PIXELS
    global GREEN_PIXELS
    global BLUE_PIXELS
    
    # Get the pixel value.
    blue  = image[y_pos][x_pos][0] # BLUE
    green = image[y_pos][x_pos][1] # GREEN
    red   = image[y_pos][x_pos][2] # RED
    
    # CUBE - GREEN
    if ((search_object == "CUBE") and (red < 70) and (green > 70) and (blue < 70)) : 
        
        # If the pixel value is inside the object's color limits, set the pixel value to the object's color.
        image.itemset((y_pos,x_pos,0),0)
        image.itemset((y_pos,x_pos,1),255)
        image.itemset((y_pos,x_pos,2),0)
        GREEN_PIXELS += 1
            
    # HEXAGON - BLUE        
    elif ((search_object == "HEXAGON") and (red < 70) and (green < 70) and (blue > 70)):
           
        image.itemset((y_pos,x_pos,0),255)
        image.itemset((y_pos,x_pos,1),0)
        image.itemset((y_pos,x_pos,2),0)
        BLUE_PIXELS += 1
            
    # STAR - RED        
    elif ((search_object == "STAR") and (red > 70) and (green < 70) and (blue < 70)):

        image.itemset((y_pos,x_pos,0),0)
        image.itemset((y_pos,x_pos,1),0)
        image.itemset((y_pos,x_pos,2),255)
        RED_PIXELS += 1
            
    # Else set the pixel value to white.    
    else:
        
        image.itemset((y_pos,x_pos,0),255)
        image.itemset((y_pos,x_pos,1),255)
        image.itemset((y_pos,x_pos,2),255)  



##################################################### -- MAIN PROGRAM -- #####################################################

# The object to be detected.
DETECT_OBJECT = "STAR"

print "\n\nReading the library images"

# read the library images (0: return a GRAYSCALE image)
img_cube = cv2.imread('../Library/Cube.jpg') 
img_hexagon = cv2.imread('../Library/Hexagon.jpg')
img_star = cv2.imread('../Library/Star.jpg')

print "Reading the test image"
img_test = cv2.imread('./Images/Test.jpg')

# INPUT ERROR CATCHING
if ((img_cube is None) or (img_hexagon is None) or (img_star is None)):
   print "Error: A library image was not found. Exiting."
   sys.exit(-1)

if (img_test is None):
   print "Error: The test image was not found. Exiting."
   sys.exit(-1)

##################################################################################################

# ADJUST TEST IMAGE COLOR
print "Adjusting the color of the test image"

# Get the width and height of the image.
height = img_test.shape[0]
width = img_test.shape[1]

x_pos = 0
# Iterate through the rows.
while (x_pos < width):
    y_pos = 0
    
    # Iterate through the column for each row.
    while (y_pos < height):
        # Adjust the color of the pixel based on the object that needs to be detected.
        adjust_pixel(DETECT_OBJECT,img_test,x_pos,y_pos)
        y_pos += 1
        
    x_pos += 1  
    
# If the number of colored pixels is more than the set pixel threshold, proceed with testing.    
if ((RED_PIXELS > PIXEL_THRESHOLD) or (BLUE_PIXELS > PIXEL_THRESHOLD) or (GREEN_PIXELS > PIXEL_THRESHOLD)):   

    # CANNY EDGE ALGORITHM
    print "Applying the Canny Edge Detector to the library images"
    img_cube    = cv2.Canny(img_cube, 1200, 100)
    img_hexagon = cv2.Canny(img_hexagon, 1200, 100)
    img_star    = cv2.Canny(img_star, 1200, 100)
    
    print "Applying the Canny Edge Detector to the test image"
    img_test = cv2.Canny(img_test, 1200, 100)
    
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
    
    # initialise matching results
    img_matched  = ''
    cube_rate    = 0
    hexagon_rate = 0
    star_rate    = 0
    
    # If the image wasn't cleared (no descriptors) - when the picture doesn't match the desired object.
    if (test_dpts is not None): 
        
       # BFMatcher with default parameters
       bfmatcher = cv2.BFMatcher()
    
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
    if   ((cube_rate > hexagon_rate) and (cube_rate > star_rate) and (cube_rate > MATCH_LIMIT_PERCENT) and (GREEN_PIXELS > GREEN_THRESHOLD)):
       img_matched = 'cube'
    elif ((star_rate > hexagon_rate) and (star_rate > MATCH_LIMIT_PERCENT) and (RED_PIXELS > RED_THRESHOLD)):
       img_matched = 'star'
    elif ((hexagon_rate > MATCH_LIMIT_PERCENT) and (BLUE_PIXELS > BLUE_THRESHOLD)):
       img_matched = 'hexagon'
    
    
    # DISPLAY RESULTS
    if (img_matched != None): print '\n\nTest image matched to "{0}"'.format(img_matched)
    else:                     print '\n\nImage not matched'


# If the number of colored pixels is less than the set pixel threshold - not enough data present to make a decision.
else:
    print '\n\nObject Detection cancelled. Not enough data present.'







