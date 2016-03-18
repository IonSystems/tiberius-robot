#! usr/bin/env python

##########################################################################
# Test script to capture an image using the pi camera module.
#
# Output image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
#
# Date: 28/03/2015
# Version: 1.0
##########################################################################

import picamera

# Instantiate the camera module.
camera = picamera.PiCamera()

# Display a preview to ensure that you capture the right test image.
camera.start_preview()
camera.resolution = (640, 480)

# Wait until CTRL+C is pressed.
try:
    while True:
        pass

# Capture an image.
except KeyboardInterrupt:
    camera.stop_preview()
    camera.capture('Images/Test.jpg')
