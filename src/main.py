from src.hardware.camera import Camera
import src.common.tools as tools
from src.common.log import *
import cv2

from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces

data = collect_photos()

for photo in data._photos:
    cv2.imshow("Input photo's", photo)
    cv2.waitKey()

faces = get_faces(data)

for face in faces:
    cv2.imshow("output", face.face_image)
    log.info("Face appended:" + str(face.confidence))
    cv2.waitKey()


log.info("great succes!")
