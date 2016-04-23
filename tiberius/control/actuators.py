import time

from tiberius.config.config_parser import TiberiusConfigParser

import math


def to_arm_coords(x, y, z, m, n):
    # Cartesian control is only for use in front of tiberius
    # So we must limit the values that can be used
    '''
    if x < -50 or x > 50:
        print 'Invalid  X Position'
        return

    if y < 30 or y > 70:
        print 'Invalid  Y Position'
        return

    if z < -40 or z > 50:
        print 'Invalid  Z Position'
        return
    '''
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

    # Now we must convert these angles into what the arm actually needs to do, since this is for an 'ideal' arm ie it
    # can go from 0 to 360 on every joint

    # for the base we need to rotate the whole thing by the angle to the center, which on Tiberius 3 is 145 degrees



    theta -= 153



    # The same must be done for the other two joins

    # The added numbers are the offset that the arm cannot travel too.

    # Since the shoulder joint can go below horizontal we  add some to make it properly horizontal
    rho = math.degrees(rho) + 52  # This is the angle from horizontal to the first arm segment

    # Since the elbow joint cannot go inline with the lower arm segment we need to take away the difference
    sigma = math.degrees(sigma) - 80  # This is the angle from the first arm segment
    # to the second at the bottom. ie so it forms a set of triangles

    # We then round the result to remove the pointless precision
    print [round(theta, 2), round(rho, 2), round(sigma, 2)]

    if theta > 300 or theta < 0:
        print 'Cannot move to that position'
        return
    if rho > 210 or rho < 0:
        print 'Cannot move to that position'
        return
    if sigma > 205 or sigma < 0:
        print 'Cannot move to that position'
        return

    return [round(theta, 2), round(rho, 2), round(sigma, 2)]


if TiberiusConfigParser.isArmEnabled():
    import drivers.arm as robotic_arm
    from tiberius.database.decorators import database_arm_update


    class Arm:
        """
        .. module:: actuators
           :synopsis: Provides access to all actuators supported by Tiberius.
           This most importantly includes the motors to drive Tiberius's wheels.

        .. moduleauthor:: Cameron A. Craig <camieac@gmail.com>
        """
        __config = TiberiusConfigParser()
        arm = robotic_arm.RoboticArmDriver()
        positions = {
            'park': __config.getArmParkParams(),
            'centre': __config.getArmCentreParams(),
            'basket': __config.getArmBasketParams(),
            'home': __config.getArmHomeParams(),
        }

        # We must home before doing anything else or anything could happen
        homed = False
        cartesian_usable = False

        # Store current position of each joint
        waist_angle = 0
        shoulder_angle = 0
        elbow_angle = 0

        # Store cartesian coordinates
        x = 0
        y = 0
        z = 0

        arm_shoulder_elbow_length = 0.3
        arm_elbow_gripper_length = 0.3

        def move_x(self, amount):
            if not self.cartesian_usable:
                print 'Arm must be homed and centered first before using cartesian control'
                return
            self.x += amount
            self.cartesian_move()

        def move_y(self, amount):
            if not self.cartesian_usable:
                print 'Arm must be homed and centered first before using cartesian control'
                return
            self.y += amount
            self.cartesian_move()

        def move_z(self, amount):
            if not self.cartesian_usable:
                print 'Arm must be homed and centered first before using cartesian control'
                return
            self.z += amount
            self.cartesian_move()

        def cartesian_move(self):
            if not self.cartesian_usable:
                print 'Arm must be homed and centered first before using cartesian control'
                return
            new_position = to_arm_coords(self.x, self.y, self.z, self.arm_shoulder_elbow_length,
                                         self.arm_elbow_gripper_length)
            self.waist_angle = new_position[0]
            self.shoulder_angle = new_position[1]
            self.elbow_angle = new_position[2]

            self.arm.move_joints_to(self.waist_angle, self.shoulder_angle, self.elbow_angle)



        def set_position_to(self, position):
            p = self.positions[position]
            self.waist_angle = p['x']
            self.shoulder_angle = p['y']
            self.elbow_angle = p['z']

        def home(self):
            # We home in reverse order to make sure the arm is in front of tiberius for the x home which will stop
            # us from hitting anything
            self.arm.home_z()
            time.sleep(2)
            self.arm.home_y()
            time.sleep(2)
            self.arm.home_x()
            time.sleep(2)
            self.set_position_to('home')
            print 'Please wait for homing to complete...'
            # It is quite hard to figure out when homing is done so just wait for a reasonable amount of time
            time.sleep(4)

            self.homed = True;

        def park(self):
            if not self.homed:
                print 'Arm must be homed first'
                return
            '''
                Move the arm to the parked position,
                for safe storage whilst not in use.
            '''
            # Move arm out of harms way
            self.arm.move_joints_to(self.waist_angle, 100, 100)

            # Move arm to parking position
            self.arm.home_x()
            p = self.positions['park']
            self.arm.move_joints_to(p['x'], p['y'], p['z'])

            # Close gripper
            self.arm.move_gripper(True)
            self.set_position_to('park')

        def centre(self):
            if not self.homed:
                print 'Arm must be homed first'
                return
            '''
                Bring the arm round to the centre position, ready to use.
            '''
            # Move arm out of harms way
            self.arm.move_joints_to(self.waist_angle, 100, 100)

            # Move arm to centre position
            p = self.positions['centre']
            self.arm.move_joints_to(p['x'], p['y'], p['z'])
            self.set_position_to('centre')
            self.cartesian_usable = True;
            self.x = 0
            self.y = -0.5
            self.z = 0

        def basket(self):
            if not self.homed:
                print 'Arm must be homed first'
                return
            '''
                Swing the arm round around over the basket and ungrasp,
                then return to the old position.
            '''
            # Move arm out of harms way
            self.arm.move_joints_to(self.waist_angle, 100, 100)

            # Move arm to parking position
            self.arm.home_x()
            p = self.positions['park']
            self.arm.move_joints_to(p['x'], p['y'], p['z'])

            # Close gripper
            self.arm.move_gripper(True)
            self.set_position_to('basket')

        # get the points location
        def get_waist(self):
            return self.waist_angle

        def get_shoulder(self):
            return self.shoulder_angle

        def get_elbow(self):
            return self.elbow_angle

        @database_arm_update
        def rotate_waist(self, change, angle=None):
            if not self.homed:
                print 'Arm must be homed first'
                return
            if angle:
                self.waist_angle = angle
            else:
                self.waist_angle += change  # move from current location by change
                if self.waist_angle > 300:  # normalize the angle
                    self.waist_angle = 300
                elif self.waist_angle < 0:
                    self.waist_angle = 0
            print str(self.waist_angle)
            self.arm.rotate_arm(self.waist_angle)
            time.sleep(0.05)

        @database_arm_update
        def move_shoulder(self, change, angle=None):
            if not self.homed:
                print 'Arm must be homed first'
                return
            if angle:
                self.shoulder_angle = angle
            else:
                self.shoulder_angle += change
                if self.shoulder_angle > 210:  # normalize the angle
                    self.shoulder_angle = 210
                elif self.shoulder_angle < 0:
                    self.shoulder_angle = 0
            print str(self.shoulder_angle)
            self.arm.move_shoulder(self.shoulder_angle)
            time.sleep(0.8)

        @database_arm_update
        def move_elbow(self, change, angle=None):
            if not self.homed:
                print 'Arm must be homed first'
                return
            if angle:
                self.elbow_angle = angle
            else:
                self.elbow_angle += change
                if self.elbow_angle > 205:  # normalize the angle
                    self.elbow_angle = 205
                elif self.elbow_angle < 0:
                    self.elbow_angle = 0
            print str(self.elbow_angle)
            self.arm.move_elbow(self.elbow_angle)
            time.sleep(0.05)

if TiberiusConfigParser.areMotorsEnabled():
    import drivers.md03 as md03
    from states import MotorState
    from tiberius.database.decorators import database_motor_update


    class Motor:
        '''
                Tiberius's four motors.
                Contains basic motor movement methods.
                Does not contain any feedback.
        '''
        __config = TiberiusConfigParser()

        front_left = md03.MotorDriver(__config.getMotorFrontLeftAddress())
        rear_left = md03.MotorDriver(__config.getMotorRearLeftAddress())
        front_right = md03.MotorDriver(__config.getMotorFrontRightAddress())
        rear_right = md03.MotorDriver(__config.getMotorRearRightAddress())

        state = MotorState.STOP

        # 0 - 255
        speed = 255
        accel = 0

        def setSpeedPercent(self, speed_percent):
            self.speed = (255 * speed_percent) / 100

        @database_motor_update
        def stop(self):
            self.front_left.move(0, 0)
            self.rear_left.move(0, 0)
            self.front_right.move(0, 0)
            self.rear_right.move(0, 0)
            self.state = MotorState.STOP

        @database_motor_update
        def moveForward(self):
            self.front_left.move(self.speed, self.accel)
            self.rear_left.move(self.speed, self.accel)
            self.front_right.move(self.speed, self.accel)
            self.rear_right.move(self.speed, self.accel)
            self.state = MotorState.FORWARD

        @database_motor_update
        def moveBackward(self):
            self.front_left.move(-self.speed, self.accel)
            self.rear_left.move(-self.speed, self.accel)
            self.front_right.move(-self.speed, self.accel)
            self.rear_right.move(-self.speed, self.accel)
            self.state = MotorState.BACKWARD

        # Turn on the spot, to the right
        @database_motor_update
        def turnRight(self):
            self.front_left.move(self.speed, self.accel)
            self.rear_left.move(self.speed, self.accel)
            self.front_right.move(-self.speed, self.accel)
            self.rear_right.move(-self.speed, self.accel)
            self.state = MotorState.RIGHT

        # Turn on the spot, to the left
        @database_motor_update
        def turnLeft(self):
            self.front_right.move(self.speed, self.accel)
            self.rear_left.move(-self.speed, self.accel)
            self.front_left.move(-self.speed, self.accel)
            self.rear_right.move(self.speed, self.accel)
            self.state = MotorState.LEFT

        # Used for going forward accurately by adjusting left and right speeds.
        @database_motor_update
        def moveForwardDualSpeed(self, left_speed, right_speed):
            left_speed = self.__clipSpeedValue(left_speed)
            right_speed = self.__clipSpeedValue(right_speed)

            self.front_right.move(right_speed, self.accel)
            self.front_left.move(left_speed, self.accel)
            self.rear_right.move(right_speed, self.accel)
            self.rear_left.move(left_speed, self.accel)

            # TODO:This is unsafe! could be going forwards,backwards,left or right
            self.state = MotorState.FORWARD

        # Used for going forward accurately by adjusting left and right speeds.
        # TODO: The database takes the unclipped speeds! Make a decorator
        # for clipping speeds so the correct args can be passed to database.
        @database_motor_update
        def moveIndependentSpeeds(
                self,
                front_left,
                front_right,
                rear_left,
                rear_right):
            front_left = self.__clipSpeedValue(front_left)
            front_right = self.__clipSpeedValue(front_right)
            rear_left = self.__clipSpeedValue(rear_left)
            rear_right = self.__clipSpeedValue(rear_right)

            self.front_left.move(front_left, self.accel)
            self.front_right.move(front_right, self.accel)
            self.rear_left.move(rear_left, self.accel)
            self.rear_right.move(rear_right, self.accel)

            # TODO: This is unsafe! could be going forwards,backwards,left or right
            self.state = MotorState.FORWARD

        def __clipSpeedValue(self, speed):
            if speed > 255:
                speed = 255
            elif speed < -255:
                speed = -255
            return speed
