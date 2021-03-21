from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
from tkinter import *
import cv2
from datetime import datetime
from PIL import Image, ImageTk
import Code.my_sql as mysql
from datetime import datetime

class faceDetection():
    
    tu=True
    
    def start(self, faceNet, cover_model, master):
        self.con=0
        self.label=None
        self.access=None
        self.cover=None
        self.color=None
        self.no=True
        today=datetime.now()
        self.entry_time = str(today.hour)+":"+str(today.minute)+":"+str(today.second)
        root = Toplevel(master)

        # Setting Window size 
        root.geometry("1920x1080")

        # creating label
        Label(root, text="Checking Face", font=("Comic Sans MS", 40, "bold"), fg="red").pack()
        
        # Creating frame for showing vidoe frame
        f1 = LabelFrame(root, bg="red")
        f1.pack()
        L1 = Label(f1, bg="red")
        L1.pack()
        global coverlbl
        global accesslbl

        # creating label to show access granted or denied
        coverlbl=Label(root, text="hello",font=("Comic Sans MS", 20, "bold"), fg="red")
        #creating label to show warning
        accesslbl=Label(root, text="hello", font=("Comic Sans MS", 20, "bold"), fg="red")
        coverlbl.pack()
        accesslbl.pack()

        # creating back button
        Button(root, text="Back", command=lambda:root.destroy()).pack()

        # accessing camera 
        vs = VideoStream(src=1).start()  

        while True:
            # reading camera video
            frame = vs.read()
            (locs, preds) = self.detect_and_predict_mask(frame, faceNet, cover_model)
			
            for (box, pred) in zip(locs, preds):
                
                (startX, startY, endX, endY) = box
                (covered, not_covered) = pred
                self.label = "Covered" if covered > not_covered else "Not Covered"
                self.color = (0, 0, 255) if self.label == "Covered" else (0, 255, 0)
                self.con = int(max(covered, not_covered) * 100)
                label1 = ''
                label1 = "{:.2f}%".format(max(covered, not_covered) * 100)

                # Putting text in video frame ie confidence level
                cv2.putText(frame, label1, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.color, 2)
                # Putting rectangle around face 
                cv2.rectangle(frame, (startX, startY), (endX, endY), self.color, 2)
            
            # converting image from BGR to RGB
            img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # converting image to array and giving it to imagetk 
            img = ImageTk.PhotoImage(Image.fromarray(img2))
            # placing video in frame
            L1["image"] = img
            if self.con>=80 and self.label == "Not Covered":
                self.access = "ATM Access Granted"
                self.cover = ""
                # if self.tu == True:
                #     self.save_img(img2)

            else:
                self.access = "ATM Access Denied"
                self.cover = "Please uncover your face for a while"	
            self.change_text()
            root.update()
            if self.tu==False:
                cv2.destroyAllWindows()
                vs.stop()
                root.destroy()
                return self.no
                

    def detect_and_predict_mask(self, frame, faceNet, cover_model):
    	# grab the dimensions of the frame and then construct a blob
    	# from it
    	(h, w) = frame.shape[:2]
    	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
    		(104.0, 177.0, 123.0))
    
    	# pass the blob through the network and obtain the face detections
    	faceNet.setInput(blob)
    	detections = faceNet.forward()
    
    	# initialize our list of faces, their corresponding locations,
    	# and the list of predictions from our face mask network
    	faces = []
    	locs = []
    	preds = []
    
    	# loop over the detections
    	for i in range(0, detections.shape[2]):
    		# extract the confidence (i.e., probability) associated with
    		# the detection
    		confidence = detections[0, 0, i, 2]
    
    		# filter out weak detections by ensuring the confidence is
    		# greater than the minimum confidence
    		if confidence > 0.5:
    			# compute the (x, y)-coordinates of the bounding box for
    			# the object
    			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    			(startX, startY, endX, endY) = box.astype("int")
    
    			# ensure the bounding boxes fall within the dimensions of
    			# the frame
    			(startX, startY) = (max(0, startX), max(0, startY))
    			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
    
    			# extract the face ROI, convert it from BGR to RGB channel
    			# ordering, resize it to 224x224, and preprocess it
    			face = frame[startY:endY, startX:endX]
    			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    			face = cv2.resize(face, (224, 224))
    			face = img_to_array(face)
    			face = preprocess_input(face)
    
    			# add the face and bounding boxes to their respective
    			# lists
    			faces.append(face)
    			locs.append((startX, startY, endX, endY))
    
    	# only make a predictions if at least one face was detected
    	if len(faces) > 0:
    		# for faster inference we'll make batch predictions on *all*
    		# faces at the same time rather than one-by-one predictions
    		# in the above `for` loop
    		faces = np.array(faces, dtype="float32")
    		preds = cover_model.predict(faces, batch_size=32)
    
    	# return a 2-tuple of the face locations and their corresponding
    	# locations
    	return (locs, preds)
    
    def save_img(self, frame):
        # converting image to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        filename = "Images/"+str(datetime.now().today()).replace(":"," ")+".jpg"	
        # Saving image to directory
        # cv2.imwrite(filename, frame)
        # self.tu=False
        # # calling mysql function
        # mysql.my_sql(filename=filename, entry_time=self.entry_time)

    def change_text(self):
        if self.color == (0, 0, 255):
            colour="red"
        else:
            colour="green"
        accesslbl.config(text=self.cover, fg=colour)
        coverlbl.config(text=self.access, fg=colour)   
    


            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    