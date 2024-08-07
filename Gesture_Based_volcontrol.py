import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# video capture height and width...
wcam , hcam =  550,480

video = cv2.VideoCapture(0)
video.set(3,wcam)
video.set(4,hcam)
ptime = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minvol = volRange[0]
maxvol = volRange[1]
detector = htm.FindHands()
while True:
    success, img = video.read()

    img, lmlist = detector.getPosition(img,[4,8])
    if len(lmlist) != 0:
        x1,y1 = lmlist[0][0],lmlist[0][1]
        x2,y2 = lmlist[1][0],lmlist[1][1]
        cx,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img,(x1,y1),15 , (255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
        cv2.circle(img,(cx,cy),15 , (255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        vol = np.interp(length,[50,300],[minvol , maxvol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length <50:
            cv2.circle(img , (cx,cy) ,15,(0,255,0),cv2.FILLED)
        if length >= 300:
            cv2.circle(img , (cx,cy) ,15,(0,0,255),cv2.FILLED)
    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img,f'fps:{int(fps)}',(40 ,50) , cv2.FONT_HERSHEY_COMPLEX, 1,(250,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)