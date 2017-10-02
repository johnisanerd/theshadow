# This is for testing scenarios where you need a socket server.
# For example, run this to develop the motor_control.py program.

import time
import random
import socket
import sys
import threading
import atexit

##########################################
# CONTROL VARIABLES
##########################################
port_number = 10011
socket_timeout = 2                   # 2 Second timeout on socket listening.
debug_socks_on = True                # Turn this off and on to show the debug outputs.

average_x       = 10.001
average_y       = 105.001
people_count    = 10

# Debug function for sockets
def debug_sockets(string_in):
    if debug_socks_on:
        print("Debug Sockets:" + string_in)

##########################################
# Sockets Setup
##########################################
# Create a TCP/IP socket
socket.setdefaulttimeout(socket_timeout)    # Set the socket timeout for listening.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow us to reuse addresses.
# https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow us to reuse addresses.

# Bind the socket to the port
server_address = ('localhost', port_number)
debug_sockets("Starting up on %s port %s" % server_address)

while True:
    try:
        sock.bind(server_address)
        break
    except:
        debug_sockets("Connection refused, try again in 5 seconds.")
        time.sleep(5)

# Listen for incoming connections
sock.listen(1)

##########################################
# End Sockets Setup
##########################################

def socket_server():
    ##########################################
    # Sockets
    ##########################################

    # Wait for a connection
    debug_sockets("Waiting for a connection.")
    try:
        connection, client_address = sock.accept()

        debug_sockets("Connection from " + str(client_address))

        # Format the data so that it's always 3 digits wide.
        x_data = str('%03.0f' % average_x)
        y_data = str('%03.0f' % average_y)

        data_joined = str(x_data) + "," + str(y_data) + "," + str(people_count)
        debug_sockets( data_joined)

        connection.sendall(data_joined)

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        # Clean up the connection
        connection.close()
    except socket.error, exc:
        debug_sockets("Uncaught Socket Error: " + str(exc))
    except Exception,e:
        debug_sockets("Listening exception: " + str(e))
        # No need to close a connection here?
    finally:
        # Clean up the connection
        try:
            connection.close()
        except Exception,e:
            debug_sockets("Ucaught exception: " + str(e))

    ##########################################
    # End Sockets
    ##########################################

while True:
    # Start the server threading.
    try:
        server_thread = threading.Thread(target=socket_server)
        if not server_thread.isAlive():
            server_thread.start()
            debug_sockets("Server thread dead, starting.")
        else:
            debug_sockets("Server thread alive, not starting.")
        server_thread.join()
    except Exception,e:
        debug_sockets("Start the server threading. Exception: " + str(e))
