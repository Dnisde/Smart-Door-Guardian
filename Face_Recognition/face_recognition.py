# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
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
		self.main()

	def build_argument(self):
		self.ap.add_argument("-o", "--Output", type=str, help="path to output video")

		self.ap.add_argument("-y", "--Display", type=int, default=1, help="whether or not to display output frame to screen")

		# self.ap.add_argument("-i", "--Image", required=True, help="path to input image")

		self.ap.add_argument("-e", "--Encodings", required=True, help="path to serialized db of facial encodings")

		self.ap.add_argument("-c", "--Cascade", required=True, help="path to where the face cascade resides")

		self.ap.add_argument("-m", "--Model", type=str, default="cnn", help="face detection model to use: either `hog` or `cnn`")

		# Define and initialize the host_name of our program.
		self.host_name = ["Chuwei Chen", "Taozhan Zhang", "Zhaozhong Qi"]

		self.RECOGNIZED = False

		args = vars(self.ap.parse_args())

		return args


	def load_encoding(self):
		# load the known faces and embeddings
		args = self.build_arugment()
		print("[INFO] loading encodings + face detector...")
		data = pickle.loads(open(args["Encodings"], "rb").read())
		# Instantiate our face detector using the OpenCV: Haar cascade method
		# The method which is efficient to detect objects in images at multiple scales in realtime
		detector = cv2.CascadeClassifier(args["Cascade"])
		return args, data, detector

	def main(self):
		args, data, detector = self.load_encoding()
		"Initialize Raspberry Pi camera: "
		# Initialize the video stream and pointer to output video file, then
		# allow the camera sensor to warm up
		print("[INFO] starting video stream...")
		# Using Pi-Camera at here:
		vs = VideoStream(usePiCamera=True).start()
		# Wait for the camera to warm up
		time.sleep(2.0)

		# Start our frames per second, FPS counter
		fps = FPS().start()

		# Loop over frames from the video file stream, keep recognize the face until a certain signal comes up.
		# Right now, it continues until we press the "q" in terminal, will change in the future.
		while True:
			# Grab a specific frame from the threaded video stream
			# Grab the frame from the threaded video stream and resize it to 500px (to speedup processing)
			frame = vs.read()
			frame = imutils.resize(frame, width=500)

			# convert the input frame from
			# (1) BGR to grayscale (for face detection)
			# (2) from BGR to RGB (for face recognition)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			# detect faces in the grayscale frame
			rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

			# OpenCV returns bounding box coordinates in (x, y, w, h) order
			# However, we need them in (top, right, bottom, left) order, so we do a reordering at here:
			boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

			# compute the facial embeddings for each face bounding box
			encodings = face_recognition.face_encodings(rgb, boxes)

			# Initialize name variable for each time of the Face_Recognition Application Start:
			names = []

			# loop over the facial embeddings
			for encoding in encodings:
				# attempt to match each face in the input image to our known encodings
				matches = face_recognition.compare_faces(data["Encodings"], encoding)
				# If the model cannot recognize the face in bounding box, it will show as: Unknown Face
				name = "Unknown"

				# check to see if we have found a match
				if True in matches:
					# Find the indexes of all matched faces,
					# then initialize a dictionary to count the total number of times each face was matched
					matched_Index = [i for (i, b) in enumerate(matches) if b]
					counts = {}
					# loop over the matched indexes and maintain a count for each recognized face.
					for i in matched_Index:
						name = data["names"][i]
						counts[name] = counts.get(name, 0) + 1

					# Determine the recognized face with the largest number of votes by using K-Nearest-Neighbors.
					# 	Note: in the event of an unlikely tie Python will select first entry in the dictionary
					name = max(counts, key=counts.get)

				# If Found the familiar faces in our encoding frame
				# update the list of names
				names.append(name)

				if name != "Unknown":
					# Print the name of the recognized face in terminal
					print(f"You are {name}")
					self.RECOGNIZED = True


			# loop over the recognized faces
			for ((top, right, bottom, left), name) in zip(boxes, names):
				# draw the predicted face name on the image
				cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
				if top - 15 > 15:
					y = top - 15
				else:
					y = top + 15
				cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

			# check to see if we are supposed to display the output frame to
			# the screen, Set display attribute to one to see if it is
			if args["Display"] > 0:
				cv2.imshow("Frame", frame)
				key = cv2.waitKey(1) & 0xFF

			if self.RECOGNIZED == True:
				break

			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

		# stop the timer and display FPS information
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()

# def recognition_face_image(self):
	# 	# initialize the list of names for each face detected
	#
	# 	# load the input image and convert it from BGR (OpenCV ordering) to dlib ordering (RGB)
	# 	image = cv2.imread(args["Image"])
	# 	# OpenCV orders color channels in BGR,
	# 	# But the face_recognition module uses dlib, so before we proceed,
	# 	# let’s swap color spaces on Line 37, naming the new image rgb.
	# 	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	#
	# 	# Detect the (x, y)-coordinates of the bounding boxes corresponding
	# 	# to each face in the input image, then compute the facial embeddings for each face
	# 	print("[INFO] recognizing faces...")
	# 	boxes = face_recognition.face_locations(rgb, model=args["Model"])
	#
	# 	encodings = face_recognition.face_encodings(rgb, boxes)
	#
	# 	encodings = self.load_encoding()
	#
	# 	names = []
	#
	# 	# loop over the facial embeddings
	# 	for encoding in encodings:
	# 		# attempt to match each face in the input image to our known encodings
	# 		matches = face_recognition.compare_faces(data["encodings"],encoding)
	# 		name = "Unknown"
	# 		# check to see if we have found a match
	# 		if True in matches:
	# 			# find the indexes of all matched faces then initialize a
	# 			# dictionary to count the total number of times each face
	# 			# was matched
	# 			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
	# 			counts = {}
	# 			# loop over the matched indexes and maintain a count for
	# 			# each recognized face face
	# 			for i in matchedIdxs:
	# 				name = data["names"][i]
	# 				counts[name] = counts.get(name, 0) + 1
	# 			# determine the recognized face with the largest number of
	# 			# votes (note: in the event of an unlikely tie Python will
	# 			# select first entry in the dictionary)
	# 			name = max(counts, key=counts.get)
	#
	# 		# update the list of names
	# 		names.append(name)


Face_Recognition()

