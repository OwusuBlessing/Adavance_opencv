# -*- coding: utf-8 -*-
"""
Created on Thu May 26 08:48:43 2022

@author: USER 1
"""



# import libraries
import os
import cv2
import mediapipe as mp
import time # to check frame rate


# hand tracking module ###########################################
class  handdetector():
    def __init__(self,mode =False,maxhands = 2,modelC = 0,detecCon = 0.5,TrackConf = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.modelC = modelC
        self.detecCon = detecCon
        self.TrackConf = TrackConf
        #initialize other variables
        
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands( self.mode,self.maxhands,self.modelC,self.detecCon,self.TrackConf)
        self.mpDraw = mp.solutions.drawing_utils
    def find_hands(self,img,draw = True):
        
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
     # process hands in imgRGB
        self.results = self.hands.process(imgRGB)
     #print(results.multi_hand_landmarks)
     # check if hands are detected
        if self.results.multi_hand_landmarks:
           for handlandmark in self.results.multi_hand_landmarks:
               if draw:
             
                  self.mpDraw.draw_landmarks(img,handlandmark,self.mphands.HAND_CONNECTIONS)
        return img
    def getposition(self,img,HandsNO=0,draw = True):
        
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        self.results = self.hands.process(imgRGB)
        

        #landmark list
        lmlist =[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[HandsNO]
            for Id,lm in enumerate(myhand.landmark):
                  # height,width and channel of image
                  h,w,c = img.shape
                  # find position
                  cx,cy = int(lm.x * w),int(lm.y * h)
                  #print(Id,cx,cy)
                  lmlist.append([Id,cx,cy])
                  if draw:
                      cv2.circle(img,(cx,cy),5,(176,245,157),cv2.FILLED)
        return lmlist      
#############################################################



wCam,hCam =  640,480
# create video obejct
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime =0
cTime = 0
# read finger images
folderpath = "assets/fingerImages"
myList = os.listdir(folderpath)
overlayList = []
for impath in myList:
    image = cv2.imread(f'{folderpath}/{impath}')
    resized = cv2.resize(image,(200,200),interpolation = cv2.INTER_AREA)
    overlayList.append(resized)

print(overlayList)

detector = handdetector(detecCon=0.7)
tipIds = [4,8,12,16,20]
fingers  = []
while True:
     success,img = cap.read()
     #img = cv2.flip(img,1)
     img = detector.find_hands(img)
     lmlist = detector.getposition(img,draw = False)
     #print(lmlist)
     if len(lmlist) !=0 :
        fingers = []
        #thumb
        if lmlist[tipIds[0]][1] >  lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
       # four fingers
        for Id in range(1,5):
                # write conditions for openness and closeness of fingers
                 if lmlist[tipIds[Id]][2] < lmlist[tipIds[Id] - 2][2]:
                     fingers.append(1)
                 else:
                     fingers.append(0)
      
    # print(fingers)  
     total_fingers = fingers.count(1)
     #print(total_fingers)
     h,w,c = overlayList[total_fingers].shape
     img[0:h,0:w] = overlayList[total_fingers]
     cv2.rectangle(img,(480,350),(640,480),(0,255,0),cv2.FILLED)
     
     
     cv2.putText(img,f'{str(int(total_fingers))}',(540,465),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),5)      
     
            
           
     cTime = time.time()
     fps = 1/(cTime - pTime)
     pTime = cTime
     
     cv2.putText(img,f'fps:{str(int(fps))}',(500,40),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)      
     cv2.imshow("image",img)
     if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()