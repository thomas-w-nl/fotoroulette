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

    def _generate_image(self, index_face_left, index_face_right):
        overlay = cv2.imread(self._overlay)

        overlay_height, overlay_width, overlay_channel = overlay.shape

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, int(overlay_width / 2), overlay_height)

            fg_offset_y = -50
            fg_offset_x = 0
            if i is index_face_right:
                fg_offset_x = -100

            overlay = ov.apply_overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

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

        overlay_height, overlay_width, overlay_channel = overlay.shape

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, int(overlay_width / 2) - 100, overlay_height - 100)

            fg_offset_y = -65
            fg_offset_x = -20
            if i is index_face_right:
                fg_offset_x = -80

            overlay = ov.apply_overlay(overlay, face.face_image, fg_offset_x, fg_offset_y, False)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".png", overlay)

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
        overlay_height, overlay_width, overlay_channel = overlay.shape

        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, int(overlay_width / 2) - 150, overlay_height - 150)

            fg_offset_y = -30
            fg_offset_x = -35
            if i is index_face_right:
                fg_offset_x = -70

            overlay = ov.apply_overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

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