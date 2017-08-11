#Adapted from https://pymotw.com/2/socket/tcp.html

import socket
import sys
import random
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow us to reuse addresses.
# https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow us to reuse addresses.


# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address

while True:
    try:
        sock.bind(server_address)
        break
    except:
        print "Connection refused, try again in 5 seconds."
        time.sleep(5)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >> sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    # atexit.register(connection.close())
    try:
        print >> sys.stderr, 'connection from', client_address

        data1 = str(random.randint(111,999))
        data2 = str(random.randint(111,999))
        data_joined = data1 + "," + data2
        print data_joined
        #data_joined = 'Hello'
        # connection.sendall('HELLO')
        connection.sendall(data_joined)
        # Receive the data in small chunks and retransmit it
        '''
        while True:

            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            '''

    finally:
        # Clean up the connection
        connection.close()
