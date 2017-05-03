import cv2
import numpy as np
import sqlite3

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
 
cam=cv2.VideoCapture(0);

def InsertOrUpdate(id,name):
	conn=sqlite3.connect("facebase.db")
	print "success 1"
	cmd="SELECT * FROM people WHERE ID="+str(id)
	cursor=conn.execute(cmd)
	isRecordExist=0
	for row in cursor:
		isRecordExist=1
	if(isRecordExist==1):
		cmd="UPDATE people SET NAME="+str(name)+" WHERE  ID="+str(id)
	else:
		cmd="INSERT INTO people(ID,NAME) Values("+str(id)+","+str(name)+")" 
	conn.execute(cmd)
	conn.commit()
	print "success 2"
	conn.close()

id=raw_input("enter user id:")
name=raw_input("enter user name:")
InsertOrUpdate(id,name)

sample=0;
while(True):
	ret,img=cam.read(); 
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
	faces=facedetect.detectMultiScale(gray,1.3,5); 
	for(x,y,w,h) in faces:
		sample=sample+1;
		cv2.imwrite("dataset/user."+str(id)+"."+str(sample)+".jpg",gray[y:y+h,x:x+w]) 
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 
	cv2.imshow("Face",img); 
	cv2.waitKey(1);
	if(sample>20):
		break;
cam.release()
cv2.destroyAllWindows()
