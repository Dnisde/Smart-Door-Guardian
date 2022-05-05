from imutils.video import VideoStream
from imutils.video import FPS
from time import sleep
from picamera import PiCamera

import face_recognition
import imutils
import pickle
import time
import cv2


def test():
	# Test Camera: 
	print("Start test taking photo, warm up...")
	camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.start_preview()

	#camera warm-up time
	sleep(2)
	camera.capture( 'image.jpg’')
	print("Test finishing, camera works good..")

	# Test Video streaming by using camera
	print("[INFO] starting video stream...")
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# if the `q` key was pressed, break from the loop
	fps = FPS().start()

	time.sleep(2.0)

	# update the FPS counter

	# stop the timer and display FPS information
	fps.stop()

	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	print("Video stream and all packages works good! Finish the test")


test()
