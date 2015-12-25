import os

import sys

sys.path.insert(0,'../../control')
from control import Control

c = Control()
if __name__ == "__main__":
	c.motors.stop()
