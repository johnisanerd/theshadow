# USAGE
# python detect.py --images images
# Original Tutorial: http://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/

# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import time

debug = True


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera

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
# Pi CAMERA OPTIONS
##########################################
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)
##########################################
'''


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--images", required=True, help="path to images directory")
#args = vars(ap.parse_args())

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
# imagePaths = list(paths.list_images(args["images"]))
# imagePaths = list(paths.list_images(args["images"]))

cv2.destroyAllWindows()


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
        print("x Avg: " + str(x_avg))
        print("y Avg: " + str(y_avg))
    
    MeanData(x_avg, y_avg)
    
    return x_avg, y_avg

if __name__ == '__main__':
    while True:
        # load the image and resize it to (1) reduce detection time
        # and (2) improve detection accuracy
        
        ##########################################
        ## VIDEO EXAMPLES OPTIONS
        ##########################################
        _,image = cap.read()
        orig = image.copy()
        ##########################################

        '''
        ##########################################
        # Pi CAMERA OPTIONS
        ##########################################
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        ##########################################
        '''
        
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
            padding=(8, 8), scale=1.05)

        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        
        print(find_center_mass(image, pick))
        
        # Draw a red circle representing the running average position.
        cv2.circle(image, (average_x, average_y), 5, (0,0,255), -1)
        
        # show some information on the number of bounding boxes
        # filename = imagePath[imagePath.rfind("/") + 1:]
        print("[INFO] : {} original boxes, {} after suppression".format(
            len(rects), len(pick)))

        # show the output image
        # cv2.imshow("Before NMS", orig)    # This is the original before treatment.
        cv2.imshow("After NMS", image)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
        print("==================================================")
    cv2.destroyAllWindows()