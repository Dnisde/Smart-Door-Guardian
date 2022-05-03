### Encode and Train Labeled Faces into the Network:


1. "Train and enbedded the network by using CNN: **Careful: Takes more longer to train...**"

`python encoding_face.py --Dataset Image_Dataset --Encodings ./Model_Encoded/cnn.pickle --Model cnn`

2. "Train and enbebdded the network by using HOG: HOG + Linear SVM"

`python encoding_face.py --Dataset Image_Dataset --Encodings ./Model_Encoded/hog.pickle --Model hog`

\

### Recognize faces by using K-Nearest Neighbors:


1. "Load CNN embedded model to recognize real-time faces: " 

`python Face_Recognition.py --Encodings ./Model_Encoded/cnn.pickle --Cascade haarcascade_frontalface_default.xml --Display 1`

2. "Load HOG + Linear embedded model to recognize real-time faces: "

`python Face_Recognition.py --Encodings ./Model_Encoded/hog.pickle --Cascade haarcascade_frontalface_default.xml --Display 1`
