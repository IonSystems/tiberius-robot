from optparse import OptionParser
from subprocess import Popen, PIPE
from tiberius.control.control_thread import ControlThread
from multiprocessing import Process
from enum import Enum
import sys
import time


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
control_thread = ControlThread()
control_thread.polycreate_sensor_validity()
control_thread.polycreate_ultrasonics_validity()
control_thread.polycreate_ultrasonic()
control_thread.polycreate_compass()
control_thread.polycreate_gps()


# Start sensor data threads
ultrasonics = Process(target=control_thread.ultrasonics_thread).start()
compass = Process(target=control_thread.compass_thread).start()
gps = Process(target=control_thread.gps_thread).start()

# Start the control API
print "Starting the control API..."
server = Popen("python tiberius/control_api/api.py", shell=True)
print "Control API started"

if action == Action.WEB_SERVER:
    print "Starting the web server..."
    server = Popen("python tiberius/web-interface/manage.py runserver", shell=True)
    print "Web server started"

# Wait for a keyboard interrupt
try:
    time.sleep(0.1)
except KeyboardInterrupt:
    print "Stopping Tiberius Software Suite..."
    print "Stopping ultrasonics process..."
    assert isinstance(ultrasonics, Process)
    ultrasonics.terminate()
    print "Stopping compass process..."
    compass.terminate()
    if action == Action.WEB_SERVER:
        print "Stopping web server..."
        Popen.kill(server)
    print "Tiberius Software Suite Stopped"
sys.exit()
