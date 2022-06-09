# -*- coding: utf-8 -*-

import cv2
import time
import mediapipe as mp
cap = cv2.VideoCapture(0)

wCam,hCam =640,480

cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0
#import mediapipe face detection
mpfacedtection = mp.solutions.face_detection
mpdraw = mp.solutions.drawing_utils
facedetect = mpfacedtection.FaceDetection(0.4)

while True:
    rent,img = cap.read()  
    img = cv2.resize(img,(1200,720),fx=0,fy=0,interpolation =cv2.INTER_CUBIC)
    
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    results = facedetect.process(imgRGB)
    if results.detections:
        for Id,detection in enumerate(results.detections):
            #mpdraw.draw_detection(img, detection)
            #print(Id,detection)ete
            ih,iw,ic = img.shape
            bboxC = detection.location_data.relative_bounding_box
            bbox = int(bboxC.xmin * iw ),int(bboxC.ymin * ih ),\
                   int(bboxC.width * iw ),int(bboxC.height * ih) 
            cv2.rectangle(img,bbox,(255,0,255),2)
            
            cv2.putText(img,f'{int(detection.score[0] *100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_COMPLEX,2,(0,213,123),2)      
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f' fps {str(int(fps))}',(20,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,213,123),2)      
    cv2.imshow("Image",img)
    if cv2.waitKey(1) == ord('q'):
             break
cap.release()
cv2.destroyAllWindows()




       