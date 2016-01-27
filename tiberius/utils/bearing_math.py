def normalize_bearing(bearing):
	while bearing > 180.0 or bearing < -180.0:
		if bearing > 180.0:
			bearing -= 360.0
		elif bearing < -180.0:
			bearing += 360.0
	return bearing
