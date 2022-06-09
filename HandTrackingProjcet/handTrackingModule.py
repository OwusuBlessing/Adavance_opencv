
# # -*- coding: utf-8 -*-

# The hand tracking mediapipe uses handlandmarks and palm detection

# import libraries
import cv2
import mediapipe as mp
import time # to check frame rate



class  handdetector():
    def __init__(self,mode =False,maxhands = 2,modelC = 1,detecCon = 0.5,TrackConf = 0.5):
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
                 
                 #print(Id,lm)
                 

def main():
    
# create video obejct
    cap = cv2.VideoCapture(0)
    detector = handdetector()
  
    pTime =0
    cTime = 0
    
    while True:
        success,img = cap.read()
        image = detector.find_hands(img)
        lmlist = detector.getposition(img,draw = True)
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
   
if __name__ == "__main__":
        main()
