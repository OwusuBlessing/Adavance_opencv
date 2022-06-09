# -*- coding: utf-8 -*-

# The hand tracking mediapipe uses handlandmarks and palm detection

# import libraries
import cv2
import mediapipe as mp
import time # to check frame rate

# create video obejct
cap = cv2.VideoCapture(0)
# create hand detector object
mphands = mp.solutions.hands
hands = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils
# write frame rate
pTime =0
cTime = 0
while True:
     success,img = cap.read()
     # the rgb image will be sent to the hands object
     # convert image to rgb
     imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
     # process hands in imgRGB
     results = hands.process(imgRGB)
     #print(results.multi_hand_landmarks)
     # check if hands are detected
     if results.multi_hand_landmarks:
         for handlandmark in results.multi_hand_landmarks:
             # get id number and landmark for each hand
             for Id,lm in enumerate(handlandmark.landmark):
                 # height,width and channel of image
                 h,w,c = img.shape
                 # find position
                 cx,cy = int(lm.x*w),int(lm.y*h)
                 # print(Id,cx,cy)
                 # cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
                 
                 
                 #print(Id,lm)
                 
             mpDraw.draw_landmarks(img,handlandmark,mphands.HAND_CONNECTIONS)
             # draw using media pipe code
             
     cTime = time.time()
     fps = 1/(cTime - pTime)
     pTime = cTime 
     cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)      
             
             
     # use for loop to check if there are multiple hands
     
     cv2.imshow("image",img)
     cv2.waitKey(1)
   
