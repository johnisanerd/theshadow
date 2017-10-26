#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import threading

debug = True

'''

https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/stacking-hats

Board 0: Address = 0x60 Offset = binary 0000 (no jumpers required)
Board 1: Address = 0x61 Offset = binary 0001 (bridge A0)
Board 2: Address = 0x62 Offset = binary 0010 (bridge A1, the one above A0)
Board 3: Address = 0x63 Offset = binary 0011 (bridge A0 & A1, two bottom jumpers)
Board 4: Address = 0x64 Offset = binary 0100 (bridge A2, middle jumper)
'''

# create a default object, no changes to I2C address or frequency
mh1 = Adafruit_MotorHAT(addr=0x61)
#mh2 = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh1.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
	'''
	mh2.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
	'''

atexit.register(turnOffMotors)

# Initialize the Steppers
myStepper1 = mh1.getStepper(200, 1)       # 200 steps/rev, motor port #1, Mercury Motor
myStepper2 = mh1.getStepper(200, 2)       # 200 steps/rev, motor port #2
#myStepper3 = mh2.getStepper(200, 1)       # 200 steps/rev, motor port #3
#myStepper4 = mh2.getStepper(200, 2)       # 200 steps/rev, motor port #4

rpm = 50	# Max 50
# Setup Initial Speed
myStepper1.setSpeed(rpm)                 # 30 RPM
myStepper2.setSpeed(rpm)                 # 30 RPM
#myStepper3.setSpeed(rpm)                 # 30 RPM
#myStepper4.setSpeed(rpm)                 # 30 RPM

# Threading control of Steppers
def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    try:
		# Blocking
		# myStepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		# myStepper2.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		# myStepper3.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
		# myStepper4.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

		move = Adafruit_MotorHAT.DOUBLE
		# move = Adafruit_MotorHAT.INTERLEAVE
		# move = Adafruit_MotorHAT.SINGLE

		# Non-Blocking
		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 360, Adafruit_MotorHAT.FORWARD, move))
		st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 360, Adafruit_MotorHAT.FORWARD, move))
		#st3 = threading.Thread(target=stepper_worker, args=(myStepper3, 100, Adafruit_MotorHAT.FORWARD, move))
		#st4 = threading.Thread(target=stepper_worker, args=(myStepper4, 100, Adafruit_MotorHAT.FORWARD, move))
		st1.start()
		st2.start()
		#st3.start()
		#st4.start()

		#while st1.isAlive():
		#	time.sleep(1)
		while(st1.isAlive()):
			time.sleep(1)
		while(st2.isAlive()):
			time.sleep(1)

		# Non-Blocking
		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 360, Adafruit_MotorHAT.BACKWARD, move))
		st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 360, Adafruit_MotorHAT.BACKWARD, move))
		#st3 = threading.Thread(target=stepper_worker, args=(myStepper3, 100, Adafruit_MotorHAT.BACKWARD, move))
		#st4 = threading.Thread(target=stepper_worker, args=(myStepper4, 100, Adafruit_MotorHAT.BACKWARD, move))
		st1.start()
		st2.start()
		#st3.start()
		#st4.start()

		while(st1.isAlive()):
			time.sleep(1)
		while(st2.isAlive()):
			time.sleep(1)

		print("Loop over.")
    except Exception as e:
		if debug:
			print e
        	print("There was an exception.")

    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
    #print("Interleaved coil steps")
    #myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    #print("Microsteps")
    #myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
