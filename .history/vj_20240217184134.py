import cv2
from ipython import HandDetector  # Check the correct module name
import numpy as np
import math
import time
import os  # Import os module for directory operations
import keyboard
cap = cv2.VideoCapture(0)
detector = HandDetector(max_hands=1)  # Check if the argument is max_hands instead of maxHands
offset = 30
imgSize = 300
folder = "C:/Users/jimve/Documents/CEG-HACKATHON/DATA/A"

# Check if the directory exists, if not, create it
if not os.path.exists(folder):
    os.makedirs(folder)

counter = 0
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
        aspectRatio = h / w
        
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
        
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
    
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    print("Hello")
    ch = keyboard.getch()
    print("hsf"+ch)
    if key == ch: 
        print("Hello55") # Change from "a" to "s"
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(f"Image {counter} saved.")
