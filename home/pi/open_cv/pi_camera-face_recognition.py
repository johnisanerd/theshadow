
'''

THIS EXAMPLE ONLY READS THE FRONT OF THE FACE.


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
from random import randint

debug = False

'''
##########################################
## VIDEO EXAMPLES OPTIONS
##########################################
#cap = cv2.VideoCapture('Gallery-1.mp4')
cap = cv2.VideoCapture('Gallery-2.mp4')#
#cap = cv2.VideoCapture('Gallery-3.mp4')
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
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_eye.xml')

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
    
    if debug:
        print("Modulo: " + str(array_pos))
        print("X_List: " + str(x_list))
        print("Y_List: " + str(y_list))
        print("X_List Sum: " + str(sum(x_list)))
        print("Y_List Sum: " + str(sum(y_list)))
        print("Average X: " + str(average_x))
        print("Average Y: " + str(average_y))

##########################################
##########################################
    
    
# This function calculates the middle of the crowd
def find_center_mass(img, rects):
    # Totals so we can average the math out.
    x_total = 0
    y_total = 0
    for x, y, w, h in rects:
        x_total = x + (x_total + (w/2))
        y_total = y + (y_total + (h/2))
    #Average the totals out
    x_avg = x_total/len(rects)
    y_avg = y_total/len(rects)
    
    if debug:
        print "x Avg: " + str(x_avg)
        print "y Avg: " + str(y_avg)
    
    MeanData(x_avg, y_avg)
    
    return x_avg, y_avg

def face_analyze(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        
        # The code below generated a random number on the face
        # random_number = str(randint(0,99999999))
        # cv2.putText(gray,random_number,(x,y+h), font, 1,(255,255,255),2)
    print(faces)
    try:
        print(find_center_mass(gray, faces))
    except Exception,e: 
        print("No Face Found!")
        if debug:
            print str(e)
    
    # Draw a red circle representing the running average position.
    cv2.circle(gray, (average_x, average_y), 5, (0,0,255), -1)

    return gray

time.sleep(1)

while(True):
    
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

    cv2.imshow('img',face)
    # cv2.imshow('img',frame)
    # out.write(face)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break 

# Release everything if job is finished
cap.release()
# out.release()
cv2.waitKey(0)
cv2.destroyAllWindows()