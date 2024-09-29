import numpy as np
import cv2
import autopy
import HandTrackingModule as htm
import time
import pyscreenshot as ImageGrab
import os
from PIL import ImageGrab

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
import pyautogui
smoothening = 7
##########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
print(wScr, hScr)

start = 0

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:#and fingers[0] == 0
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if (fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0):

            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # 10. right Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 255), cv2.FILLED)
                autopy.mouse.click()




        #////////////////for scroll////////////////////////////////////////////////////
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:

            lengthS, imgS, lineInfoS = detector.findDistance(4, 8, img)

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # pyautogui.vscroll(clocY)
            # pyautogui.hscroll(clocX)

            if lengthS < 40:
                cv2.circle(img, (lineInfoS[4], lineInfoS[5]), 10, (0, 255, 255), cv2.FILLED)
                pyautogui.vscroll(-150)
            if lengthS > 200:
                cv2.circle(img, (lineInfoS[4], lineInfoS[5]), 10, (0, 255, 255), cv2.FILLED)
                pyautogui.vscroll(150)
#///////////////////////////screenshot////////////////////////////////////
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            i = 1
            while os.path.exists("screenshot" + str(i) + ".png"):
                i = i + 1
            ImageGrab.grab().save("screenshot" + str(i) + ".png")
            # ImageGrab.grab().show()


        #////////////////for left click ///////////////////////////////////////////////////////////////////////
        # if length < 40:
        #     cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 255, 255), cv2.FILLED)
        #     autopy.mouse.click()
        current = time.time()
        if fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[1] == 0:
            current = time.time()
            pyautogui.press("left")


        # current = time.time(0)
        # if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 :
        #     current = time.time()
        #     pyautogui.press("left")

        #////////////////////////////////////////////////////////////
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display

    cv2.imshow("Image", img)
    cv2.waitKey(1)
