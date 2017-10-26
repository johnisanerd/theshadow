# This is for testing scenarios where you need a socket client.
# For example, run this to develop the socket_server_camera.py program.
# Only gathers data for Camera1.local!

import socket
import sys
import time

port_number = 10011
server_1_name = 'camera1.local'
# server_1_name = 'localhost'
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

# Debug function for sockets
def debug_sockets(string_in):
    if debug_socks_on:
        print("Debug Sockets:" + string_in)

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
    '''
    try:
        camera_2_average_x = float(camera_2_last_socket_data_received.split(',')[0])
        camera_2_average_y = float(camera_2_last_socket_data_received.split(',')[1])
        camera_2_people_count = float(camera_2_last_socket_data_received.split(',')[2])
    except:
        print("Parsing Data Error Camera 2 Server.")
    '''

while True:
    time.sleep(5)
    get_socket_data(1)
    # get_socket_data(2)
    parse_socket_data()
    debug_sockets("C1 AvgX: " + str(camera_1_average_x))
    debug_sockets("C1 AvgY: " + str(camera_1_average_y))
    debug_sockets("C1 Count: " + str(camera_1_people_count))
    '''
    debug_sockets("C2 AvgX: " + str(camera_2_average_x))
    debug_sockets("C2 AvgX: " + str(camera_2_average_y))
    debug_sockets("C2 Count: " + str(camera_2_people_count))
    '''
    debug_sockets("==============================")
