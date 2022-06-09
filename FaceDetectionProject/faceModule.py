# -*- coding: utf-8 -*-
"""
Created on Wed May 25 04:50:29 2022

@author: USER 1
"""









# -*- coding: utf-8 -*-

import cv2
import time
import mediapipe as mp
#import mediapipe face detection
class faceDetector():
    def __init__(self,min_detect =0.8,model_select=0):
        self.min_detect = min_detect
        self.model_select = model_select
        self.mpfacedtection = mp.solutions.face_detection
        self.mpdraw = mp.solutions.drawing_utils
        self.facedetect = self.mpfacedtection.FaceDetection()
    def findface(self,img,draw = True):
         imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
         self.results = self.facedetect.process(imgRGB)
         main_bbox = []
         if self.results.detections:
             for Id,detection in enumerate(self.results.detections):
            #mpdraw.draw_detection(img, detection)
            #print(Id,detection)ete
                  ih,iw,ic = img.shape
                  bboxC = detection.location_data.relative_bounding_box
                  bbox = int(bboxC.xmin * iw ),int(bboxC.ymin * ih ),\
                   int(bboxC.width * iw ),int(bboxC.height * ih) 
                  main_bbox.append([Id,bbox,detection.score])
                  if draw:
                      img = self.fancy_draw(img,bbox)
                      cv2.putText(img,f'{int(detection.score[0] *100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)      
                      img = self.fancy_draw(img,bbox)
                          
            
         return img,main_bbox
    def fancy_draw(self,img,bbox,l = 30,t = 7):
             
             x,y,w,h = bbox
             x1,y1 =x + w,y+h
             
             cv2.rectangle(img,bbox,(231,156,122),2)
             # top left 
             cv2.line(img,(x,y),(x+l,y),(255,0,255),t)
             # top right
             cv2.line(img,(x+w,y),(x +w -l,y),(255,0,255),t)
             # bottom left 
             cv2.line(img,(x,y+h),(x+l,y +h),(255,0,255),t)
             # bottom right
             cv2.line(img,(x+w,y+h),(x+w-l,y+h),(255,0,255),t)
             return img
             
             
             
         


def main():
    
  
    cap = cv2.VideoCapture("assets/vid2.mp4")
    pTime = 0
    cTime = 0
    detec= faceDetector()
    while True:
        successs,img = cap.read()
        
        img = cv2.resize(img,(1200,720),fx=0,fy=0,interpolation =cv2.INTER_CUBIC)
        image ,main_bbox= detec.findface(img,draw=True)
        print(main_bbox)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image,f' fps {str(int(fps))}',(20,70),cv2.FONT_HERSHEY_COMPLEX,2,(0,213,123),1)      
        cv2.imshow("Image",image)
        if cv2.waitKey(10) == ord('q'):
                 break
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
    