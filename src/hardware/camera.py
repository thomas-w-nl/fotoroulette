import random
from os import listdir

import numpy as np
import cv2
from src.common.log import *

CAMERA_H_ANGLE = 62.2


class Camera:
    def get_frame(self):
        """
        krijg de current frame van de camera.
        :rtype: cv2.Mat
        :return: plaatje van de camera
        """

        ret, frame = self._cap.read()
        if frame is None:
            message = "Failed to get feed from cam!"
            log.error(message)
            raise ValueError(message)

        return frame

    photo = 0

    def get_dummy_frame(self, index=0) -> np.array:

        img_path = "img"

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
            raise ValueError("Failed to load img!")

        return frame


    # open camera
    def __init__(self):
        """
        Start de camera
        :rtype: camera
        """
        self._cap = cv2.VideoCapture(0)

        if self._cap.isOpened() == None:
            log.error("Could not open camera")


    # TODO: destruction close camera
    def close_camera(self):
        """
        destructor
        :rtype: void
        """
        self._cap = None


