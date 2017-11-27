import random
import uuid
from enum import Enum

import cv2
import os

from src.processing import collect_photos
from src.processing import get_faces
from src.processing import overlay as ov

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
    def __init__(self, name, overlay):
        """
        :param name: Name of the game
        :param bg: background
        :param fg_list: list of images with offsets to overlay
        """
        self._game_id = uuid.uuid4()
        self.name = name
        self._overlay = overlay
        self._faces = []

    def play(self):
        self._faces = get_faces.get_faces(collect_photos.collect_photos())

    def end_game(self):
        # 1) ask user if them want to play another game
            # if so, show select screen
            # else, show end screen, upload photos and show code for website
        return

    def clear(self):
        # todo: clear
        return


class Versus(Game):
    @staticmethod
    def _overlay(overlay, face, offset_x, offset_y):

        rows_fg, cols_fg, channels_fg = face.shape
        rows_overlay, cols_bg, channels_bg = overlay.shape

        if (offset_x < -100) or (offset_x < -100):
            raise ValueError('offset more than 100%')

        # negative numbers from -100 to 1 are percentage offsets
        if offset_y < 0:
            offset_y_percentage = offset_y * -0.01
            offset_y = int((rows_overlay - rows_fg) * offset_y_percentage)

        if offset_x < 0:
            offset_x_percentage = offset_x * -0.01
            offset_x = int((cols_bg - cols_fg) * offset_x_percentage)

        if (rows_fg > rows_overlay) or (cols_fg > cols_bg):
            raise ValueError('Overlay bigger than background')

        if ((offset_y + rows_fg) > rows_overlay) or ((offset_x + cols_fg) > cols_bg):
            raise ValueError('offset too big')

        # I want to put logo on top-left corner, So I create a Region of interest (ROI)
        roi_rows_end = offset_y + rows_fg
        roi_cols_end = offset_x + cols_fg

        roi = overlay[offset_y:roi_rows_end, offset_x:roi_cols_end]

        # Now black-out the area of logo in ROI
        bg_bg = cv2.bitwise_and(roi, roi)
        # Take only region of logo from logo image.
        face_face = cv2.bitwise_and(face, face)
        # Put logo in ROI and modify the main image

        dst = cv2.add(bg_bg, face_face)

        final = overlay

        final[offset_y:roi_rows_end, offset_x:roi_cols_end] = dst

        return final

    def _generate_image(self, index_face_left, index_face_right):

        overlay = cv2.imread(self._overlay)

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, DEFAULT_WIDTH, DEFAULT_HEIGHT)

            fg_offset_y = 0
            fg_offset_x = 0
            if i is index_face_right:
                fg_offset_x = DEFAULT_WIDTH

            overlay = Versus._overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

        # cv2.imshow('out', overlay)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def play(self):
        super(Versus, self).play()

        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1 = random.randint(0, len(self._faces) - 1)
        rand2 = random.randint(0, len(self._faces) - 1)

        while rand1 == rand2:
            rand2 = random.randint(0, len(self._faces) - 1)

        self._generate_image(rand1, rand2)
        # 2) end game


class Superheroes(Game):
    def _generate_image(self, index_face_left, index_face_right):

        overlay = cv2.imread(self._overlay)

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, DEFAULT_WIDTH, DEFAULT_HEIGHT)

            fg_offset_y = 0
            fg_offset_x = 0
            if i is index_face_right:
                fg_offset_x = DEFAULT_WIDTH

            overlay = Versus._overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

        # cv2.imshow('out', overlay)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def play(self):
        super(Superheroes, self).play()
        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1 = random.randint(0, len(self._faces) - 1)
        rand2 = random.randint(0, len(self._faces) - 1)

        while rand1 == rand2:
            rand2 = random.randint(0, len(self._faces) - 1)

        self._generate_image(rand1, rand2)
        # 2) end game


class LoveMeter(Game):
    def _generate_image(self, index_face_left, index_face_right):

        overlay = cv2.imread(self._overlay)

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, DEFAULT_WIDTH, DEFAULT_HEIGHT)

            fg_offset_y = 0
            fg_offset_x = 0
            if i is index_face_right:
                fg_offset_x = DEFAULT_WIDTH

            overlay = Versus._overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

        # cv2.imshow('out', overlay)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def play(self):
        super(LoveMeter, self).play()
        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1 = random.randint(0, len(self._faces) - 1)
        rand2 = random.randint(0, len(self._faces) - 1)

        while rand1 == rand2:
            rand2 = random.randint(0, len(self._faces) - 1)

        self._generate_image(rand1, rand2)
        # 2) end game