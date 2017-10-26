# Send motor data to the Arduino over Serial.

import time
import serial
import atexit

arduinoSerialData = serial.Serial('/dev/ttyACM0',2000000)

def atexit_shutdown_serial():
    arduinoSerialData.close()


atexit.register(atexit_shutdown_serial)

def readSerial():
    while arduinoSerialData.inWaiting == 0:  # Or: while ser.inWaiting():
        print "Waiting"

    try:
        bytesToRead = arduinoSerialData.inWaiting()
        print(arduinoSerialData.read(bytesToRead))
        #break;
    except:
        print "Error reading."
        #break;

while 1:
    var = raw_input("Please enter: ")
    arduinoSerialData.write(var)
    time.sleep(1)
    readSerial()
