#!/usr/bin/python

import subprocess

args = ("/home/pi/Desktop/Autonomy/readlidar/readlidar")
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
print output
