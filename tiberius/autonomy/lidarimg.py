#!/usr/bin/python

import cv2
import csv
import cmath
import numpy as np


def createimg(height, width, grayclr):
    """Create new numpy array for a grayscale image(def white)"""
    array = np.zeros((height, width, 1), np.uint8)

    # make the image white
    array[:] = grayclr

    return array

# creating a white blank image
height, width = 1400, 1400
color = 255

image = createimg(height, width, color)


# reading lidar data from the file
xycoord = []
with open('lidardata.csv', 'rb') as lidar:
    readldr = csv.reader(lidar)
    for row in readldr:
        r = row[1]
        ph = row[0]
        # converting lidar data from polar to rectangular coordinates
        z = cmath.rect(float(r) / 10, float(ph) / 180 * cmath.pi)
        # print int(round(z.real)), int(round(z.imag))
        # filling the image with lidar data
        image[int(round(z.imag)) + 700, int(round(z.real)) + 700] = 0
        xycoord.append([int(round(z.real)), int(round(z.imag))])
cv2.imwrite('lidarimg.jpg', image)

with open('lidarxy.csv', 'wb') as f:
    lid = csv.writer(f)
    lid.writerows(xycoord)
