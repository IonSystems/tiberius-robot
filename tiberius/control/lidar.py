#!/usr/bin/python

import subprocess

args = ("/home/pi/git/tiberius-robot/tiberius/autonomy/readlidar/readlidar")
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read()
print output
