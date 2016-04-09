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

print "Starting Tiberius Software Suite..."

# Start the database API if it is not already running
print "Checking if database is running..."
database = Popen("/home/pi/poly9.0/linux/raspi/bin/rtrdb -r data_service=8001 db", shell=True, stdout=PIPE)
lines_iterator = iter(database.stdout.readline, b"")
for line in lines_iterator:
    if line == "Ready":
        print "Database started successfully"
        break
    if "Failed" in line:
        print "Database already running"
        break

# Create database tables for data
print "Creating database tables for data"
c = DatabaseThreadCreator()
# Wait for the connection to the database to start
time.sleep(2)
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

print 'Waiting for tables to finish being created...'
time.sleep(10)

print 'Starting sensor data threads...'
# Start sensor data threads
ultrasonics = Process(target=c.ultrasonics_thread).start()
print "ultrasonic thread started"
time.sleep(5)
#gps = Process(target=c.gps_thread).start()
print "GPS thread started"
#time.sleep(5)
if TiberiusConfigParser.isCompassEnabled():
    compass = Process(target=c.compass_thread).start()
    print "compass thread started"
#time.sleep(5)
if TiberiusConfigParser.isLidarEnabled():
    lidar = Process(target=c.lidar_thread).start()
    print "lidar thread started"
time.sleep(5)
#diagnostics = Process(target=c.diagnostics_thread()).start()
#time.sleep(5)

# Start the control API
#server = Popen("python tiberius/control_api/api.py", shell=True)
#print "Control API started"

if action == Action.WEB_SERVER:
    server = Popen("python tiberius/web-interface/manage.py runserver", shell=True)
    print "Web server started"

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

print "tiberius fully started"
