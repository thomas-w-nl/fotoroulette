import uuid
from enum import Enum

import cv2
import os

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 250


class Games(Enum):
    VERSUS = 0
    SUPERHEROES = 1
    LOVEMETER = 2


def new_game(game, name, photos):
    if game == Games.VERSUS:
        return Versus(name, photos)
    elif game == Games.SUPERHEROES:
        return Superheroes(name, photos)
    elif game == Games.LOVEMETER:
        return LoveMeter(name, photos)


class Game:
    def __init__(self, name, bg, fg_list):
        """
        :param name: Name of the game
        :param bg: background
        :param fg_list: list of images with offsets to overlay
        """
        self._game_id = uuid.uuid4()
        self.name = name
        self._bg = bg
        self._fg_list = fg_list

    def push_photo(self, photo):
        """
        Push a photo to the photos array
        :param photo: path of the image
        """
        self._photos.append(photo)

    def play(self):
        # 1) turn to each position
            # check if someone in front of it (and if between given "play" range
            # if so, take pictures on position
        # 2) for each picture get faces and save
        return

    def end_game(self):
        # 1) ask user if them want to play another game
            # if so, show select screen
            # else, show end screen, upload photos and show code for website
        return

    def clear(self):
        self._photos = []


class Versus(Game):
    @staticmethod
    def overlay(bg, fg, offset_x, offset_y):

        rows_fg, cols_fg, channels_fg = fg.shape
        rows_bg, cols_bg, channels_bg = bg.shape

        if (offset_x < -100) or (offset_x < -100):
            raise ValueError('offset more than 100%')

        # negative numbers from -100 to 1 are percentage offsets
        if offset_y < 0:
            offset_y_percentage = offset_y * -0.01
            offset_y = int((rows_bg - rows_fg) * offset_y_percentage)

        if offset_x < 0:
            offset_x_percentage = offset_x * -0.01
            offset_x = int((cols_bg - cols_fg) * offset_x_percentage)

        if (rows_fg > rows_bg) or (cols_fg > cols_bg):
            raise ValueError('Overlay bigger than background')

        if ((offset_y + rows_fg) > rows_bg) or ((offset_x + cols_fg) > cols_bg):
            raise ValueError('offset too big')

        # I want to put logo on top-left corner, So I create a Region of interest (ROI)
        roi_rows_end = offset_y + rows_fg
        roi_cols_end = offset_x + cols_fg

        roi = bg[offset_y:roi_rows_end, offset_x:roi_cols_end]

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

        bg[offset_y:roi_rows_end, offset_x:roi_cols_end] = dst

        return bg

    def generate_image(self):

        bg = cv2.imread(self._bg)

        for fg_i in self._fg_list:
            fg_i_img = cv2.imread(fg_i[0])
            fg_offset_x = fg_i[1]
            fg_offset_y = fg_i[2]

            bg = Versus.overlay(bg, fg_i_img, fg_offset_x, fg_offset_y)

        cv2.imshow('out', bg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def play(self):
        self.play()
        # 1) choose pairs of 2 and generate a Versus overlay and show them on the screen.
        # (if more than 2 continue until every player has a Versus picture of them)

        # 2) end game
        return


class Superheroes(Game):
    def generate_image(self):
        # 1) choose pairs of 2 and generate a Superheroes overlay and show them on the screen.
        # (if more than 2 continue until every player has a Superheroes picture of them)

        # 2) end game
        return

    def play(self):
        self.play()
        return


class LoveMeter(Game):
    def generate_image(self):
        return

    def play(self):
        # 1) choose pairs of 2 and generate a Lovemeter overlay and show them on the screen.
        # (if more than 2 continue until every player has a Versus picture of them)

        # 2) end game
        super.end_game();
        return
