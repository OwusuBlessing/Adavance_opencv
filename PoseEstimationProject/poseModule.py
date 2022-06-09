# -*- coding: utf-8 -*-

import cv2
import mediapipe as mp
import time

class posedetector():
    def __init__(self,mode=False,mc=1,smoothL=True,enableseg=False,smoothseg=True,mindetection=0.5,minTrack=0.5):
        self.mode = mode
        self.mc = mc
        self.smoothL = smoothL
        self.enableseg = enableseg
        self.smoothseg = smoothseg
        self.mindetection = mindetection
        self.minTrack = minTrack
        self.mppose = mp.solutions.pose
        self.pose = self.mppose.Pose()
        self.mpDraw = mp.solutions.drawing_utils
    
    def getpose(self,img,draw = True):
            self.draw = draw
                    
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results = self.pose.process(imgRGB)
            # store landmarks
            if self.results.pose_landmarks:
                if draw:
                 self. mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mppose.POSE_CONNECTIONS)
        
            return img
    def getposition(self,img,draw = True):
           lmlist = []
           if self.results.pose_landmarks:
               for Id,lm in enumerate(self.results.pose_landmarks.landmark):
                   h,w,c = img.shape
                   cx, cy = int(lm.x * w),int(lm.y * h)
                   lmlist.append([Id,cx,cy])
                   if draw:
                       cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
                       
           return lmlist
                      
def main():
    cap = cv2.VideoCapture("C:/Users/user/Desktop/DL_tutorial/Advanced_opencv/PoseEstimationProject/poseVideos/vid1.mp4")
        
    while True:
        success,img = cap.read()
                
        pTime = 0
        cTime = 0
        pose = posedetector()
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
        cv2.circle(img,(lmlist[14][1],lmlist[14][2]),5,(255,0,0),cv2.FILLED)
            
        
        cv2.putText(image,str(int(fps)),(60,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)      
        cv2.imshow("Image",image)
        
        if cv2.waitKey(1) == ord('q'):
                 break
    cap.release()
    cv2.destroyAllWindows()
           
    
            
    
if __name__== "__main__":
    main()