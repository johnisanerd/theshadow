#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

'''

https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/stacking-hats

Board 0: Address = 0x60 Offset = binary 0000 (no jumpers required)
Board 1: Address = 0x61 Offset = binary 0001 (bridge A0)
Board 2: Address = 0x62 Offset = binary 0010 (bridge A1, the one above A0)
Board 3: Address = 0x63 Offset = binary 0011 (bridge A0 & A1, two bottom jumpers)
Board 4: Address = 0x64 Offset = binary 0100 (bridge A2, middle jumper)
'''

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x63)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myMotor = mh.getMotor(3)

# set the speed to start, from 0 (off) to 255 (max speed)
max_speed = 125
myMotor.setSpeed(max_speed)

print "Forward! "
myMotor.run(Adafruit_MotorHAT.FORWARD)

print "\tSpeed up..."
for i in range(max_speed):
    myMotor.setSpeed(i)
    time.sleep(0.01)

#time.sleep(10)
while (True):
	print "Forward! "
	myMotor.run(Adafruit_MotorHAT.FORWARD)

	print "\tSpeed up..."
	for i in range(255):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print "\tSlow down..."
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		time.sleep(0.01)
