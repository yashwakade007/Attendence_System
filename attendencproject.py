import cv2 
import numpy as np 
import face_recognition
import os 
from datetime import datetime
path='opencv1\imagesattendence'
images=[]
className=[]
myList=os.listdir(path)
print(myList)

for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])
print(className)

def findencodings(images):
    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
encodelistknown=findencodings(images)
print("Encoding Complete")

def markattendence(name):
    with open('opencv1\\attendence.csv','r+')as f:
        mydatalist=f.readlines()
        namelist=[]
        for line in mydatalist:
            entry=line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


cap=cv2.VideoCapture(0)
while True:
    success,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25,)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurframe=face_recognition.face_encodings(imgS,faceCurFrame)

    for encodeFace,faceloc in zip(encodeCurframe,faceCurFrame):
        matches=face_recognition.compare_faces(encodelistknown,encodeFace)
        facedist=face_recognition.face_distance(encodelistknown,encodeFace)
        print(facedist)
        matchindex=np.argmin(facedist)
        if matches[matchindex]:
            name=className[matchindex].upper()
            # print(name)
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markattendence(name)
    cv2.imshow('Webcam',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

# faceloc=face_recognition.face_locations(imgelon)[0]
# encodeElon=face_recognition.face_encodings(imgelon)[0]
# cv2.rectangle(imgelon,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,250),2)


# faceloctest=face_recognition.face_locations(imgtest)[0]
# encodetest=face_recognition.face_encodings(imgtest)[0]
# cv2.rectangle(imgtest,(faceloctest[3],faceloctest[0]),(faceloctest[1],faceloctest[2]),(255,0,250),2)
# print(faceloctest)

# results=face_recognition.compare_faces([encodeElon],encodetest)
# facedis=face_recognition.face_distance([encodeElon],encodetest)
# print(results,facedis)
# cv2.putText(imgtest,f'{results}{round(facedis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2,)
# cv2.imshow('Elon Musk',imgelon)
# cv2.imshow('Elon Musk',imgtest)
