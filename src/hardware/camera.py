import random
from os import listdir, getcwd

import numpy as np
import cv2
from src.common.log import *

CAMERA_H_FOV = 62.2


class Camera:
    photo = 0

    # open camera
    def __init__(self):
        """
        Start de camera
        """
        self._cap = cv2.VideoCapture(0)

        if self._cap.isOpened() == None:
            log.error("Could not open camera")

    def get_frame(self):
        """
        Krijg de current frame van de camera.

        Returns:
           Een plaatje van de camera.
        """

        ret, frame = self._cap.read()
        if frame is None:
            message = "Failed to get feed from cam!"
            log.error(message)
            raise ValueError(message)

        return frame

    def get_dummy_frame(self, index=0) -> np.array:
        print(getcwd())
        img_path = "../img"

        # Crasht het hier? Check je working dir in run config!
        image_list = listdir(img_path)

        if self.photo == (len(image_list) - 1):
            self.photo = 0
        else:
            self.photo += 1

        pick = self.photo

        if index != 0:
            pick = index

        frame = cv2.imread(img_path + "/" + str(image_list[pick]))

        if frame is None:
            log.error("Failed to load image!")

        return frame



    # TODO: destruction close camera
    def close_camera(self):
        """
        destructor
        """
        self._cap = None
