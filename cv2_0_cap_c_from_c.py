import cv2

camera = cv2.VideoCapture(0)

_, frame = camera.read()

cv2.imwrite('../img_test/test-cv.jpg', frame)
