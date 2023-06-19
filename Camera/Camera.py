import cv2
import math
import numpy as np

cap = cv2.VideoCapture(2)

if not cap.isOpened():
  raise Exception("Could not open video device")

while True:
  ret, frame = cap.read()
  
  frame = np.array(frame)

  cv2.imshow('frame', frame)

  if cv2.waitKey(1) == ord('q'):
    break

print(math.atan((27 / 50)))