# -*- coding: utf-8 -*-
"""
Created on Tue May 31 20:35:02 2022

@author: user
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
    def 
#############################################################





