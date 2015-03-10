#######################
####--README FILE--####
#######################

Last Update: 25/02/2015

!!! Please update this file as you update the software. !!!


The "Image Processing/Testbench" folder contains scripts, that test the functionality of individual components 
of the image processing sector.


################
capture_image.py
################
  Test script to capture an image using the pi camera module.

  Current version: 0.0


##############
surf_extract.py
##############
  Test script to extract the keypoints and descriptors from a test image.

  Current version: 0.0

##############
match.py
##############
  Test script to compare the descriptors of 2 images.
  Returns a match_success based on Lowe's ratio test.
  Uses BFMatcher and FLANN matching.

  Current version: 0.0

##############
match_multiple.py
##############
  Test script to compare the descriptors of multiple library images with an input test image.
  Returns a match_success based on Lowe's ratio test using BFMatcher.

  Current version: 0.0

