import math


def to_arm_coords(x, y, z, m, n):
    # We cannot handle the arm going straight up or down, it breaks the math (divide by 0)
    if x == 0 and y == 0:
        print 'Invalid Position - Must not be straight up'
        return

    theta = 0.0  # Rotation around base
    rho = 0.0  # Angle of elevation from base (Shoulder)
    sigma = 0.0  # Angle of elbow

    # Calculate base rotation
    theta = math.atan2(x, y)

    # -180->180    ->     0->360
    theta = math.degrees(theta)
    if theta < 0:
        theta += 360

    # Calculate angle of elbow
    sigma = math.acos(
        (math.pow(m, 2) + math.pow(n, 2) - (math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))) / (2 * m * n))

    # Temporary variables for rho calculation
    j = (math.pow(m, 2) + (math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)) - math.pow(n, 2)) / (
    2 * m * math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))
    k = (math.sqrt(math.pow(x, 2) + math.pow(y, 2)))

    l = math.atan(z / k)
    rho = l + math.acos(j)

    return [theta, math.degrees(rho), math.degrees(sigma)]
