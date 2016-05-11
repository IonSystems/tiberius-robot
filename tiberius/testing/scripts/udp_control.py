import sys
from tiberius.logger import logger
from tiberius.control.drivers import motor_udp
import logging
d_logger = logging.getLogger('tiberius.testing.udp_control')
import tty
import termios
import time

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
    while(True):

        key = getKey()
        d_logger.debug("Key %s pressed", key)
        if(key == 'c'):
            motor_udp.stop()
            sys.exit(0)
        elif(key == 'C'):
            motor_udp.stop()
            sys.exit(0)
        elif(key == 'w'):
            motor_udp.send_motor_speed_fl(50)
            motor_udp.send_motor_speed_fr(50)
            motor_udp.send_motor_speed_rr(50)
            motor_udp.send_motor_speed_rl(50)
        elif(key == 'W'):
            motor_udp.send_motor_speed_fl(100)
            motor_udp.send_motor_speed_fr(100)
            motor_udp.send_motor_speed_rr(100)
            motor_udp.send_motor_speed_rl(100)
        elif(key == 'a'):
            motor_udp.skid_left(20)
        elif(key == 'A'):
            motor_udp.skid_left(40)
        elif(key == 's'):
            motor_udp.send_motor_speed_fl(-50)
            motor_udp.send_motor_speed_fr(-50)
            motor_udp.send_motor_speed_rr(-50)
            motor_udp.send_motor_speed_rl(-50)
        elif(key == 'S'):
            motor_udp.send_motor_speed_fl(-100)
            motor_udp.send_motor_speed_fr(-100)
            motor_udp.send_motor_speed_rr(-100)
            motor_udp.send_motor_speed_rl(-100)
        elif(key == 'd'):
            motor_udp.skid_right(20)
        elif(key == 'D'):
            motor_udp.skid_right(40)
        elif(key == ' '):
            motor_udp.stop()
            time.sleep(0.1)
