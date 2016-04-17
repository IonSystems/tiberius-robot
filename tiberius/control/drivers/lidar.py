#!/usr/bin/python

import subprocess
import json


class RoboPeakLidar:
    '''
    Interfaces with the RPLidar driver, which is implemented in C++.
    TODO: If you really want to port the driver to Python.

    The C++ driver returns a JSON formatted array of objects. Each object
    contains:
    - angle
    - distance
    - start_flag
    - quality
    '''

    def get_lidar_data(self):
        '''
        Run the readlidar executable and read the data from standard output.
        Returns a Python dictionary containing all results from the scan.
        '''
        args = ("/home/pi/git/tiberius-robot/tiberius/autonomy/readlidar/readlidar")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        return self.format_data(output)

    def format_data(self, data):
        '''
        Convert the raw JSON text to a Python dictionary.
        '''
        data = self.check_commas(data)
        return json.loads(data)

    def check_commas(self, data):
        '''
        As of witing, the readlidar implementations returns an extra comma in
        it's JSON output, which causes json.loads() to fail. This function
        removes the last comma from the output so it can be succesfully
        parsed.
        '''
        return data.replace(',\n]', ']')

if __name__ == "__main__":
    l = RoboPeakLidar()
    l.get_lidar_data()
