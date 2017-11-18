import cv2
import numpy as np
from src.processing.photo_data import PhotoData

MIN_FACE_CONFIDENCE = 0.5


def get_faces(photos_with_data: PhotoData) -> list:
    faces = ()

    for single_photo in photos_with_data:
        print(single_photo)


        #     imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     face_cascade = cv2.CascadeClassifier("/home/thomas/PycharmProjects/raspberry-pi/haarCascades"
        #                                          "/haarcascade_frontalface_default.xml")
        #
        #     if face_cascade == None:
        #         print("Face cascade failed to load!")
        #         quit(1)
        #
        #     # faces_with_levels[0]= faces
        #     #  faces_with_levels[1]= reject_levels?
        #     #  faces_with_levels[2]= confidence_weights
        #
        #     faces_with_levels = face_cascade.detectMultiScale3(
        #         imgGrey,
        #         scaleFactor=1.1,
        #         minNeighbors=5,
        #         minSize=(30, 30),
        #         flags=cv2.CASCADE_SCALE_IMAGE,
        #         outputRejectLevels=True
        #     )
        #
        # pass


def crop_image(img: np.array, rect: list) -> np.array:
    pass
