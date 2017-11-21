import random
from os import listdir

import numpy as np
import cv2
from src.common.log import *

# TODO moet dit niet in de camera class?
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


