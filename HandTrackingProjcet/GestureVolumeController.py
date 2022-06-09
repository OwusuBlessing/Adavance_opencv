# -*- coding: utf-8 -*-
"""
Created on Wed May 25 06:43:47 2022

@author: USER 1
"""



# import libraries


import cv2
import mediapipe as mp
import time # to check frame rat
import numpy as np
import math
import pycaw
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

# hand tracking module ######################################
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
#reset width and height of camera
wCam,hCam =640,480
# create video obejct
cap = cv2.VideoCapture("assets/vid2.mp4")
cap.set(3,wCam)
cap.set(4,hCam)
pTime =0
cTime = 0
detector = handdetector(detecCon=0.5)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange() #-95.25, 0.0, 0.75
#volume.GteMasterVolumeLevel(-20,0,None)
min_vol = volRange[0]
max_vol = volRange[1]
print(min_vol)
vol = 0
lenght = 0
volBar = 400
while True:
     success,img = cap.read()
     # find landmarks
     
     img = detector.find_hands(img)
     
     lmlist = detector.getposition(img,draw=False)
     if len(lmlist) != 0 :
         # thum and index finger landmark
         #print(lmlist[4],lmlist[8])
            x1,y1 = lmlist[4][1],lmlist[4][2] # thumb
            x2,y2 = lmlist[8][1],lmlist[8][2] # index finger
            # centre poimts
            cX,cY = (x1+x2)/2,(y1+y2)/2
            cv2.circle(img,(x1,y1),7,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),7,(0,255,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)
           # cv2.circle(img,(cX,cY),7,(0,255,0),cv2.FILLED)
            lenght = math.hypot(x2-x1,y2-y1)
            print(lenght)
            # hang range (20,175)
            # convert to volume range(-95,0) using interpolation
            vol = np.interp(lenght,[25,230],[min_vol,max_vol])
            volBar = np.interp(vol,[25,230],[400,150])
            
            # set master volume
            volume.SetMasterVolumeLevel(vol,None) 
            # draw volume bar
            volpercent = np.interp(lenght,[25,230],[0,100])
            
            cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
            cv2.putText(img,f'{str(int(volpercent))}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)      
            
            
           
     cTime = time.time()
     fps = 1/(cTime - pTime)
     pTime = cTime
     
     cv2.putText(img,f'fps:{str(int(fps))}',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)      
     cv2.imshow("image",img)
     if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()