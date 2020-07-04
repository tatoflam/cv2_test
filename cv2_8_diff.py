#!/usr/bin/python 

# coding=UTF-8 
import cv2 
import numpy as np 

ESC = 27         # Escキー 
INTERVAL= 33     # インターバル 

windowOrg = "Original" 
windowDiff = "Difference" 

cv2.namedWindow(windowOrg) 
cv2.namedWindow(windowDiff) 

sourceVideo = cv2.VideoCapture(0)

# read the first frame
hasNext, iFrame = sourceVideo.read()
iFrame = cv2.flip(iFrame, 0)

# read background frmae
bFrame = np.zeros_like(iFrame, np.float32) 

# image conversion
while hasNext == True: 

  # convert image to float 
  fFrame = iFrame.astype(np.float32) 

  #diff 
  dFrame = cv2.absdiff(fFrame, bFrame) 

  # convert to gray scale
  gray = cv2.cvtColor(dFrame.astype(np.uint8), cv2.COLOR_RGB2GRAY) 

  # derive outline
  cannyFrame = cv2.Canny(gray, 50, 110) 

  ret, thresh = cv2.threshold(gray, 127, 255, 0) 
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

  i = 0 
  sv = 0 
  ix = 0 

  for cnt in contours: 
    area = cv2.contourArea(cnt) 
    if  area > sv: 
      sv = area 
      ix = i 
    i = i + 1 

  cx = 0 
  cy = 0 

  if ix > 0 and sv > 10 : 
    M = cv2.moments(contours[ix]) 
    if M['m00'] != 0 : 
      cx = int(M['m10']/M['m00']) 
      cy = int(M['m01']/M['m00']) 
      # print('x:' + str(cx) + ' y:' + str(cy) + ' area:' + str(sv))

  # update background 
  cv2.accumulateWeighted(fFrame, bFrame, 0.025) 

  # display frame
  cv2.imshow(windowOrg, iFrame) 
  cv2.imshow(windowDiff, dFrame.astype(np.uint8)) 

  # shutdown by escape key
  key = cv2.waitKey(INTERVAL) 

  if key == ESC: 
    break 

  # read next frame
  hasNext, iFrame = sourceVideo.read() 
  iFrame = cv2.flip(iFrame, 0)

# finalize
cv2.destroyAllWindows() 
sourceVideo.release() 
