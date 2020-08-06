import cv2
from imutils import paths
import numpy as np
import imutils
import os

def find_marker(image):
	# converting the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	# detecting the image
	bgrl = np.array([170, 120, 70], np.uint8)  # took masking value by masking in previous example and taking the values
	bgrh = np.array([180, 255, 255], np.uint8)  # storing the masking color values in the array of unsigned integer 8
	# COLOR MASKING
	mask = cv2.inRange(gray, bgrl, bgrh)  # masking so as to be more efficient
	edged = cv2.Canny(mask, 35, 125)
	cv2.imshow('canny', edged)

	# finding the contour in image
	contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	# finding the largest contour in image
	c = max(contours, key = cv2.contourArea)

	# returning the boundary box
	return cv2.minAreaRect(c)

def distance_to_camera(objWdth, fclLnth, perWdth):
	# calculating distance between camera and object
	return (objWdth * fclLnth) / perWdth

# object pre-defined distance from the camera
objDist = 15

# object pre-defined width
objWdth = 2.3

# reading pre-defined image
image = cv2.imread("images/1.jpg")
# finding contour in image
marker = find_marker(image)
# manipulating focal length through pre-defined data
fclLnth = (marker[1][0] * objDist) / objWdth
print('fclLnth : ', fclLnth)

cap = cv2.VideoCapture(0)

while True:
	ret, image = cap.read(0)
	marker = find_marker(image)
	# finding distance
	distInch = distance_to_camera(objWdth, fclLnth, marker[1][0])
	# drawing a box around the image
	box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(image, [box], -1, (255, 255, 0), 3)
	# displaying output on image
	cv2.putText(image, "%.2f Inch" % (distInch), (80, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 0), 3)
	print("Image-",  ": %.2f Inch" % (distInch))
	# full-screen window
	cv2.namedWindow('image- ', cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty('image- ', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	# displaying image

	cv2.imshow('image', image)
	if cv2.waitKey(1500) == ord('q'):
		break

cap.release(0)
cv2.destroyAllWindows()
