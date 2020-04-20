#import needed libaries
#cv2 allows us to interact with the camera and find objects in the fram
import cv2
import sys
import time
import RPi.GPIO as gpio

#servo and pin setup
gpio.setmode(gpio.BCM)
gpio.setup(11,gpio.OUT)
servo = gpio.PWM(11,50)
servo.start(7.5)
servo.ChangeDutyCycle(0)

#set up the varibles
currentPos = 7.5
faceCenter = 0
maxRight = False
maxLeft = True
#THESE WILL BE DETERMINED BY THE MOUNT WE BUILD############# becarful edditing these and running without testing
minPos = 3 # This is the most left position within non-breakage range for the servo
maxPos = 11.5 # This is the most right position within non-breakage range for the servo
########################################
rangeRight = 230 #this is the X range for the face detection
rangeLeft = 140  

#if this is too fast it wont find the face, bigger the number the faster it moves
incrementServo = .15 

#set up face detection using cv2
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

#get the video feed in
videoCapture = cv2.VideoCapture(0)
videoCapture.set(3, 320)
videoCapture.set(4, 240)


#when no face is in frame this function scans from left t right untill it finds one
def scan():
	global currentPos
	global maxRight
	global maxLeft
	
	if not maxRight: 
		servoRight()
		if currentPos >= maxPos:
			maxRight = True
			maxLeft = False
	if not maxLeft:
		servoLeft()
		if currentPos <= minPos:
			maxRight = False
			maxLeft = True 

#moves the servo left once
def servoLeft():
	global currentPos
	#looks to see if in minPos
	if currentPos > minPos:
		currentPos = currentPos - incrementServo
		servo.ChangeDutyCycle(currentPos)
	time.sleep(.02) #sleep to keep from jerking too fast
	servo.ChangeDutyCycle(0) #stops sending the signal to stop jitter

#moves the servo right once
def servoRight():
	global currentPos
	#checks to see if its in the maxPos
	if currentPos < maxPos:
		currentPos = currentPos + incrementServo
		servo.ChangeDutyCycle(currentPos)
	time.sleep(.02) #sleep to keep from jerking too fastr
	servo.ChangeDutyCycle(0) #stops sending the signal to stop jitter

#if face is in the range don't do anything. If its outside of the range adjust the servo so face is in range
#keep in mind the cameras left is our right
def track_face(facePos):

	# turn the SERVO to the left (our right)
	if facePos > rangeRight:
		servoLeft()
	
	# turn the SERVO to the right (our left)
	if facePos < rangeLeft:
		servoRight()
	time.sleep(.01)
	servo.ChangeDutyCycle(0)

#infintie loop to run the program
while(True):
	#capture frame by frame
	ret, frame = videoCapture.read()
	
	#find the position of the face
	face = faceCascade.detectMultiScale(
		frame,
		scaleFactor = 1.3,
		minNeighbors = 1,
		minSize = (40,40),
		flags = (cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH + cv2.CASCADE_SCALE_IMAGE))

	#draw a box around and find the center of the face 
	for (x, y, w, h) in face:
		cv2.rectangle(frame, (x, y), (x+w,y+h), (0,0,255))
		faceCenter = (w/2+x)
		
	#display video frame
	cv2.imshow('Video', frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	#if we found a face send the position to the servo
	if faceCenter != 0:
		track_face(faceCenter)

    #constatly look for a face until we find one
	else:
		scan()
	#set the value to zero for the next pass
	faceCenter = 0 	
		

# clean up pins and stop the video feed
gpio.cleanup()
videoCapture.release()
#close the video view winfow
cv2.destroyAllWindows()

	
