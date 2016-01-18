from tiberius.control.actuators import Motor

m = Motor()

print "front left(" + hex(m.front_left.address) + "): " +  str(m.front_left.version)
print "front right(" + hex(m.front_right.address) + "): "  + str(m.front_right.version)
print "rear left(" + hex(m.rear_left.address) + "): " + str(m.rear_left.version)
print "rear right(" + hex(m.rear_right.address) + "): " + str(m.rear_right.version)
