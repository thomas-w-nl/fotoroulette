from os import listdir

import numpy as np
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# from src.common.log import *

CAMERA_H_FOV = 62.2



class Camera:
    def get_frame(self):
        """
        krijg de current frame van de camera.
        :rtype: cv2.Mat
        :return: plaatje van de camera
        """

        # grab an image from the camer
        image = self.rawCapture.array

        if image is None:
            message = "Failed to get feed from cam!"
            # log.error(message)
            raise ValueError(message)

        return image

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
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.resolution = (3296, 2464)  # 2592, 1952
        time.sleep(0.1)

        if self.camera == None:
            # log.error("Could not open camera")
            print("Error opening camera and log is broken")

    # TODO: destruction close camera
    def close_camera(self):
        """
        destructor
        :rtype: void
        """
        self.camera.close()


if __name__ == "__main__":
    cam = Camera()
    img = cam.get_frame()
    cv2.imwrite('photo.png', img)
