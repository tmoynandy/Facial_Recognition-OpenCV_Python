import cv2
import numpy as np
import sqlite3

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); 
cam=cv2.VideoCapture(0);
rec=cv2.face.createLBPHFaceRecognizer();
rec.load("recognizer/trainingdata.yml")
id=0

def getProfile(id):
	conn=sqlite3.connect("facebase.db")
	cmd="SELECT * FROM people WHERE ID="+str(id)
	cursor=conn.execute(cmd)
	profile=None
	for row in cursor:
		profile=row
	conn.close()
	return profile

font=cv2.FONT_HERSHEY_SIMPLEX
while(True):
	ret,img=cam.read() 
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
	faces=facedetect.detectMultiScale(gray,1.3,5); 
	for(x,y,w,h) in faces: 
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		conf=rec.predict(gray[y:y+h,x:x+w])
		id=conf
		profile=getProfile(id)
		if(profile!=None):
			cv2.putText(img,str(profile[0]),(x,y+h), font, 1,(255,255,255),2);
		        cv2.putText(img,str(profile[1]),(x,y+h+30), font, 1,(255,255,255),2);


	cv2.imshow("Face",img); 
	if(cv2.waitKey(10)==ord('q')): 
		break;
cam.release()
cv2.destroyAllWindows()
