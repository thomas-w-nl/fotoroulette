import configparser
import time

import cv2
import numpy as np
from picamera import PiCamera
# import the necessary packages
from picamera.array import PiRGBArray


# from src.common.log import *


class Camera:
    def get_frame(self):
        """
        Krijg de current frame van de camera.

        Returns:
           Een plaatje van de camera.
        """
        camera_config = configparser.ConfigParser().read('fotoroulette.conf')['Camera']
        width = camera_config.getint('CAMERA_RESOLUTION_H')
        height = camera_config.getint('CAMERA_RESOLUTION_V')

        # The horizontal resolution is rounded up to the nearest multiple of 32 pixels.
        buffer_width = int(np.math.ceil(width / 32) * 32)
        # The vertical resolution is rounded up to the nearest multiple of 16 pixels.
        buffer_height = int(np.math.ceil(height / 16) * 16)

        # create an empty buffer, with accommodation for image resolution rounding
        image = np.empty((buffer_height * buffer_width * 3,), dtype=np.uint8)

        self.camera.capture(image, 'bgr')

        # reshape buffer to image dimensions
        image = image.reshape((buffer_height, buffer_width, 3))

        if image is None:
            message = "Failed to get feed from camera!"
            # log.error(message)
            raise ValueError(message)

        # reshape buffer to requested resolution
        image = image[:height, :width, :]

        return image

    def __init__(self):
        """
        Start de camera
        """
        self.camera = PiCamera()

        # self.rawCapture = PiRGBArray(self.camera)  # dit is redundant volgens mij

        camera_config = configparser.ConfigParser().read('fotoroulette.conf')['Camera']
        width = camera_config.getint('CAMERA_RESOLUTION_H')
        height = camera_config.getint('CAMERA_RESOLUTION_V')
        self.camera.resolution = [width, height]
        # allow camera to warm up
        time.sleep(2)

        if self.camera is None:
            log.error("Could not open camera")

    def close_camera(self):
        """
        Destructor
        """
        self.camera.close()


if __name__ == "__main__":
    print("test")

    cam = Camera()
    img = cam.get_frame()
    cv2.imshow("photo", img)
    cv2.waitKey()
