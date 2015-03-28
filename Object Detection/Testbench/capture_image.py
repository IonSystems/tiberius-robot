#! usr/bin/env python

##########################################################################
# Test script to capture an image using the pi camera module.
#
# Output image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
#
# Date: 10/03/2015 
# Version: 1.0
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

