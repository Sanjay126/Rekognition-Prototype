from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of images")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model: `hog` and `cnn` are supported")
ap.add_argument("-e", "--encodings", required=True,
	help="path to store facial encodings")
args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args["dataset"]))
imagePaths.sort()

knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
	name = imagePath.split(os.path.sep)[-2]

	
	image = cv2.imread(imagePath)
	if image is None:
		continue
	height, width = image.shape[:2]
	max_height = 768
	max_width = 1366

	# only shrink if img is bigger than required
	if max_height < height or max_width < width:
	    # get scaling factor
		scaling_factor = max_height / float(height)
		if max_width/float(width) < scaling_factor:
			scaling_factor = max_width / float(width)
		# resize image
		image = cv2.resize(image,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)	
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	try:
		#get bounding boxes for faces in image
		boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
		#get encodings of faces
		encodings = face_recognition.face_encodings(rgb, boxes,num_jitters=2)
	except:
		continue

	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings 
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
