import uuid

import cv2
import os

import numpy as np

from PIL import Image

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 250


class Game:

    def __init__(self, name, photos):
        """
        :param name: Name of the game
        :param photos:
        """
        self._game_id = uuid.uuid4()
        self.name = name
        self._photos = photos

    def push_photo(self, photo):
        """
        Push a photo to the photos array
        :param photo: String: path of the image
        """
        self._photos.append(photo)

    def clear(self):
        self._photos = []


class Versus(Game):

    def generate_image(self):
        img1 = cv2.imread(self._photos[0])
        img2 = cv2.imread(self._photos[1])

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        # create empty matrix
        background = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

        # combine 2 images
        background[:h1, :w1, :3] = img1
        background[:h2, w1:w1 + w2, :3] = img2

        # load overlay
        overlay = Image.open(PROJECT_ROOT_DIR + "/assets/overlays/versus.png")
        overlay = overlay.convert("RGBA")

        # generate final image
        gen_img = Image.new('RGBA', (DEFAULT_WIDTH, DEFAULT_HEIGHT), (0, 0, 0, 0))
        gen_img.paste(img1, (0, 0))
        gen_img.paste(overlay)
        gen_img.save(PROJECT_ROOT_DIR + "/assets/generated_output/" + str(self._game_id) + ".jpg", format="png")
