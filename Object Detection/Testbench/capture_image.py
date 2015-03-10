#! usr/bin/env python

##########################################################################
# Test script to capture an image using the pi camera module.
#
# Output image folder: pi/Desktop/tiberius/Image Processing/Testbench/Images/
#
# Date: 17/02/2015 
# Version: 0.0
##########################################################################

import picamera
from time import sleep

# Instantiate the camera module.
camera = picamera.PiCamera()

# Display a preview to ensure that you capture the right test image.
camera.start_preview()
sleep(10)
camera.stop_preview()

camera.capture('Images/Test.jpg')

