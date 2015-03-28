#! usr/bin/env python

###########################################################################################################
# Capture an image and detect whether the object in the image is the one that has been set by the mission.
# Uses a socket connection to communicate with the database unit.
#
# Image Library: home/pi/Desktop/tiberius/Object Detection/Library
#
# Date: 22/03/2015 
# Version: 1.0
###########################################################################################################

import cv2
import numpy as np
import time
import socket
import picamera

############################################ -- GLOBAL VARIABLES -- #############################################

# An object is matched, if its match percentage is more than the limit.
MATCH_LIMIT_PERCENT = 10
# Objects
CUBE    = "CUBE"
HEXAGON = "HEXAGON"
STAR    = "STAR"
NONE    = "NONE"
# Socket parameters
DATABASE_HOST = "192.168.0.2"
DATABASE_PORT = 60000 


############################################## -- FUNCTIONS -- ################################################

######################################################
# Receive a message from the database via the socket.
######################################################
def receive_message(database,message):
    database.sendall(message)
    recv_message = database.recv(2048)
    recv_message = recv_message.replace("\n","") # Database sends the message with a "\n" appended at the end.
    return recv_message


#####################
# Capture an image.
#####################
def capture_image():
    camera = picamera.PiCamera()
    camera.capture('./Image.png')
    
    
######################################################
# Get the descriptors of the library images.
# Return a dictionary with image:descriptor pairs.
######################################################    
def get_library():
    # READ THE LIBRARY IMAGES (0: return a GRAYSCALE image)
    img_cube = cv2.imread('./Library/Cube.png',0) 
    img_hexagon = cv2.imread('./Library/Hexagon.png',0)
    img_star = cv2.imread('./Library/Star.png',0)

    # RESIZING
    img_cube    = cv2.resize(img_cube, (1136,640))
    img_hexagon = cv2.resize(img_hexagon, (1136,640))
    img_star    = cv2.resize(img_star, (1136,640))

    # CANNY EDGE ALGORITHM
    img_cube    = cv2.Canny(img_cube,300,20)
    img_hexagon = cv2.Canny(img_hexagon,300,20)
    img_star    = cv2.Canny(img_star,300,20)

    # OPENING (EROSION FOLLOWED BY DILATION)
    kernel = np.ones((5,5),np.uint8)
    img_cube    = cv2.morphologyEx(img_cube,cv2.MORPH_GRADIENT,kernel)
    img_hexagon = cv2.morphologyEx(img_hexagon,cv2.MORPH_GRADIENT,kernel)
    img_star    = cv2.morphologyEx(img_star,cv2.MORPH_GRADIENT,kernel)

    # THRESHOLD (INVERSE BINARY)
    ret,img_cube    = cv2.threshold(img_cube,0,255,cv2.THRESH_BINARY_INV)
    ret,img_hexagon = cv2.threshold(img_hexagon,0,255,cv2.THRESH_BINARY_INV)
    ret,img_star    = cv2.threshold(img_star,0,255,cv2.THRESH_BINARY_INV)

    # SURF - FIND KEYPOINTS AND DESCRIPTORS
    surf = cv2.SURF()
    (cube_kpts, cube_dpts) = surf.detectAndCompute(img_cube,None)
    (hexagon_kpts, hexagon_dpts) = surf.detectAndCompute(img_hexagon,None)
    (star_kpts, star_dpts) = surf.detectAndCompute(img_star,None)

    # LIBRARY IMAGE DICTIONARY - IMAGE:DESCRIPTORS  
    library = {CUBE:cube_dpts, HEXAGON:hexagon_dpts, STAR:star_dpts}
    return library
      
    
#####################################################################
# Analyse an image and check whether it matches the mission object.
#####################################################################
def analyse_image(mission_object,library,database):  
    
    ############## -- CAPTURED IMAGE -- #########################
    image = cv2.imread('./Image.png',0)
    # RESIZING
    image    = cv2.resize(image, (1136,640))
    # CANNY EDGE ALGORITHM
    image    = cv2.Canny(image,300,20)
    # OPENING (EROSION FOLLOWED BY DILATION)
    kernel = np.ones((5,5),np.uint8)
    image    = cv2.morphologyEx(image,cv2.MORPH_GRADIENT,kernel)
    # THRESHOLD (INVERSE BINARY)
    ret,image    = cv2.threshold(image,0,255,cv2.THRESH_BINARY_INV)
    # SURF - FIND KEYPOINTS AND DESCRIPTORS
    surf = cv2.SURF()
    (image_kpts, image_dpts) = surf.detectAndCompute(image,None)
    
    ############## -- COMPARING -- ############################
     
    # BFMatcher with default parameters
    bfmatcher = cv2.BFMatcher()

    # object results
    img_matched  = ""
    cube_rate    = 0
    hexagon_rate = 0
    star_rate    = 0

    # Iterate through all library images
    for name, descriptor in library.iteritems():
  
       matches = bfmatcher.knnMatch(descriptor, image_dpts, k=2)

       # matching results
       good_matches  = 0
       total_matches = 0
       match_rate    = 0

       # Apply ratio test
       for dmatch_1,dmatch_2 in matches:
          total_matches += 1
          if dmatch_1.distance < 0.75 * dmatch_2.distance:
             good_matches += 1
             
       # round the match_rate to 2 decimal places         
       match_rate = round(((float(good_matches) / total_matches) * 100),2)

       if   (name == CUBE):    cube_rate    = match_rate
       elif (name == HEXAGON): hexagon_rate = match_rate
       elif (name == STAR):    star_rate    = match_rate


    # CHECK RESULTS
    if   ((cube_rate > hexagon_rate) and (cube_rate > star_rate) and (cube_rate > MATCH_LIMIT_PERCENT)):
       img_matched = CUBE
    elif ((star_rate > hexagon_rate) and (star_rate > MATCH_LIMIT_PERCENT)):
       img_matched = STAR
    elif (hexagon_rate > MATCH_LIMIT_PERCENT):
       img_matched = HEXAGON
       
    # if the detected image matches the mission object   
    if (img_matched == mission_object): 
        # tell the mission that the object has been detected and send to the database the matching results
        database.sendall("WRITE.OBJECT_SIMILARITY,CUBE:" + str(cube_rate) + ",HEX:" + str(hexagon_rate) + ",STAR:" + str(star_rate) +".")
        database.sendall("WRITE.MISSION_STATUS,OBJECT_DETECTED.")
        # close the connection to the database and wait for 1 minute
        database.close()
        time.sleep(60)
        
    else:
        # tell the mission to continue scanning for other objects
        database.sendall("WRITE.MISSION_STATUS,SCANNING_OBJECTS.")






############################################### -- MAIN PROGRAM -- ######################################################  

library = get_library() # store the descriptors of the library images in a dictionary

while 1:
    
    # CONNECTING TO THE DATABASE
    try: 
        
        database = socket.socket()
        database.connect((DATABASE_HOST,DATABASE_PORT))
        
        # get the mode of Tiberius
        mode = receive_message(database,"READ.TIBERIUS_STATUS.")
        
        # IF AUTONOMY MODE
        if(mode == "AUTONOMY_MODE"):
            # get the object to be detected in the mission
            mission_object = receive_message(database,"READ.MISSION_OBJECT.")
            
            
            # IF AN OBJECT HAS BEEN SELECTED
            if(mission_object != "NONE"):
                # get the current status of the mission
                mission_status = receive_message(database,"READ.MISSION_STATUS.")
                
                
                # ANALYSING IMAGE => AN IMAGE NEEDS TO BE CAPTURED AND ANALYSED
                if(mission_status == "ANALYSING_IMAGE"):
                    #capture_image()
                    analyse_image(mission_object,library,database)
                
                # FOR ANY OTHER STATUS
                else:
                    # close the connection and wait for 2 seconds before trying again
                    database.close()
                    time.sleep(2)
           
           
            # IF NO OBJECT HAS BEEN SELECTED   
            else:
                # close the connection and wait for 1 minute before trying again
                database.close()
                time.sleep(60)
        
        
        # ANY OTHER MODE    
        else:
            # close the connection and wait for 10 seconds before trying again
            database.close() 
            time.sleep(10)
            
            
    # CONNECTION UNAVAILABLE     
    except socket.error:
        # wait for 5 seconds before trying again
        time.sleep(5)
                