#! usr/bin/env python

######################################################################
# Test script to capture an image using the pi camera module.
#
# Output image folder: pi/Desktop/Image Processing/Testbench/Images/
#
# Date: 20/01/2015 
# Version: 0.0
######################################################################

import picamera

# Instantiate the camera module and capture an image.
camera = picamera.PiCamera()

camera.capture('Images/test.jpg')

