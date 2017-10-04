# Send motor data to the Arduino over Serial.

import time
import serial
import atexit
import socket
import sys
import random
import signal

timeout_time_m = 15                  # Minutes to timeout the whole process.  Feeds to timeout_time_s

port_number = 10011
server_1_name = 'camera1.local'
server_2_name = 'camera2.local'

socket_timeout = 2                   # 2 Second timeout on socket listening.
debug_socks_on = True                # Turn this off and on to show the debug outputs.

camera_1_last_socket_data_received = ""
camera_2_last_socket_data_received = ""

camera_1_average_x = 0.0
camera_1_average_y = 0.0
camera_1_people_count = 0.0

camera_2_average_x = 0.0
camera_2_average_y = 0.0
camera_2_people_count = 0.0

##########################################################################
#########################################################################
# Randomness

random_min_sec = 5
random_max_sec = 30

##########################################################################
#########################################################################


##########################################################################
#########################################################################
# Timeout
# NOTE: BE SURE THERE IS NO CONFLICT WITH RANDOMNESS!

timeout_time_s = 60*timeout_time_m
# timeout_time_s = 5

def timeouthandler(signum, frame):
   print "Timed out!"
   raise Exception("Timeout Exception: Timed out!")

signal.signal(signal.SIGALRM, timeouthandler)

def timeout_start():
    signal.alarm(timeout_time_s)

def timeout_end():
    signal.alarm(0)
##########################################################################
#########################################################################

try:
    arduinoSerialData = serial.Serial('/dev/ttyACM0',2000000)
except Exception as e:
    arduinoSerialData = serial.Serial('/dev/ttyACM1',2000000)
finally:
    pass


def atexit_shutdown_serial():
    arduinoSerialData.close()

atexit.register(atexit_shutdown_serial)

# Debug function for sockets
def debug_sockets(string_in):
    if debug_socks_on:
        print("Debug Sockets: # " + string_in)

# Debug function for motors
def debug_motors(string_in):
    if debug_socks_on:
        print("Debug Motors: # " + string_in)

# Read data from the serial line.
def readSerial():
    while arduinoSerialData.inWaiting == 0:  # Or: while ser.inWaiting():
        print "Waiting on serial line."

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


##########################################################################
#########################################################################
# Sockets: Here is our socket data.
def get_socket_data(server_number):
    global camera_1_last_socket_data_received
    global camera_2_last_socket_data_received

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Timeout in seconds
    # Connect the socket to the port where the server is listening
    if(server_number == 1):
        server_address = (server_1_name, port_number)
    else:
        server_address = (server_2_name, port_number)

    debug_sockets('connecting to %s port %s' % server_address)
    debug_sockets("Server Address: " + str(server_address))

    try:
        sock.connect(server_address)
        # Look for the response
        amount_received = 0
        amount_expected = 1 #len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            debug_sockets('received "%s"' % data)
            time.sleep(1)
        debug_sockets("Got Data!")
        if(server_number == 1):
            camera_1_last_socket_data_received = str(data)   # Pass the socket data over.
        else:
            camera_2_last_socket_data_received = str(data)   # Pass the socket data over.

        debug_sockets('closing socket')

    except Exception,e:
        debug_sockets("Client exception: " + str(e))
        sock.close()

    finally:
        sock.close()


# The function in which we take the last socket data and
# turn it into actual data.
def parse_socket_data():
    global camera_1_last_socket_data_received
    global camera_2_last_socket_data_received

    global camera_1_average_x
    global camera_1_average_y
    global camera_1_people_count

    global camera_2_average_x
    global camera_2_average_y
    global camera_2_people_count

    # Break out the socket data we received.
    try:
        camera_1_average_x = float(camera_1_last_socket_data_received.split(',')[0])
        camera_1_average_y = float(camera_1_last_socket_data_received.split(',')[1])
        camera_1_people_count = float(camera_1_last_socket_data_received.split(',')[2])
    except:
        print("Parsing Data Error Camera 1 Server.")

    try:
        camera_2_average_x = float(camera_2_last_socket_data_received.split(',')[0])
        camera_2_average_y = float(camera_2_last_socket_data_received.split(',')[1])
        camera_2_people_count = float(camera_2_last_socket_data_received.split(',')[2])
    except:
        print("Parsing Data Error Camera 2 Server.")

# This function can run with dummy tests on camera1.local and camera2.local.
# demos receiving the correct information and parsing it.

def dummy_socket_test():
    get_socket_data(1)
    get_socket_data(2)
    parse_socket_data()
    debug_sockets("C1 AvgX: " + str(camera_1_average_x))
    debug_sockets("C1 AvgX: " + str(camera_1_average_y))
    debug_sockets("C1 Count: " + str(camera_1_people_count))
    debug_sockets("C2 AvgX: " + str(camera_2_average_x))
    debug_sockets("C2 AvgX: " + str(camera_2_average_y))
    debug_sockets("C2 Count: " + str(camera_2_people_count))

##########################################################################
#########################################################################
# Scenarios: These are True/False statements that take in the x, y average,
# and the people count.  If the scenario fits, it simply returns true or
# false.

# Example Scenario 1:  More than 11 people on camera 2.
def scenario_1(x_avg1, y_avg1, count1, x_avg2, y_avg2, count2):
    # Here's our test

    test_case = count2 > 30

    if test_case:
        print("Found Test Case 1 Scenario TRUE!")
        return True
    else:
        return False

##########################################################################
#########################################################################
# Motors:  Test all the scenarios and the run the "run_motors" program.

# The motor run is always the same.  Call this and run the motors.
def run_motors():

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    debug_motors("Go Forward.")
    go_forward()
    go_stop()

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    # Sleep for a random amount of time.
    sleepy_time = random.randint(random_min_sec, random_max_sec)
    time.sleep(sleepy_time)

    debug_motors("Go Backward.")
    go_backward()
    go_stop()

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    debug_motors("Stop.")
    go_stop()

def test_for_run_motors():
    if scenario_1(camera_1_average_x, camera_1_average_y, camera_1_people_count, camera_2_average_x, camera_2_average_y, camera_2_people_count):
        run_motors()

while True:
    print("Starting the loop!")
    print("#################")
    timeout_start()     #  Start with the timeout timer!  If the loop takes
                        # Too long to complete, we'll start over.
    # Everything is in a try loop to make sure that we are protected by timeouts!
    try:

        # Always start the loop with a stop.
        print("Stop.")
        go_stop()

        get_socket_data(1)  # Poll for socket data and update camera_x_average_x/y
        get_socket_data(2)  # Poll for socket data and update camera_x_average_x/y
        parse_socket_data()

        test_for_run_motors()

    except:
        print("==========Timed out!===========")
        timeout_start()

    print("==Ending the Loop!============")
    print("==============================")


def testing_junkyard():

        # dummy_socket_test()   # Run the dummy sockets test to test network.

    '''
    print("Starting the loop!")
    print("#################")
    try:
        print("Testing timeout on!")
        time.sleep(20)

    except:
        print("==========Timed out!===========")
        timeout_start()

    '''
