import configparser
import time
import cv2
import numpy as np
from picamera import PiCamera
from src.common import log


class Camera:
    def get_frame(self):
        """
        Krijg de current frame van de camera.

        Returns:
           Een plaatje van de camera.
        """
        config = configparser.ConfigParser()
        config.read('fotoroulette.conf')

        width = config['Camera'].getint('CAMERA_RESOLUTION_H')
        height = config['Camera'].getint('CAMERA_RESOLUTION_V')

        # The horizontal resolution is rounded up to the nearest multiple of 32 pixels.
        buffer_width = int(np.math.ceil(width / 32) * 32)
        # The vertical resolution is rounded up to the nearest multiple of 16 pixels.
        buffer_height = int(np.math.ceil(height / 16) * 16)

        # create an empty buffer, with accommodation for image resolution rounding
        buffer = np.empty((buffer_height * buffer_width * 3,), dtype=np.uint8)

        self.camera.capture(buffer, 'bgr')

        # reshape buffer to image dimensions
        image = buffer.reshape((buffer_height, buffer_width, 3))

        if image is None:
            log.error("Failed to get feed from camera!")

        # reshape buffer to requested resolution
        image = image[:height, :width, :]

        return image

    def __init__(self):
        """
        Start de camera
        """
        self.camera = PiCamera()

        # self.rawCapture = PiRGBArray(self.camera)  # dit is redundant volgens mij

        config = configparser.ConfigParser()
        config.read('fotoroulette.conf')

        width = config['Camera'].getint('CAMERA_RESOLUTION_H')
        height = config['Camera'].getint('CAMERA_RESOLUTION_V')
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
