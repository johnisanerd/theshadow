# Send motor data to the Arduino over Serial.

import time
import serial
import atexit
try:
    arduinoSerialData = serial.Serial('/dev/ttyACM0',2000000)
except Exception as e:
    arduinoSerialData = serial.Serial('/dev/ttyACM1',2000000)
finally:
    pass


def atexit_shutdown_serial():
    arduinoSerialData.close()

atexit.register(atexit_shutdown_serial)

# Read data from the serial line.
def readSerial():
    while arduinoSerialData.inWaiting == 0:  # Or: while ser.inWaiting():
        print "Waiting"

    output_string = ""
    try:
        bytesToRead = arduinoSerialData.inWaiting()
        output_string = arduinoSerialData.read(bytesToRead)
        # print(output_string)
        #break;
    except:
        print "Error reading."
        #break;
    return output_string

# Write a string to the serial line.
def writeSerial(var):
    try:
        arduinoSerialData.write(var)
    except Exception as e:
        print("ERROR: " + str(e))

# This Function stops the motors
def go_stop():
    data_in = ""
    while('1' not in data_in):
        writeSerial("1")        # Send the number "1" and you'll stop.
        time.sleep(1)
        data_in = readSerial()
        time.sleep(0.5)
    info = data_in
    return info

# This Function Moves the Motors Forward
def go_forward():
    data_in = ""
    while('2' not in data_in):
        writeSerial("2")        # Send the number "2" and you'll go forward.
        time.sleep(1)
        data_in = readSerial()
        time.sleep(0.5)
        print("Tried Go_Forward and haven't gotten a response.")
    info = data_in
    return info

# This Function Moves the Motors Backward
def go_backward():
    data_in = ""
    while('3' not in data_in):
        writeSerial("3")        # Send the number "3" and you'll go backward.
        time.sleep(1)
        data_in = readSerial()
        time.sleep(0.5)
        print("Tried Go_Backward and haven't gotten a response.")
    info = data_in
    return info

# This Function Gets the Status of the Switch Bank
def get_info():
    data_in = ""
    while('4' not in data_in):
        writeSerial("4")        # Send the number "4" and you'll get the info back.
        time.sleep(1)
        data_in = readSerial()
        time.sleep(0.5)
    info = data_in.splitlines()[1]
    return info


while 1:
    print("Stop.")
    go_stop()
    time.sleep(5)

    print("Get Information from Switch Bank")
    print(get_info())

    print("Go Forward.")
    go_forward()
    go_stop()

    print("Get Information from Switch Bank")
    print(get_info())

    print("Go Backward.")
    go_backward()
    go_stop()

    print("Get Information from Switch Bank")
    print(get_info())

    print("Stop.")
    go_stop()
