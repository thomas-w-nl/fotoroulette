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
    @staticmethod
    def overlay(bg, fg, offset_x, offset_y):

        rows_fg, cols_fg, channels_fg = fg.shape
        rows_bg, cols_bg, channels_bg = bg.shape

        if offset_x == -1:
            offset_x = int((rows_bg - rows_fg) / 2)

        if offset_y == -1:
            offset_y = int((cols_bg - cols_fg) / 2)

        if (rows_fg > rows_bg) or (cols_fg > cols_bg):
            raise ValueError('Overlay bigger than background')

        if ((offset_x + rows_fg) > rows_bg) or ((offset_y + cols_fg) > cols_bg):
            raise ValueError('offset too big')

        # I want to put logo on top-left corner, So I create a Region of interest (ROI)
        roi_rows_end = offset_x + rows_fg
        roi_cols_end = offset_y + cols_fg

        roi = bg[offset_x:roi_rows_end, offset_y:roi_cols_end]

        # Now create a mask of logo and create its inverse mask also
        gray_fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
        # 0 en 255 zijn cutoff values, we nemen nu de hele fg
        ret, mask = cv2.threshold(gray_fg, 0, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        bg_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # Take only region of logo from logo image.
        fg_fg = cv2.bitwise_and(fg, fg, mask=mask)
        # Put logo in ROI and modify the main image

        dst = cv2.add(bg_bg, fg_fg)

        bg[offset_x:roi_rows_end, offset_y:roi_cols_end] = dst

        return bg

    def generate_image(self):
        bg = cv2.imread(self._photos[0])
        fg = cv2.imread(self._photos[1])

        # todo for each image
        out = Versus.overlay(bg, fg, -1, -1)

        cv2.imshow('out', out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
