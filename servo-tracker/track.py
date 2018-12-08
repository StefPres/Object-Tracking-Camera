# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import argparse
import cv2
import imutils
import time
import serial

arduino = serial.Serial('/dev/ttyACM0', 115200)
screenx = 480
screeny = 360
obsize = 8
loopstart = 0
loopend = 0
horiz = ""
vert = ""

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    print "grabbing video"
    #vs = VideoStream(src=0).start()
    camera = PiCamera()
    camera.resolution = (screenx, screeny)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(screenx, screeny))

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array
    # handle the frame from VideoCapture or VideoStream
    #frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        print "broke while loop"
        break


    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > obsize:
            # draw the circle and centroid on the frame,
            # then update the list of tracked poi
            centerx = int(x)
            centery = int(y)
            if(centerx > (screenx*2/3)):
                print("right")
                horiz = "right"
            elif((centerx >= (screenx/3)) and (centerx <= (screenx*2/3))):
                print("horizontal center")
                horiz = "center"
            else:
                print("left")
                horiz = "left"

            if(centery > (screeny*2/3)):
                print("down")
                vert = "down"
            elif((centery >= (screeny/3)) and (centery <= (screeny*2/3))):
                print("center")
                vert = "center"
            else:
                print('up')
                vert = "up"
            arduino.write(horiz + "," + vert + "\n")


    # show the frame to our screen and increment the frame counter
    #cv2.imshow("Frame", frame)
    #key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    #if key == ord("q"):
    #   break
    rawCapture.truncate(0)

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
#cv2.destroyAllWindows()
