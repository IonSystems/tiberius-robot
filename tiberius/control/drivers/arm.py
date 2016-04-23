from tiberius.control.robotic_arm.cartesian import to_arm_coords
from tiberius.utils import detection
import serial
import logging
import time
from tiberius.config.config_parser import TiberiusConfigParser


class RoboticArmDriver:
    """
        Class to interface the stepper motors with the robotic arm using RAMPS
        This will be using GCODE as used in 3D printers
        All joints are using stepper motors except for the gripper which uses a servo
    """

    if detection.detect_windows():
        port = 'COM6'
    else:
        port = TiberiusConfigParser.getArmSerialPort()
    baud = 19200

    # Time required to close and open the robotic gripper
    gripper_timeout = 5

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control.robotic_arm.RoboticArmDriver')
        self.logger.info('Creating an instance of RoboticArmDriver')
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
        except serial.serialutil.SerialException as e:
            self.logger.error(e)

        try:
            self.ser.open()
        except:
            self.logger.warning("Serial port already open continuing.")

    def move_joints_to(self, rotation, shoulder, elbow):
        self.ser.write("G0 X" + str(rotation) + "Y" + str(shoulder) + "Z" + str(elbow) + "\n")

    def move_gripper(self, close):
        if close:
            self.ser.write("M280 P0 S0\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")
        else:
            self.ser.write("M280 P0 S90\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")

    def home_x(self):
        self.ser.write("G28 X")

    def home_y(self):
        self.ser.write("G28 Y")

    def home_z(self):
        self.ser.write("G28 Z")

    def rotate_arm(self, angle):
        self.ser.write("G0 X" + str(angle) + "\n")

    def move_shoulder(self, angle):
        self.ser.write("G0 Y" + str(angle) + "\n")

    def move_elbow(self, angle):
        self.ser.write("G0 Z" + str(angle) + "\n")
