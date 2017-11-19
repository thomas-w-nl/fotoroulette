import random
from os import listdir

import numpy as np
import cv2

CAMERA_H_ANGLE = 62.2


class Camera:
    def take_picture(self) -> np.array:
        # todo dummy data


        image_list = listdir("../../img")

        pick = random.randrange(0, len(image_list))

        frame = cv2.imread("../../img/" + str(image_list[pick]))

        if frame is None:
            raise ValueError("Failed to load img!")

        return frame

    # open camera
    def __init__(self):
        pass

    # TODO: destruction close camera
    def close_camera(self) -> bool:
        pass
