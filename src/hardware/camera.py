import random
import numpy as np
import cv2



class Camera:
    CAMERA_H_ANGLE = 62.2

    def take_picture(self) -> np.array:
        # todo dummy data

        image_list = (
            'img/faces.jpg',
            'img/arnold.jpg',
            'img/cryGirl.jpg',
            'img/rogueGirl.jpg',
        )

        pick = random.randrange(0, len(image_list))

        frame = cv2.imread(image_list[pick])
        frame = cv2.imread("../../img/faces.jpg")

        if frame is None:
            raise ValueError("Failed to load img!")

        return frame

    # open camera
    def __init__(self):
        pass

    # TODO: destruction close camera
    def close_camera(self) -> bool:
        pass

