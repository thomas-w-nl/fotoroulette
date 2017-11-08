from modules.log import *
import cv2
import numpy as np

log.info("OpenCV version: " + cv2.__version__)
cap = cv2.VideoCapture("bennyLava.avi")
log.debug(cap.read())
while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()