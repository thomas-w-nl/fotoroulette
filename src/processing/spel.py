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


class Game:
    def __init__(self, overlay):
        self._game_id = uuid.uuid4()
        self._overlay = overlay
        self._faces = []

    def play(self):
        """
        This will start taking pictures and cutting the faces out of them to use in the game
        """
        self._faces = get_faces.get_faces(collect_photos.collect_photos())

    def end_game(self):
        # 1) ask user if them want to play another game
            # if so, show select screen
            # else, show end screen, upload photos and show code for website
        return

    def _random_images(self) -> (int, int):
        """
        This will pick 2 different random indexes of the [_face] property
        :return: tuple with the 2 indexes
        """
        rand1 = random.randint(0, len(self._faces) - 1)
        rand2 = random.randint(0, len(self._faces) - 1)

        while rand1 == rand2:
            rand2 = random.randint(0, len(self._faces) - 1)

        return rand1, rand2


def new_game(game_type: Games, overlay: str) -> Game:
    """
    Returns a new [Game] object based on the [game_type] parameter
    :param game_type:
    :param overlay:
    :return:
    """
    if game_type == Games.VERSUS:
        return Versus(overlay)
    elif game_type == Games.SUPERHEROES:
        return Superheroes(overlay)
    elif game_type == Games.LOVEMETER:
        return LoveMeter(overlay)


class Versus(Game):
    def _generate_image(self, index_face_left, index_face_right):
        """
        Will generate the image with the two given face indexes and applies the overlay
        :param index_face_left: face 1 overlay
        :param index_face_right: face 2 overlay
        """

        overlay = cv2.imread(self._overlay)

        overlay_height, overlay_width, overlay_channel = overlay.shape

        # add each image to the overlay with the given x/y values
        for i in [index_face_left, index_face_right]:
            face = self._faces[i]

            face.face_image = ov.resize_fit(face.face_image, int(overlay_width / 2), overlay_height)

            fg_offset_y = -50
            fg_offset_x = 0

            # move second image to the right
            if i is index_face_right:
                fg_offset_x = -100

            # apply face to the final image
            overlay = ov.apply_overlay(overlay, face.face_image, fg_offset_x, fg_offset_y)

        # write final image to disk
        cv2.imwrite("assets/generated_output/" + str(uuid.uuid4()) + ".jpg", overlay)

    def play(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Versus, self).play()

        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(Versus, self)._random_images()

        self._generate_image(rand1, rand2)
        # 2) end game


class Superheroes(Game):
    def _generate_image(self, index_face_left, index_face_right):
        """
        Will generate the image with the two given face indexes and applies the overlay
        :param index_face_left: face 1 overlay
        :param index_face_right: face 2 overlay
        """

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
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Superheroes, self).play()
        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(Superheroes, self)._random_images()

        self._generate_image(rand1, rand2)
        # 2) end game


class LoveMeter(Game):
    def _generate_image(self, index_face_left, index_face_right):
        """
        Will generate the image with the two given face indexes and applies the overlay
        :param index_face_left: face 1 overlay
        :param index_face_right: face 2 overlay
        """

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
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(LoveMeter, self).play()
        if len(self._faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(LoveMeter, self)._random_images()

        self._generate_image(rand1, rand2)
        # 2) end game