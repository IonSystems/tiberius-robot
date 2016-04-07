#!/usr/bin/python

import subprocess
import json


class RoboPeakLidar:

    def get_lidar_data():
        args = ("/home/pi/git/tiberius-robot/tiberius/autonomy/readlidar/readlidar")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        return format_data(output)

    def format_data(data):
        return json.loads(data)


if __name__ == "__main__":
    print get_lidar_data()
