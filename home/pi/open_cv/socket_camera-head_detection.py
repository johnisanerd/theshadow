
'''
1. This example detects heads in view.
2. This example serves up the average x,y on a socket.
Note: Webcam works best!

THIS EXAMPLE ONLY READS THE FRONT and the side of the head.
Webcam works best!


"Brute Force" method.

	K-Nearest Neighbor. - Idea is to search for closest match of the test data in feature space.

	Face Detection using Haar Cascads -
	Haar-cascade Detection in OpenCV. OpenCV comes with a trainer as well as detector. If you want to train your own classifier for any object like car, planes etc. you can use OpenCV to create one. Its full details are given here: Cascade Classifier Training. Here we will deal with detection.
	http://docs.opencv.org/master/d7/d8b/tutorial_py_face_detection.html

	https://www.youtube.com/watch?v=WfdYYNamHZ8
	'''

import numpy as np
import cv2
import time
import random
import numpy as np
import socket
import sys
import threading
import atexit

##########################################
# CONTROL VARIABLES
##########################################
port_number = 10002
socket_timeout = 2                   # 2 Second timeout on socket listening.
debug_video_on = True                # Turn this off and on to show the debug outputs.
debug_socks_on = True                # Turn this off and on to show the debug outputs.
show_output = False         # Turn this off and on to show the picture output.
##########################################

# Debug function for video
def debug_video(string_in):
    if debug_video_on:
        print("Debug Video:" + string_in)

# Debug function for sockets
def debug_sockets(string_in):
    if debug_socks_on:
        print("Debug Sockets:" + string_in)

'''
##########################################
## VIDEO EXAMPLES OPTIONS
##########################################
#cap = cv2.VideoCapture('Gallery-1.mp4')
#cap = cv2.VideoCapture('Gallery-2.mp4')#
cap = cv2.VideoCapture('Gallery-3.mp4')
#cap = cv2.VideoCapture(0)
##########################################
'''

##########################################
## WEBCAM OPTIONS
##########################################
cap = cv2.VideoCapture(0)
##########################################

'''
##########################################
# Pi CAMERA OPTIONS
##########################################
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
##########################################
'''

# allow the camera to warmup
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
head_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_profileface.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

##########################################
# Weighting functions.
##########################################
average_x = 0   # Average position of x
average_y = 0   # Average position of y
array_position = 0

x_list = [0,0]   # Starting array with 0's
y_list = [0,0]   # Starting array with 0's

list_max_size = 20  # The maximum size of the array of position data.

# This function will calculate a running average of the position of the head.
# The running average position is stored in a global array and will be used with cv2.circle to draw a circle on the picture, and eventually control the servos/motors.
def MeanData(new_x_value, new_y_value):
    global array_position
    global x_list
    global y_list
    global average_x, average_y

    array_position = array_position + 1     # Increase the Array Position!
    array_pos = array_position % list_max_size   # Calculate the modulo

    # Check that list size is less than max_list_size     # If it's not, just tack it on at the end of the list.
    if len(x_list) < list_max_size:
        x_list.append(new_x_value)  # Tack on the new value to the list.
    else:
        # If it's larger, divide and place in the modulo.
        x_list[array_pos] = new_x_value

    if len(y_list) < list_max_size:
        y_list.append(new_y_value)  # Tack on the new value to the list.
    else:
        # If it's larger, divide and place in the modulo.
        y_list[array_pos] = new_y_value

    # Calculate the running average.
    average_x = sum(x_list)/len(x_list)
    average_y = sum(y_list)/len(y_list)

    debug_video("Modulo: " + str(array_pos))
    debug_video("X_List: " + str(x_list))
    debug_video("Y_List: " + str(y_list))
    debug_video("X_List Sum: " + str(sum(x_list)))
    debug_video("Y_List Sum: " + str(sum(y_list)))
    debug_video("Average X: " + str(average_x))
    debug_video("Average Y: " + str(average_y))

##########################################
##########################################


# This function calculates the middle of the crowd
def find_center_mass(img, faces, heads):
    # Totals so we can average the math out.
    # Max Window Height is 0 - 400
    # Max Window Widgth is
    image_height, image_width = img.shape[:2]
    debug_video("Image Dimensions: " + str(image_height) + ", " + str(image_width))

    x_total = 0
    y_total = 0
    for x, y, w, h in faces:
        x_total = x + (x_total + (w/2))
        y_total = y + (y_total + (h/2))
    for x, y, w, h in heads:
        x_total = x + (x_total + (w/2))
        y_total = y + (y_total + (h/2))
    #Average the totals out
    x_avg = x_total/(len(faces)+len(heads))
    y_avg = y_total/(len(faces)+len(heads))

    debug_video("x Avg: " + str(x_avg))
    debug_video("y Avg: " + str(y_avg))

    MeanData(x_avg, y_avg)

    return x_avg, y_avg

# This function finds the faces and the side faces.
def face_analyze(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    heads = head_cascade.detectMultiScale(gray, 1.3, 5)


    for (x,y,w,h) in faces:
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

        '''
        # The code below generated a random number on the face
        # random_number = str(randint(0,99999999))
        # cv2.putText(gray,random_number,(x,y+h), font, 1,(255,255,255),2)
        '''

    for (x,y,w,h) in heads:
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
    try:
        center_mass_of_face = find_center_mass(gray, faces, heads)
        debug_video(center_mass_of_face)
    except Exception,e:
        debug_video("No Face Found! " + str(e))

    # Draw a red circle representing the running average position.
    cv2.circle(gray, (average_x, average_y), 5, (0,0,255), -1)

    return gray

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

        data_joined = str(x_data) + "," + str(y_data)
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


##########################################
# At Exit Commands
##########################################

def atexit_shutdown_camera():
    # Release everything if job is finished
    debug_video("CAMERA SHUTDOWN CALLED.")
    cap.release()
    # out.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    debug_video("CAMERA SHUTDOWN FINISHED.")

atexit.register(atexit_shutdown_camera)
##########################################
# End At Exit Commands
##########################################

while(True):

    try:
        ##########################################
        ## WEBCAM OPTIONS
        ##########################################
        # Capture frame-by-frame
        ret, frame = cap.read()  # returns a bool (True/False). If frame is read correctly, it will be True. So you can check end of the video by checking this return value.
        ##########################################

        '''
        ##########################################
        # Pi CAMERA OPTIONS
        ##########################################
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array
        ##########################################
        '''

        face = face_analyze(frame)
        if show_output:
            cv2.imshow('img',face)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break
    # except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    #    atexit_shutdown_camera()
    except Exception,e:
        debug_video("Exit the loop with error " + str(e))
    #    atexit_shutdown_camera()

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
