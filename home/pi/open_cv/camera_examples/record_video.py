import cv2


# find the webcam

capture = cv2.VideoCapture(0)

# video recorder
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoOut = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))


# record video
while (capture.isOpened()):
    ret, frame = capture.read()
    if ret:
        videoOut.write(frame)
        cv2.imshow('Video Stream', frame)

    else:
         break

    # Tiny Pause
    key = cv2.waitKey(1)

capture.release()
videoOut.release()
cv2.destroyAllWindows()
