# # -*- coding: utf-8 -*-

import sys               
import cv2
import mediapipe as mp
import time
sys.path.append("HandTrackingProjcet/handTrackingModule.py")
import handTrackingModule as htm

detector=htm.handdetector()
# create video obejct
cap = cv2.VideoCapture(0)

  
pTime =0
cTime = 0

while True:
    success,img = cap.read()
    image = detector.find_hands(img)
    lmlist = detector.getposition(img)
    if len(lmlist) != 0:
        print(lmlist[4])
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)      
 
    cv2.imshow("image",img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
   