import random

import numpy as np
import cv2


class Camera:
    def take_picture(self) -> np.array:
        # todo dummy data

        image_list = (
            'img/faces.jpg',
            'img/arnold.jpg',
            'img/cryGirl.jpg',
            'img/rogueGirl.jpg',
        )

        pick = random.randrange(50, 200)

        frame = cv2.imread(image_list[pick])
        return frame

    # open camera
    def __init__(self) -> bool:
        pass

    # TODO: destruction close camera
    def close_camera(self) -> bool:
        pass
