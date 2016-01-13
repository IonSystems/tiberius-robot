from tiberius.control.actuators import Motor

m = Motor()

print "front left: " + str(m.front_left.version())
print "front right: " + str(m.front_right.version())
print "rear left: " + str(m.rear_left.version())
print "rear right: " + str(m.rear_right.version())
