import time

import cv2
import numpy as np
from picamera import PiCamera
# import the necessary packages
from picamera.array import PiRGBArray

# from src.common.log import *

CAMERA_H_FOV = 62.2
CAMERA_RESOLUTION = [1664, 928]  # [3280, 246]  # (2592, 1952) (1920, 1080)


class Camera:
    def get_frame(self):
        """
        Krijg de current frame van de camera.

        Returns:
           Een plaatje van de camera.
        """
        width, height = CAMERA_RESOLUTION

        # grab an image from the camera
        self.camera.resolution = (width, height)
        self.camera.framerate = 24
        time.sleep(2)

        # The horizontal resolution is rounded up to the nearest multiple of 32 pixels.
        buffer_width = int(np.math.ceil(width / 32) * 32)
        # The vertical resolution is rounded up to the nearest multiple of 16 pixels.
        buffer_height = int(np.math.ceil(height / 16) * 16)

        image = np.empty((buffer_height * buffer_width * 3,), dtype=np.uint8)
        self.camera.capture(image, 'bgr')
        image = image.reshape((height, width, 3))

        if image is None:
            message = "Failed to get feed from camera!"
            # log.error(message)
            raise ValueError(message)

        return image

    # open camera
    def __init__(self):
        """
        Start de camera
        """
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.resolution = CAMERA_RESOLUTION
        # allow camera to warm up
        time.sleep(2)

        if self.camera == None:
            # log.error("Could not open camera")
            print("Error opening camera and log is broken")

    # TODO: destruction close camera
    def close_camera(self):
        """
        destructor
        """
        self.camera.close()


if __name__ == "__main__":
    cam = Camera()

    img = cam.get_frame()
    cv2.imwrite('photo.png', img)
