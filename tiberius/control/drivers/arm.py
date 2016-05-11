from tiberius.utils import detection
import serial
import logging
import time
from tiberius.config.config_parser import TiberiusConfigParser


class RoboticArmDriver:
    """
        Class to interface with the robotic arm
        This is using G-code

        Useful reference for all commands used:
        http://reprap.org/wiki/G-code
        The board is running a custom version of Marlin with a RAMPS1.4 board, DRV8825 stepper drivers and
        a DRV8838 Motor driver
    """

    if detection.detect_windows():
        port = 'COM6'
    else:
        port = TiberiusConfigParser.getArmSerialPort()
    baud = 19200

    # Time required to close and open the robotic gripper
    gripper_timeout = 1  # A value of 1 gives about 6 positions for the gripper

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
        self.ser.write("G0 X" + str(rotation) + " Y" + str(shoulder) + " Z" + str(elbow) + "\n")

    def move_gripper(self, close):
        if close:
            self.ser.write("M42 P42 S255\n")  # Close
            self.ser.write("M42 P44 S255\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M42 P44 S0\n")
        else:
            self.ser.write("M42 P42 S0\n")  # Open
            self.ser.write("M42 P44 S255\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M42 P44 S0\n")

    # The light uses the direction pin on the gripper driver so it will go on and off when the motor is running
    def set_light(self, state):
        if state:
            self.ser.write("M42 P42 S0\n")  # On
        else:
            self.ser.write("M42 P42 S255\n")  # Off

    def home_x(self):
        self.ser.write("G28 X \n" )

    def home_y(self):
        self.ser.write("G28 Y \n")

    def home_z(self):
        self.ser.write("G28 Z \n")

    def rotate_arm(self, angle):
        self.ser.write("G0 X" + str(angle) + "\n")

    def move_shoulder(self, angle):
        self.ser.write("G0 Y" + str(angle) + "\n")

    def move_elbow(self, angle):
        self.ser.write("G0 Z" + str(angle) + "\n")
