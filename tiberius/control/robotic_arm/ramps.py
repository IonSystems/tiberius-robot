from tiberius.control.robotic_arm.cartesian import to_arm_coords
import serial
from tiberius.utils import detection
import logging
import time


class RoboticArmDriver:
    """
        Class to interface the stepper motors with the robotic arm using RAMPS
        This will be using GCODE as used in 3D printers
        All joints are using stepper motors except for the gripper which uses a servo
    """

    if detection.detect_windows():
        port = 'COM6'
    else:
        port = '/dev/ttyACM0'
    baud = 115200
    m = 0.3
    n = 0.3
    # Time required to close and open the robotic gripper
    gripper_timeout = 5

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control.robotic_arm.RoboticArmDriver')
        self.logger.info('Creating an instance of RoboticArmDriver')
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
        except serial.serialutil.SerialException as e:
            self.logger.error(e)
            raise serial.serialutil.SerialException

        try:
            self.ser.open()
        except:
            self.logger.warning("Serial port already open continuing.")

    def move_waist(self, angle):
        self.ser.write("G0 X" + str(angle) + "\n")

    def move_shoulder(self, angle):
        self.ser.write("G0 Y" + str(angle) + "\n")

    def move_elbow(self, angle):
        self.ser.write("G0 Z" + str(angle) + "\n")

    def move_arm_to(self, x, y, z):
        arm_coords = to_arm_coords(x, y, z, self.m, self.n)
        self.ser.write("G0 X" + str(arm_coords[0]) + "Y" + str(arm_coords[1]) + "Z" + str(arm_coords[2]) + "\n")
<<<<<<< HEAD
        # Tell the RAMPS console to move the given GCODE
=======
>>>>>>> e50d856ed6bfde256bc57052da8c2cd3ac92ad27

    def move_gripper(self, close):
        if close:
            self.ser.write("M280 P0 S0\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")
        else:
            self.ser.write("M280 P0 S90\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")
