# from common import tools, log ?
from common.log import *
from hardware.camera import Camera
from processing.collect_photos import collect_photos
from processing.get_faces import get_faces

import common.tools as tools
import cv2

if __name__ == "__main__":
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
