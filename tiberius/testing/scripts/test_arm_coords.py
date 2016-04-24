from tiberius.control.actuators import to_arm_coords

try:
    print to_arm_coords(0, -0.2, -0.3, 0.3, 0.3)
except ValueError:
    print 'Arm cannot reach that location'
