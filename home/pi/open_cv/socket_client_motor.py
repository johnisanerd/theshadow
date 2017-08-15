#!/usr/bin/python
#Adapted from https://pymotw.com/2/socket/tcp.html

import socket
import sys
import random
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import threading

debug = True    # Turn this on and off for development.

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

# Initialize the Steppers
myStepper1 = mh1.getStepper(200, 1)       # 200 steps/rev, motor port #1
myStepper2 = mh1.getStepper(200, 2)       # 200 steps/rev, motor port #2
myStepper3 = mh2.getStepper(200, 1)       # 200 steps/rev, motor port #3
myStepper4 = mh2.getStepper(200, 2)       # 200 steps/rev, motor port #4

# Setup Initial Speed
myStepper1.setSpeed(400)                 # 30 RPM
myStepper2.setSpeed(400)                 # 30 RPM
myStepper3.setSpeed(400)                 # 30 RPM
myStepper4.setSpeed(400)                 # 30 RPM

# Threading control of Steppers
def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

def send_motor_command(steps):
    try:
        print("Starting motors forward.")
        '''
        # Blocking
        myStepper1.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
        '''
        # Non-Blocking
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
        st3 = threading.Thread(target=stepper_worker, args=(myStepper3, steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
        st4 = threading.Thread(target=stepper_worker, args=(myStepper4, steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE))
        st1.start()
        st2.start()
        st3.start()
        st4.start()

        time.sleep(5)

    except:
        print("There was an exception.")

while True:
    ###############################################################################
    # Sockets
    ###############################################################################

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    ###############################################################################
    # End Sockets
    ###############################################################################
    data = ''

    try:
        # Poll for the motor data.
        amount_received = 0
        amount_expected = 1 #len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            if debug:
                print >> sys.stderr, 'received "%s"' % data

            time.sleep(1)

    finally:
        if debug:
            print >>sys.stderr, 'closing socket'
        sock.close()

    # Parse out the x, y coordinates
    x_coord = int(data[0:3])
    y_coord = int(data[4:7])
    if debug:
        print("x_coord: " + str(x_coord))
        print("y_coord: " + str(y_coord))
    send_motor_command(x_coord)
