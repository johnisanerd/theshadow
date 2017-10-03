# Send motor data to the Arduino over Serial.

import time
import serial
import atexit
import socket
import sys

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
        print("Debug Sockets:" + string_in)

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


##########################################################################
#########################################################################
# Scenarios: These are True/False statements that take in the x, y average,
# and the people count.  If the scenario fits, it simply returns true or
# false.

def scenario_1(x_avg, y_avg, count):
    # Here's our test
    if(x_avg < 250 and y_avg > 100):
        return True
    else:
        return False

while True:

    # Always start the loop with a stop.
    print("Stop.")
    go_stop()
    time.sleep(5)



    '''
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
    '''

    get_socket_data(1)
    get_socket_data(2)
    parse_socket_data()
    debug_sockets("C1 AvgX: " + str(camera_1_average_x))
    debug_sockets("C1 AvgX: " + str(camera_1_average_y))
    debug_sockets("C1 Count: " + str(camera_1_people_count))
    debug_sockets("C2 AvgX: " + str(camera_2_average_x))
    debug_sockets("C2 AvgX: " + str(camera_2_average_y))
    debug_sockets("C2 Count: " + str(camera_2_people_count))
    debug_sockets("==============================")
