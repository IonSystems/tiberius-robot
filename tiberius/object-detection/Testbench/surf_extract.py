#! usr/bin/env python

###########################################################################
# Test script to extract the keypoints and descriptors from a test image.
#
# Input image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
# Output image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
#
# Date: 29/03/2015
# Version: 1.0
###########################################################################

import cv2
import numpy as np
import sys

# open the test image
image = cv2.imread('./Images/Test.jpg')

if (image is None):
    print "Error: Image not found. Exiting."
    sys.exit(-1)

# find the edges in the image using the Canny algorithm
image = cv2.Canny(image, 1200, 100)

# apply opening (erosion followed by dilation) to the image.
kernel = np.ones((5, 5), np.uint8)
image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

# apply a threshold to the image (INVERSE BINARY)
ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)

surf = cv2.SURF()

# find the keypoints and descriptors of the image
(keypoints, descriptors) = surf.detectAndCompute(image, None)

# draw only keypoints location, not size and orientation and write the
# result to the output image
image_out = cv2.drawKeypoints(image, keypoints, color=(0, 255, 0), flags=0)

cv2.imwrite('Images/Test_Output.jpg', image_out)
