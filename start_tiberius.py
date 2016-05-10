#!/usr/bin/env python
from optparse import OptionParser
from subprocess import Popen, PIPE
from tiberius.database.database_threads import DatabaseThreadCreator
from multiprocessing import Process
from enum import Enum
import sys
import time
from tiberius.config.config_parser import TiberiusConfigParser
import tiberius.database.create as cr
import tiberius.database.insert as ins
from tiberius.communications import antenna_thread as ant_thread
from tiberius.control.control import Control
from tiberius.diagnostics.external_hardware_controller import compass_monitor


class Action(Enum):
    WEB_SERVER = 0


parser = OptionParser()

parser.add_option(
    "-w",
    "--web-server",
    action="store_const",
    const=Action.WEB_SERVER,
    dest="action",
    help="Also start the web interface.")

(options, args) = parser.parse_args()
action = options.action
control = Control()
print "Starting Tiberius Software Suite..."

#config write
#TiberiusConfigParser.setBatteryMonitorPort("/dev/ttyACM0")

# Start the database API if it is not already running
print "Checking if database is running..."
database = Popen("/home/pi/poly9.0/linux/raspi/bin/rtrdb -r data_service=8001 db", shell=True, stdout=PIPE)
time.sleep(5)

# Create database tables for data
print "Creating database tables for data"
c = DatabaseThreadCreator()
# Wait for the connection to the database to start
time.sleep(1)
cr.create_sensor_validity_table(c.poly)
ins.insert_initial_sensor_validity(c.poly)
cr.create_ultrasonics_validity_table(c.poly)
ins.insert_initial_ultrasonics_validity(c.poly)
cr.create_ultrasonics_table(c.poly)
cr.create_compass_table(c.poly)
cr.create_gps_table(c.poly)
cr.create_lidar_table(c.poly)
cr.create_arm_table(c.poly)
cr.create_motors_table(c.poly)
cr.create_steering_table(c.poly)
cr.create_battery_table(c.poly)

print 'Waiting for tables to finish being created...'
time.sleep(10)

print 'Starting sensor data threads...'
# Start sensor data threads
if TiberiusConfigParser.areUltrasonicsEnabled():
    print "ultrasonic thread starting"
    ultrasonics = Process(target=c.ultrasonics_thread).start()
    time.sleep(0.5)
if TiberiusConfigParser.isGPSEnabled():
    print "GPS thread starting"
    gps = Process(target=c.gps_thread).start()
    time.sleep(0.5)
if TiberiusConfigParser.isCompassEnabled():
    print "compass thread starting"
    compass = Process(target=c.compass_thread).start()
    time.sleep(0.5)
if TiberiusConfigParser.isLidarEnabled():
    print "lidar thread starting"
    lidar = Process(target=c.lidar_thread).start()
    time.sleep(0.5)

#if TiberiusConfigParser.isCompassEnabled() and TiberiusConfigParser.isGPSEnabled():
    #print "antenna thread starting"
    #antenna = Process(target=ant_thread).start()
    #time.sleep(0.5)
if TiberiusConfigParser.isArmCamEnabled():
    print "arm webcam thread starting"
    arm_camera_start = check_output("sudo service motion", shell=True)
if TiberiusConfigParser.isMonitorEnabled():
    print "battery monitor thread starting"
    powermanagement = Process(target=c.powermanagement_thread).start()

# Start the control API
# server = Popen("python tiberius/control_api/api.py", shell=True)
# print "Control API started"
if action == Action.WEB_SERVER:
    server = Popen("python tiberius/web-interface/manage.py runserver", shell=True)
    print "Web server started"

# Now run other stuff

print "Starting loop"
while True:
    #c.diagnostics_thread(control)
    compass_monitor(control)
    time.sleep(2)

# Wait for a keyboard interrupt
try:
    time.sleep(0.1)
except KeyboardInterrupt:
    print "Stopping Tiberius Software Suite..."
    print "Stopping ultrasonics process..."
    ultrasonics.terminate()
    print "Stopping compass process..."
    compass.terminate()
    print "Stopping gps process..."
    gps.terminate()
    print "Stopping diagnostics process..."
    diagnostics.terminate()
    if action == Action.WEB_SERVER:
        print "Stopping web server..."
        Popen.kill(server)
    print "Tiberius Software Suite Stopped"
sys.exit()



