# Send motor data to the Arduino over Serial.
######

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
# Minimum and maximum time that the random number generator will use to
# stay open or stay closed.

random_open_min_sec = 1*60   # Open for 1 minute minimum
random_open_max_sec = 5*60   # Open for 5 minutes maximum

random_close_min_sec = 1*60   # Open for 1 minute minimum
random_close_max_sec = 5*60   # Open for 5 minutes maximum

'''
random_open_min_sec = 10   # Open for 1 minute minimum
random_open_max_sec = 10   # Open for 5 minutes maximum

random_close_min_sec = 5   # Open for 1 minute minimum
random_close_max_sec = 5   # Open for 5 minutes maximum
'''
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
        debug_motors("Tried Go_Forward and haven't gotten a response.")
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
        debug_motors("Tried Go_Backward and haven't gotten a response.")
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

    '''
    try:
        camera_2_average_x = float(camera_2_last_socket_data_received.split(',')[0])
        camera_2_average_y = float(camera_2_last_socket_data_received.split(',')[1])
        camera_2_people_count = float(camera_2_last_socket_data_received.split(',')[2])
    except:
        print("Parsing Data Error Camera 2 Server.")
    '''

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



##########################################################################
#########################################################################
# Motors:  Test all the scenarios and the run the "run_motors" program.

# The motor run is always the same.  Call this and run the motors.
def motors_open():

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    debug_motors("Go Forward.")
    go_forward()
    go_stop()

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    # Sleep for a random amount of time.
    sleepy_time = random.randint(random_open_min_sec, random_open_max_sec)
    debug_motors("Randomly Sleep for " + str(sleepy_time) + " seconds. ")
    debug_motors("Randomly Sleep for " + str(sleepy_time/60.0) + " minutes. ")

    time.sleep(sleepy_time)

def motors_close():
    debug_motors("Go Backward.")
    go_backward()
    go_stop()

    debug_motors("Get Information from Switch Bank")
    debug_motors(get_info())

    # Sleep for a random amount of time.
    sleepy_time = random.randint(random_close_min_sec, random_close_max_sec)
    debug_motors("Randomly Sleep for " + str(sleepy_time) + " seconds. ")
    debug_motors("Randomly Sleep for " + str(sleepy_time/60.0) + " minutes. ")
    time.sleep(sleepy_time)
    debug_motors("Stop.")
    go_stop()

# This will run and test the camera data for the scenarios we want to run.
# If we find a scenario that matches, we run it.
def test_for_run_motors():
    # X Positioning:
    # 20    - Door
    # 115   - Halfway between door and people
    # 270   - people
    # 412   - Halfway between pole and parachute
    # 500   - parachute
    debug_motors("Avg  X: " + str(camera_1_average_x))
    debug_motors("Avg  Y: " + str(camera_1_average_y))
    debug_motors("People: " + str(camera_1_people_count))
    # Here's our test
    debug_motors("Run Tests on Data.")
    # Test 1:   Are there less than three people in the room?
    #           Is the average position less than 115?

    if((camera_1_people_count < 3) and (camera_1_average_x < 300)):
        print("Found Test Case 1 Scenario TRUE!  Average is near the door.")
        motors_open()
    # Test 2:   Are there more than three people in the room?
    #           Is the average position less than 270?
    elif((camera_1_people_count > 3) and (camera_1_average_x < 270 )):
        print("More than 3 people in the room.  Average is behind the post.")
        motors_open()
    # Test 3:   Are there less three people in the room?
    #           Is the average position greater than 270?
    elif((camera_1_people_count < 3) and (camera_1_average_x >= 300 )):
        print("Less than 3 people in the room.  Average is in front of the post.")
        motors_close()
    # Test 4:   Are there more than three people in the room?
    #           Is the average position greater than 270?
    elif((camera_1_people_count > 3) and (camera_1_average_x >= 270 )):
        print("Less than 3 people in the room.  Average is in front of the post.")
        motors_close()
    else:
        print("No Scenario matched.  Nothing to change!")
        motors_close()

while True:

    # dummy_socket_test()   # Run the dummy sockets test to test network.

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
        # get_socket_data(2)  # Poll for socket data and update camera_x_average_x/y
        parse_socket_data()

        test_for_run_motors()

    except Exception as e:
        print(e)
        print("==========Errored out!===========")
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
