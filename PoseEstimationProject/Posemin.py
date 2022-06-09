# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import time

# read video
cap = cv2.VideoCapture("PoseEstimationProject/poseVideos/vid7.mp4")
pTime = 0
cTime = 0
# instantiate model
mppose = mp.solutions.pose
pose = mppose.Pose()
mpDraw = mp.solutions.drawing_utils
while True:
    success,img = cap.read()
    
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # store landmarks
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mppose.POSE_CONNECTIONS)
        for Id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            #print(Id,lm)
            cx, cy = int(lm.x * w),int(lm.y * h)
            cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
            
    
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    image = cv2.resize(img,(1200,720),fx=0,fy=0,interpolation = cv2.INTER_CUBIC)
    
    cv2.putText(image,str(int(fps)),(60,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)      
    cv2.imshow("Image",image)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
   