# -*- coding: utf-8 -*-




import cv2
import mediapipe as mp
import time
import poseModule as pm
cap = cv2.VideoCapture("PoseEstimationProject/poseVideos/vid1.mp4")
    
while True:
    success,img = cap.read()
            
    pTime = 0
    cTime = 0
    pose = pm.posedetector()
    img = pose.getpose(img)
    lmlist = pose.getposition(img)
    #print(lmlist[0])
    
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    image = cv2.resize(img,(1200,720),fx=0,fy=0,interpolation = cv2.INTER_CUBIC)
    # suppose we want to track a specific part of the body
    # suppose we want to track elbow and draw since ellbow is index 14
    #cv2.circle 
    #    cv2.circle(img,(lmlist[14][1],lmlist[14][2]),5,(255,0,0),cv2.FILLED)
        
    
    cv2.putText(image,str(int(fps)),(60,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)      
    cv2.imshow("Image",image)
    
    if cv2.waitKey(1) == ord('q'):
             break
cap.release()
cv2.destroyAllWindows()
       
    