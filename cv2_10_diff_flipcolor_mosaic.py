#!/usr/bin/python 

# coding=UTF-8 
import cv2 
import numpy as np 

ESC = 27         # Escキー 
INTERVAL= 33     # インターバル 

windowOrg = "Original" 
windowDiff = "Difference" 
windowInvertDiff = "InvertDifference" 
windowMosaic = "Mosaic" 


cv2.namedWindow(windowOrg, cv2.WINDOW_NORMAL) 
cv2.namedWindow(windowDiff, cv2.WINDOW_NORMAL) 
cv2.namedWindow(windowInvertDiff, cv2.WINDOW_NORMAL) 
cv2.namedWindow(windowMosaic, cv2.WINDOW_NORMAL) 

sourceVideo = cv2.VideoCapture(0)

# read the first frame
hasNext, iFrame = sourceVideo.read()
height = iFrame.shape[0]
width = iFrame.shape[1]
# got integer result deviding values by "//"
iFrame = cv2.resize(iFrame, (width//2, height//2))

iFrame = cv2.flip(iFrame, 0)

# read background frame
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

  # invert color
  idFrame = cv2.bitwise_not(dFrame.astype(np.uint8))

  # convert to mosaic
  ratio=0.05
  imageSmall = cv2.resize(idFrame, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
  mFrame = cv2.resize(imageSmall, idFrame.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

  # display frame
  cv2.imshow(windowOrg, iFrame) 
  cv2.imshow(windowDiff, dFrame.astype(np.uint8)) 
  cv2.imshow(windowInvertDiff, idFrame.astype(np.uint8)) 
  cv2.imshow(windowMosaic, mFrame.astype(np.uint8)) 

  # shutdown by escape key
  key = cv2.waitKey(INTERVAL) 

  if key == ESC: 
    break 

  # read next frame
  hasNext, iFrame = sourceVideo.read() 
  iFrame = cv2.resize(iFrame, (width//2, height//2))
  iFrame = cv2.flip(iFrame, 0)

# finalize
cv2.destroyAllWindows() 
sourceVideo.release() 
