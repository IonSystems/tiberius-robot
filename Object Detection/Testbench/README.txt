#######################
####--README FILE--####
#######################

Last Update: 10/03/2015

!!! Please update this file as you update the software. !!!


The "Object Detection/Testbench" folder contains scripts, that test the functionality of individual components 
of the object detection sector.


################
capture_image.py
################
  Test script to capture an image using the pi camera module.

  Current version: 1.0


##############
surf_extract.py
##############
  Test script to extract the keypoints and descriptors from a test image.

  Current version: 1.0

##############
match.py
##############
  Test script to compare the descriptors of 2 images.
  Returns a match_success based on Lowe's ratio test.
  Uses BFMatcher and FLANN matching.

  Current version: 1.0

##############
match_multiple.py
##############
  Test script to compare the descriptors of multiple library images with an input test image.
  Returns a match_success based on Lowe's ratio test using BFMatcher.

  Current version: 1.0

