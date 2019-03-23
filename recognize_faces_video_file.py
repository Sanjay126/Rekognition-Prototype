import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import numpy as np
from pytube import YouTube

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-u","--url",type=str,help="Link to youTube video to detect")
ap.add_argument("-o", "--output", type=str,default="output1.mp4",
	help="path to output video")
args = vars(ap.parse_args())

data = pickle.loads(open(args["encodings"], "rb").read())
#Download youtube video
videoName=YouTube(args["url"]).streams.filter(progressive=True,file_extension='mp4').order_by('resolution').desc().first().download('./')

stream = cv2.VideoCapture(videoName)
all_names={}
namelist=[]
writer=None
total_frames=0
scaling_factor=1
frame_no=0
while True:

	(flag, frame) =stream.read()
	if not flag:
		break
	if frame_no==0:
		height, width = frame.shape[:2]
		max_height = 768
		max_width = 1366
		#only calculate scaling factor once
		if scaling_factor==1:
		# only shrink if img is bigger than required
			if max_height < height or max_width < width:
			    # get scaling factor
				scaling_factor = max_height / float(height)
				if max_width/float(width) < scaling_factor:
					scaling_factor = max_width / float(width)

		# resize image
		if scaling_factor<1:	
			frame = cv2.resize(frame,None,fx=scaling_factor,fy=scaling_factor,interpolation=cv2.INTER_AREA)	

		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		r = frame.shape[1] / float(rgb.shape[1])
		total_frames+=1
		boxes = face_recognition.face_locations(rgb,number_of_times_to_upsample=1,model=args["detection_method"])
		encodings = face_recognition.face_encodings(rgb, boxes,num_jitters=1)

		for encoding in encodings:
			matches = face_recognition.compare_faces(data["encodings"],encoding,tolerance=0.5)
			name = "Unknown"
			if True in matches:
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1
				#final name is name with maximum matches in dataset
				name = max(counts, key=counts.get)
			namelist.append(name)
		#include name only if same name occurs in 3 frames consecutively.
		if len(namelist)>=3:
			name=namelist.pop(0)
			if name==namelist[0] and namelist[0]==namelist[1]:
				if name is not "Unknown":
					if all_names.get(name) is None:
						all_names[name]=1
					else:
						all_names[name]+=1

stream.release()
final_names=[]
#exclude names with less than 1% occurence in video
for key,value in all_names.items():
	if value>(total_frames/100):
		try:
			final_names.append(key)
		except :
			pass
print("Prediction:- ",final_names)
print("All detected faces:- ",all_names)
print("Total frames=",total_frames)
if writer is not None:
	writer.release()