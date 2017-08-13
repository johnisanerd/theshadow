#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import threading

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
mh2 = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh1.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh1.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

	mh2.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper1 = mh1.getStepper(200, 1)       # 200 steps/rev, motor port #1
myStepper1.setSpeed(400)                 # 30 RPM

myStepper2 = mh1.getStepper(200, 2)       # 200 steps/rev, motor port #2
myStepper2.setSpeed(400)                 # 30 RPM

myStepper3 = mh2.getStepper(200, 1)       # 200 steps/rev, motor port #3
myStepper3.setSpeed(400)                 # 30 RPM

myStepper4 = mh2.getStepper(200, 2)       # 200 steps/rev, motor port #4
myStepper4.setSpeed(400)                 # 30 RPM

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    #myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
    #print("Double coil steps")

    # Blocking
    myStepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
    myStepper2.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

    myStepper3.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
    myStepper4.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

    # Non-Blocking
    st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
    st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
    st3 = threading.Thread(target=stepper_worker, args=(myStepper3, 100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
    st4 = threading.Thread(target=stepper_worker, args=(myStepper4, 100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
    st1.start()
    st2.start()
    st3.start()
    st4.start()

    time.sleep(5)

    # Non-Blocking
    st1 = threading.Thread(target=stepper_worker, args=(myStepper1, 100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE))
    st2 = threading.Thread(target=stepper_worker, args=(myStepper2, 100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE))
    st3 = threading.Thread(target=stepper_worker, args=(myStepper3, 100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE))
    st4 = threading.Thread(target=stepper_worker, args=(myStepper4, 100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE))
    st1.start()
    st2.start()
    st3.start()
    st4.start()

    time.sleep(5)


    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
    #print("Interleaved coil steps")
    #myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
    #print("Microsteps")
    #myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    #myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
