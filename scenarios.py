import uuid

import cv2
import os

import numpy

from PIL import Image

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

    def push_foto(self, photo):
        self._photos.append(photo)

    def bewerk(self, index):
        return self._photos[index]

    def clear(self):
        self._photos = []


class Versus(Game):

    def generate_image(self):
        PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        overlay = cv2.imread(PROJECT_ROOT_DIR + "/assets/overlays/versus.png")

        # image1 = cv2.imread(PROJECT_ROOT_DIR + "/" + self._photos[0])

        # image2 = cv2.imread(PROJECT_ROOT_DIR + "/" + self._photos[1])

        # TODO: combine image1 and image2 to fixed size image

        #
        # output_image = cv2.addWeighted(image1, 1.0, overlay, 1.0, 0)

        background = Image.open(self._photos[0])
        overlay = Image.open(PROJECT_ROOT_DIR + "/assets/overlays/versus.png")

        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")

        text_img = Image.new('RGBA', (DEFAULT_WIDTH, DEFAULT_HEIGHT), (0, 0, 0, 0))
        text_img.paste(background, (0, 0))
        text_img.paste(overlay, (0, 0), mask=overlay)
        text_img.save(PROJECT_ROOT_DIR + "/assets/generated_output/" + str(self._game_id) + ".jpg", format="png")
