from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# Define arguments of input directory requireds
ap.add_argument("-d", "--Dataset", required=True, 
				help="path to input directory of faces + images")

ap.add_argument("-e", "--Encodings", required=True, 
				help="path to serialized db of facial encodings")

ap.add_argument("-m", "--Model", type=str, default="cnn",
				help="face detection model to use: either `hog` or `cnn`")

args = vars(ap.parse_args())


# grab the paths to the input images from our dateset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["Dataset"]))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))

	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from BGR (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	# OpenCV orders color channels in BGR, 
	# But the face_recognition module uses dlib, so before we proceed, 
	# let’s swap color spaces on Line 37, naming the new image rgb.
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image

	# Parsing two parameters:
	# rgb: Our RGB face image(Converted)
	# model: Model of the face detection of pre-trained that we defined in argument
	bounding_boxes = face_recognition.face_locations(rgb, model=args["Model"])

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, bounding_boxes)

	# loop over the encodings
	for encoding in encodings:
		# each encoding + name to our set of known names and encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

	# Continue encode and load series of images we have in the dataset


print("[INFO] serializing encodings...")
# Construct a dictionary with two keys, as we known, encoded faces information by facer_ecognition() 
data = {"encodings": knownEncodings, "names": knownNames}
# Dump the names and encodings to disk for future recall.
f = open(args["Encodings"], "wb")
f.write(pickle.dumps(data))
f.close()

