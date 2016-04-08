#!/usr/bin/python

import subprocess
import json


class RoboPeakLidar:

    def get_lidar_data(self):
        args = ("/home/pi/git/tiberius-robot/tiberius/autonomy/readlidar/readlidar")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        return self.format_data(output)

    def format_data(self, data):
       	data = self.check_commas(data)
        return json.loads(data)

    def check_commas(self, data):
        return data.replace(',\n]', ']')

if __name__ == "__main__":
    l = RoboPeakLidar()
    l.get_lidar_data()
