import sys
from tiberius.control.control import Control

import logging

d_logger = logging.getLogger('tiberius.testing.keyboard_control')
import tty
import termios
import time
import traceback

c = Control()
arm_control_mode = 'direct'


def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == "__main__":
    while True:
        try:
            key = getKey()
            d_logger.debug("Key %s pressed", key)
            # to exit
            if key == 'c':
                c.motors.stop()
                sys.exit(0)
            elif key == 'C':
                c.motors.stop()
                sys.exit(0)
            # for driving around
            elif key == 'w':
                c.motors.setSpeedPercent(50)
                c.motors.moveForward()
            elif key == 'W':
                c.motors.setSpeedPercent(100)
                c.motors.moveForward()
            elif key == 'a':
                c.motors.setSpeedPercent(50)
                c.motors.turnLeft()
            elif key == 'A':
                c.motors.setSpeedPercent(100)
                c.motors.turnLeft()
            elif key == 's':
                c.motors.setSpeedPercent(50)
                c.motors.moveBackward()
            elif key == 'S':
                c.motors.setSpeedPercent(100)
                c.motors.moveBackward()
            elif key == 'd':
                c.motors.setSpeedPercent(50)
                c.motors.turnRight()
            elif key == 'D':
                c.motors.setSpeedPercent(100)
                c.motors.turnRight()

            # to stop
            elif key == ' ':
                c.motors.stop()
                time.sleep(0.1)

            # ARM CONTROL
            # Cartesian control

            elif key == 'u' and arm_control_mode == 'cartesian':  # x increase
                c.arm.move_x(0.01)
            elif key == 'j' and arm_control_mode == 'cartesian':  # x decrease
                c.arm.move_x(-0.01)
            elif key == 'i' and arm_control_mode == 'cartesian':  # y increase
                c.arm.move_y(0.01)
            elif key == 'k' and arm_control_mode == 'cartesian':  # y decrease
                c.arm.move_y(-0.01)
            elif key == 'o' and arm_control_mode == 'cartesian':  # z increase
                c.arm.move_z(0.01)
            elif key == 'l' and arm_control_mode == 'cartesian':  # z decrease
                c.arm.move_z(-0.01)

            # Direct control

            elif key == 'u':  # waist increase
                c.arm.rotate_waist(2)
            elif key == 'j':  # waist decrease
                c.arm.rotate_waist(-2)
            elif key == 'i':  # shoulder increase
                c.arm.move_shoulder(2)
            elif key == 'k':  # shoulder decrease
                c.arm.move_shoulder(-2)
            elif key == 'o':  # elbow increase
                c.arm.move_elbow(2)
            elif key == 'l':  # elbow decrease
                c.arm.move_elbow(-2)
            elif key == 'p':  # Park
                c.arm.park()
            elif key == 'P':  # Centre
                c.arm.centre()
            elif key == 'h':  # Home
                c.arm.home()
            elif key == 'H':  # Force Home - if the arm is in a weird position and not homed properly
                c.arm.home(True)

            # Arm control modes

            elif key == '#':  # Direct arm joint control
                print 'Direct arm joint control'
                arm_control_mode = 'direct'
            elif key == '~':  # Cartesian arm join control
                print 'Cartesian arm joint control'
                arm_control_mode = 'cartesian'

            # Gripper control

            elif key == 'm':  # Close gripper
                print 'Closing gripper'
                c.arm.close_gripper()
            elif key == 'M':  # Force close gripper - for resetting position
                print 'Forcing close gripper must be run to new fully closed position'
                c.arm.close_gripper(True)
            elif key == 'n':  # Open gripper
                print 'Opening gripper'
                c.arm.open_gripper()
            elif key == 'n':  # Force open gripper- for resetting position
                print 'Forcing open gripper must be run to new fully open position'
                c.arm.open_gripper(True)

            # Light control

            elif key == ']':  # Light on
                c.arm.change_arm_light(True)
            elif key == '}':  # Light off
                c.arm.change_arm_light(False)

        except Exception as e:  # Print out any errors that occur, saves us having to restart the script if we
                                # accidentally hit a key
            print 'An error occurred:'
            traceback.print_exc()
            print e
