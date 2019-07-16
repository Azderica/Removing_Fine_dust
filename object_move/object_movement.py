# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import math
import numpy as np
import argparse
import cv2
import imutils
import time
import socket
import threading

# this is for socket
my_ip_address = '192.168.43.160'
my_port = 9009
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((my_ip_address, my_port))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
redLower = (0, 80, 80)
redUpper = (10, 255, 255)
blueLower = (40, 100, 100)
blueUpper = (80, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
i_rad = 0
rad = 0
plus = 0
# (dX, dY) = (0, 0)
direction = ""
sendData = ""
radius = 0
radius2 = 0

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=1).start()

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
sock.send('camera'.encode('utf-8'))
time.sleep(2.0)

end = False


def send_coor(second=1.0):
	global end
	if end:
		return
	threading.Timer(second, send_coor, [second]).start()
	sock.send(sendData.encode('utf-8'))

#send_coor(10.0)


# keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video

	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	blurred2 = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	hsv2 = cv2.cvtColor(blurred2, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, blueLower, blueUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	mask2 = cv2.inRange(hsv2, redLower, redUpper)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	# cv2.imshow("blue circle", mask)
	# cv2.imshow("red circle", mask2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                         cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)
	cnts2 = imutils.grab_contours(cnts2)
	center2 = None

	# only proceed if at least one contour was found
	if len(cnts) > 0 and len(cnts2) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		c2 = max(cnts2, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
		M = cv2.moments(c)
		M2 = cv2.moments(c2)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 0.5 and radius2 > 0.5:
			# draw the circlqe and centroid on the frsame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.circle(frame, (int(x2), int(y2)), int(radius2),
                            (0, 255, 255), 2)
			cv2.circle(frame, center2, 5, (0, 0, 255), -1)
			pts.appendleft(center)
			pts.appendleft(center2)

	if (not center) or (not center2):
		center = (190, 190)
		center2 = (200, 200)

	d_1 = center2[1]-center[1]
	d_0 = center2[0]-center[0]
	rad = math.atan2(d_1, d_0)

	cv2.putText(frame, "Blue X: {}, Blue Y: {}".format(center[0], center[1]),
             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
             0.35, (0, 255, 255), 1)
	cv2.putText(frame, "Red X: {}, Red Y: {}, Radian: {}".format(center2[0], center2[1], rad),
             (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
             0.35, (0, 255, 255), 1)

	if rad > 0:
		plus = 1
	else:
		plus = 0
	i_rad = int(rad*10000)

	sendData = (str(center[0]) + "," + str(center[1]) +
	            "," + str(i_rad) + ","+str(plus))
	time.sleep(2)
	sock.send(sendData.encode('utf-8'))
	#send_coor(10.0)

	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
