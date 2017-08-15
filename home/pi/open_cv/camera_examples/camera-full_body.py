# From https://stackoverflow.com/questions/34871294/full-body-detection-and-tracking-using-opencvpython-2-7
# Picamera Reference: http://picamera.readthedocs.io/en/release-1.10/api_exc.html

# To Toggle between example videos and pi camera, simply uncomment sections out.


import numpy as np
import cv2
import time

debug = False

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

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

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


# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes	
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")
    

if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    while True:
        ##########################################
        ## VIDEO EXAMPLES OPTIONS
        ##########################################
        _,frame=cap.read()
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

        
        # found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(8,8), scale=1.05)
        # print found
        # print "W: " + str(w)
        found_filtered = non_max_suppression_fast(found, 0.3)
        draw_detections(frame,found_filtered)
        try:
            print "Center mass: " + str(find_center_mass(frame,found))
        except:
            print "Probably found a zero error."
            
        # Draw a red circle representing the running average position.
        cv2.circle(frame, (average_x, average_y), 5, (0,0,255), -1)
        
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(10)
        if ch == 27:
            break
        print "=================================================="
    cv2.destroyAllWindows()
