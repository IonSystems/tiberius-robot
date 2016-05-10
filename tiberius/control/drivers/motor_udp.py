#! /usr/bin/env python
from socket import *
from struct import *
import time

# Send UDP broadcast packets
#TODO: Get these from config file
mbed_port = 43442
mbed_ip = "10.113.211.245"
mbed_address = (mbed_ip, mbed_port)

"""********************************************
		Constant Definitions
********************************************"""

#Define UDP destinations
DEST_LOCAL = "\x00"
DEST_CANBUS = "\x40"

#System commands
P_GAIN = "\x00"
LED_TOGGLE = "\x01"
MOTOR_SPEED = "\x02"
MOTOR_PWM = "\x03"
STEERING_MOVE_REL = "\x04"
STEERING_MOVE_ABS = "\x05"
STEERING_ANGLE = "\x05"

#Slave address
FRONT_RIGHT = "\x01\x01\x00\x00"
FRONT_LEFT = "\x00\x01\x00\x00"
REAR_LEFT = "\x02\x01\x00\x00"
REAR_RIGHT = "\x03\x01\x00\x00"

#Skip sequences
SKIP_5 = "\x00\x00\x00\x00\x00"
SKIP_7 = "\x00\x00\x00\x00\x00\x00\x00"

#Motor speeds
SPEED_0 = "\x00"
SPEED_50 = "\x32"
SPEED_100 = "\x64"

#Motor direction
DIR_CW = "\x00"
DIR_ACW = "\x01"

#CAN byte length
CAN_BYTES_1 = "\x01\x00\x00\x00"
CAN_BYTES_3 = "\x03\x00\x00\x00"

"""********************************************
		UDP Socket
********************************************"""
def send_udp_data_raw(data):
	s = socket(AF_INET, SOCK_DGRAM)
	print "Sending " + str(data) + " to " + str(mbed_address)
	bytes_sent = s.sendto(data, mbed_address)
	print "Bytes sent = " + str(bytes_sent)

def format_data(data):
	return bytearray(data)

def print_bytes(data):
	data = format_data(data)
	for byte in data:
 		print byte

"""********************************************
		Send Commands
********************************************"""
def send_led_toggle_slave(motor_address):
	data = DEST_CANBUS + motor_address + LED_TOGGLE + SKIP_7 + CAN_BYTES_1
	send_udp_data_raw(data)

def send_led_toggle_bridge():
	data = DEST_LOCAL + LED_TOGGLE
	send_udp_data_raw(data)

def send_motor_speed(motor_speed, motor_direction, motor_address):
	#Convert motor speed to byte if an int is given
	if isinstance(motor_speed, int):
		motor_speed = speed_convert(motor_speed)

	data = DEST_CANBUS + motor_address + MOTOR_PWM + \
		motor_direction + motor_speed + SKIP_5 + \
		CAN_BYTES_3
	send_udp_data_raw(data)

def send_motor_speed_fr(motor_speed):
	"""
		Sets motor speed for front right motor.
		motor_speed: Integer value between -100 and 100
	"""
	motor_speed, motor_direction = speed_dir_convert(motor_speed)
	send_motor_speed(motor_speed, motor_direction, FRONT_RIGHT)

def send_motor_speed_fl(motor_speed):
	"""
		Sets motor speed for front left motor.
		motor_speed: Integer value between -100 and 100
	"""
	motor_speed, motor_direction = speed_dir_convert(motor_speed)
	send_motor_speed(motor_speed, motor_direction, FRONT_LEFT)

def send_motor_speed_rr(motor_speed):
	"""
		Sets motor speed for rear right motor.
		motor_speed: Integer value between -100 and 100
	"""
	motor_speed, motor_direction = speed_dir_convert(motor_speed)
	send_motor_speed(motor_speed, motor_direction, REAR_RIGHT)

def send_motor_speed_rl(motor_speed):
	"""
		Sets motor speed for rear left motor.
		motor_speed: Integer value between -100 and 100
	"""
	motor_speed, motor_direction = speed_dir_convert(motor_speed)
	send_motor_speed(motor_speed, motor_direction, REAR_LEFT)

def speed_dir_convert(motor_speed):
	if motor_speed > 0:
		motor_direction = DIR_CW
	elif motor_speed <= 0:
		motor_direction = DIR_ACW

	motor_speed = speed_convert(abs(motor_speed))
	return motor_speed, motor_direction

def speed_convert(speed_int):
	if isinstance(speed_int, int):
		if speed_int > 100:
			speed_int = 100
		elif speed_int < 0:
			speed_int = 0
	else:
		#Default to 50% if invalid speed param
		speed_int = 50
	return pack('B', speed_int)

def stop():
	send_motor_speed(SPEED_0, DIR_CW, FRONT_RIGHT)
	send_motor_speed(SPEED_0, DIR_CW, FRONT_LEFT)
	send_motor_speed(SPEED_0, DIR_CW, REAR_RIGHT)
	send_motor_speed(SPEED_0, DIR_CW, REAR_LEFT)

"""********************************************
		Debug
********************************************"""

if __name__ == "__main__":

	while(False):
		print "Forward"
		send_led_toggle_slave(FRONT_RIGHT)
		send_motor_speed(SPEED_100, DIR_CW, FRONT_RIGHT)
		time.sleep(1)
		print "Backward"
		send_led_toggle_slave(FRONT_RIGHT)
		send_motor_speed(SPEED_100, DIR_ACW, FRONT_RIGHT)
		time.sleep(1)
		print "Stop"
		send_led_toggle_slave(FRONT_RIGHT)
		send_motor_speed(SPEED_0, DIR_CW, FRONT_RIGHT)
		time.sleep(1)

	#send_motor_speed(100, DIR_CW, FRONT_RIGHT)
	send_motor_speed_rl(100)
	send_motor_speed_rl(-100)
