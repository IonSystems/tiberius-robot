#! usr/bin/env python

###################################################################################
# Test script to extract the keypoints and descriptors from a test image using ORB.
#
# Input image folder: pi/Desktop/Image Processing/Testbench/Images/
# Output image folder: pi/Desktop/Image Processing/Testbench/Images/
#
# Date: 20/01/2015 
# Version: 0.0
###################################################################################

import numpy as np
import cv2

# open the test image
image = cv2.imread('Images/test.jpg',0)

orb = cv2.ORB()

# find the keypoints and descriptors of the image
keypoints = orb.detect(image,None)
#(keypoints, descriptors) = orb.compute(image,keypoints)

# draw only keypoints location, not size and orientation and write the result to the output image
image_out = cv2.drawKeypoints(image,keypoints,color=(0,0,255),flags=0)

cv2.imwrite('Images/output.jpg',image_out)