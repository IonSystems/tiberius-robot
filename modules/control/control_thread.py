import thread

'''
    Responsible for creating threads to communicate with the database, in order to control Tiberius.
'''

class ControlThread:

    def __init__(self, motor_control = True, lighting_control = True, gps_control = True, lidar_control = True, keyboard_control = True, compass_control = True, ultrasonic_control = True):
        #Find out what threads need to be created.
        self.motor_control = motor_control
        self.lighting_control = lighting_control
        self.gps_control = gps_control
        self.lidar_control = lidar_control
        self.keyboard_control = keyboard_control
        self.compass_control = compass_control
        self.ultrasonic_control = ultrasonic_control

        def create_motor_control_thread(self):
            thread.start_new_thread ( function, args[, kwargs] )
