# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

class Face_Recognition:

	def __init__(self):
		# construct the argument parser and parse the arguments
		self.ap = argparse.ArgumentParser()
		# Run the and Loop the face_recognition application
		# self.main() #!!!

	def build_argument(self):
		# self.ap.add_argument("-o", "--Output", type=str, help="path to output video")

		self.ap.add_argument("-y", "--Display", type=int, default=1, help="whether or not to display output frame to screen")

		self.ap.add_argument("-e", "--Encodings", required=True, help="path to serialized db of facial encodings")

		self.ap.add_argument("-c", "--Cascade", required=True, help="path to where the face cascade resides")

		self.ap.add_argument("-m", "--Model", type=str, default="cnn", help="face detection model to use: either `hog` or `cnn`")

		# Define and initialize the host_name of our program.
		self.host_name = ["Chuwei Chen", "Taozhan Zhang", "Zhaozhong Qi"]

		self.RECOGNIZED = 5 # Initial points = 5

		self.fps = FPS()

		args = vars(self.ap.parse_args())

		return args


	def load_encoding(self):
		# load the known faces and embeddings
		args = self.build_argument()
		print("[INFO] loading encodings + face detector...")
		data = pickle.loads(open(args["Encodings"], "rb").read())
		# Instantiate our face detector using the OpenCV: Haar cascade method
		# The method which is efficient to detect objects in images at multiple scales in realtime
		# detector = cv2.CascadeClassifier(args["Cascade"])
		detector = cv2.CascadeClassifier(cv2.data.haarcascades + args["Cascade"])

		return args, data, detector

	def main(self) -> bool:
		args, data, detector = self.load_encoding()
		"Initialize Raspberry Pi camera: "
		# Initialize the video stream and pointer to output video file, then
		# allow the camera sensor to warm up
		print("[INFO] starting video stream...")
		# Using Pi-Camera at here:
		vs = cv2.VideoCapture(0)
		# Wait for the camera to warm up
		time.sleep(2.0)

		# Start our frames per second, FPS counter
		fps = self.fps.start()

		# Loop over frames from the video file stream, keep recognize the face until a certain signal comes up.
		# Right now, it continues until we press the "q" in terminal, will change in the future.
		while True:
			# Grab a specific frame from the threaded video stream
			# Grab the frame from the threaded video stream and resize it to 500px (to speedup processing)

			# cv2.imshow('Imagetest',frame)
			success, frame = vs.read()
			if success == False:	
				print("Read Error, check camera or devices, No frame can be read..")
				return 

			# frame = imutils.resize(frame, width=500)

			# convert the input frame from
			# (1) BGR to grayscale (for face detection)
			# (2) from BGR to RGB (for face recognition)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			# detect faces in the grayscale frame

			# OpenCV returns bounding box coordinates in (x, y, w, h) order
			# However, we need them in (top, right, bottom, left) order, so we do a reordering at here:
			rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
			# for (x, y, w, h) in rects:
			# 	box = cv2.rectangle(rects, (x, y), (x + w, y + h), (255, 255, 255), 3)


			box = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

			# compute the facial embeddings for each face bounding box extract from our camera frame
			encodings = face_recognition.face_encodings(rgb, box)

			# Initialize name variable for each time of the frame refreshed
			names = []

			# loop over the facial embeddings
			for encode_frame in encodings:
				# attempt to match each face in the input image to our known encodings
				matches = face_recognition.compare_faces(data["encodings"], encode_frame, tolerance=0.4)
				# print(matches)
				# If the model cannot recognize the face in bounding box, it will show as: Unknown Face
				name = "Unknown"
				# print(len(matches))
				if True in matches:
					# check to see if we have found a match
					
					# Find the indexes of all matched faces,
					# then initialize a dictionary to count the total number of times each face was matched
					matched_Index = [i for (i, b) in enumerate(matches) if b]

					# print(matches)
					# print(matched_Index)

					counts = {}
					# loop over the matched indexes and maintain a count for each recognized face.
					for i in matched_Index:
						name = data["names"][i]
						counts[name] = counts.get(name, 0) + 1
						# print(counts)

					# Determine the recognized face with the largest number of votes by using K-Nearest-Neighbors.
					# 	Note: in the event of an unlikely tie Python will select first entry in the dictionary
						
					name = max(counts, key=counts.get)

				names.append(name)
			
			# Each recgonized of frame, Check if there exist host:
			if len(names) != 0:
				# If there any existing faces appears in the frame
				for reg in names:
					if reg in self.host_name:
						# In real time video, if recognize identity of the host, give 2 points of reward
						self.RECOGNIZED = self.RECOGNIZED + 5
					else:
						# In real time video, if not recognize identity of the host, give 1 point of penalty
						self.RECOGNIZED = self.RECOGNIZED - 1
						# Greater than 0 points
						
					#if self.RECOGNIZED < 0:	self.RECOGNIZED = 0
					if self.RECOGNIZED < 0:	return False

					# Once score greater than a threshold, doors open signal will release..
					if self.RECOGNIZED >= 30:	
						self.finish_recognize(signal=True)
						return True

			# Extract the face rectangle from each frame of video (.per ts)
			for ((top, right, bottom, left), name) in zip(box, names):
				# draw the predicted face name on the image
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
				if top - 15 > 15:
					y = top - 15
				else:
					y = top + 15
				cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)


			# Check to see if we are supposed to display the output frame to the screen, Set display attribute to one to see if it is
			if args["Display"] > 0:
				cv2.imshow("Frame", frame)
				key = cv2.waitKey(1) & 0xFF
				# if the `q` key was pressed, break from the loop
				if key == ord("q"):
					self.finish_recognize()
					return

		return False


	def finish_recognize(self, signal=False):
		# stop the timer and display FPS information
		self.fps.stop()
		print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
		# do a bit of cleanup
		cv2.VideoCapture(0).release()
		cv2.destroyAllWindows()
		if signal == True:
			print("Doors open please..")

