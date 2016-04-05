
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
        port = '/dev/ttyACM1'
    baud = 250000
    m = 0.3
    n = 0.3
    # Time required to close and open the robotic gripper
    gripper_timeout = 5
    current_arm_angle = 0
    current_shoulder_angle = 0
    current_elbow_angle = 0

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

    def move_arm_to(self, x, y, z):
        arm_coords = to_arm_coords(x, y, z, self.m, self.n)
        self.ser.write("G0 X" + str(arm_coords[0]) + "Y" + str(arm_coords[1]) + "Z" + str(arm_coords[2]) + "\n")
        # Tell the RAMPS console to move the given GCODE

    def move_gripper(self, close):
        if close:
            self.ser.write("M280 P0 S0\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")
        else:
            self.ser.write("M280 P0 S90\n")
            time.sleep(self.gripper_timeout)
            self.ser.write("M280 P0 S75\n")

    def rotate_arm(self, change, angle=None):
        if angle:                               ##if angle provided
            self.current_arm_angle = angle       #move to that angle
        else:
            self.current_arm_angle += change      #move from current location by change
            if (self.current_arm_angle > 360 )      #normalize the angle
                self.current_arm_angle -= 360
            elif (self.current_arm_angle > 360 )
                self.current_arm_angle += 360
        self.ser.write("G0 Y" + str(current_arm_angle) + "\n")

    def move_shoulder(self, change, angle=None):
        if angle:
            self.current_shoulder_angle = angle
        else:
            self.current_shoulder_angle += change
            if (self.current_shoulder_angle > 360 )      #normalize the angle
                self.current_shoulder_angle -= 360
            elif (self.current_shoulder_angle > 360 )
                self.current_shoulder_angle += 360
        self.ser.write("G0 Z" + str(current_shoulder_angle) + "\n")

    def move_elbow(self, change, angle=None):
        if angle:
            self.current_elbow_angle = angle
        else:
            self.current_elbow_angle += change
            if (self.current_elbow_angle > 360 )      #normalize the angle
                self.current_elbow_angle -= 360
            elif (self.current_elbow_angle > 360 )
                self.current_elbow_angle += 360
        self.ser.write("G0 X" + str(current_elbow_angle) + "\n")

    def increase_arm_rotation();
        Y = Y + 10
