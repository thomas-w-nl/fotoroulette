from cv2 import cv2

import numpy as np

# todo moet ook image path en face image offsets bevatten voor elke game type
from src.processing.get_faces import Face


class GameType:
    VERSUS = 0
    SUPERHEROES = 1
    ROULETTE = 2
    LOVEMETER = 3


def apply_overlay(frame: np.array, overlay: GameType) -> np.array:
    pass


def resize_fit(image: np.array, max_width: int, max_height: int) -> np.array:

    width, height, channels = image.shape

    scale_width = max_width / width
    scale_height = max_height / width

    print(scale_width, scale_height)

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    return res
