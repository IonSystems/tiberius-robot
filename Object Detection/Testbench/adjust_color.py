#! usr/bin/env python

###################################################################################
# Adjust the color of an image based on the desired object's color.
#
# Input image folder: home/pi/Desktop/tiberius/Object Detection/Testbench/Images/
#
# Date: 29/03/2015 
# Version: 1.0
###################################################################################

import cv2
import numpy as np


#####################################################################
# Change the color of the pixel based on the desired object's color.
#####################################################################
def adjust_pixel(search_object,image,x_pos,y_pos):
    
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
            
    # HEXAGON - BLUE        
    elif ((search_object == "HEXAGON") and (red < 70) and (green < 70) and (blue > 70)):
           
        image.itemset((y_pos,x_pos,0),255)
        image.itemset((y_pos,x_pos,1),0)
        image.itemset((y_pos,x_pos,2),0)
            
    # STAR - RED        
    elif ((search_object == "STAR") and (red > 70) and (green < 70) and (blue < 70)):

        image.itemset((y_pos,x_pos,0),0)
        image.itemset((y_pos,x_pos,1),0)
        image.itemset((y_pos,x_pos,2),255)
            
    # Else set the pixel value to white.    
    else:
        
        image.itemset((y_pos,x_pos,0),255)
        image.itemset((y_pos,x_pos,1),255)
        image.itemset((y_pos,x_pos,2),255)       
        


############################################# MAIN PROGRAM ################################

# Open the test image.
image = cv2.imread('./Images/Test.jpg')

# Get the width and height of the image.
height = image.shape[0]
width = image.shape[1]

x_pos = 0

print "Iterating through the image..."

# Iterate through the rows.
while (x_pos < width):
    y_pos = 0
    
    # Iterate through the column for each row.
    while (y_pos < height):
        
        # Adjust the color of the pixel based on the object that needs to be detected.
        adjust_pixel("CUBE",image,x_pos,y_pos)
        y_pos += 1
        
    x_pos += 1   
      

cv2.imwrite('Images/color.jpg', image)


