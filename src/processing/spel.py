import random
import uuid
from enum import Enum

import os

from src.processing import collect_photos
from src.processing import get_faces
from src.processing import overlay as ov

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Games(Enum):
    VERSUS = 0
    SUPERHEROES = 1
    LOVEMETER = 2


class Game:
    def __init__(self, overlay):
        self._game_id = uuid.uuid4()
        self.overlay = overlay
        self.faces = []

    def get_faces(self):
        """
        This will start taking pictures and cutting the faces out of them to use in the image
        """
        self.faces = get_faces.get_faces(collect_photos.collect_photos())

    def _random_images(self) -> (int, int):
        """
        This will pick 2 different random indexes of the [_face] property
        :return: tuple with the 2 indexes
        """
        rand1 = random.randint(0, len(self.faces) - 1)
        rand2 = random.randint(0, len(self.faces) - 1)

        while rand1 == rand2:
            rand2 = random.randint(0, len(self.faces) - 1)

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
    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Versus, self).get_faces()

        if len(self.faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(Versus, self)._random_images()

        return ov.generate_overlay(self, rand1, rand2, -50, 0, 0, -100)


class Superheroes(Game):
    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Superheroes, self).get_faces()
        if len(self.faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(Superheroes, self)._random_images()

        return ov.generate_overlay(self, rand1, rand2, -65, 100, -20, -80)


class LoveMeter(Game):
    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(LoveMeter, self).get_faces()
        if len(self.faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

        rand1, rand2 = super(LoveMeter, self)._random_images()

        return ov.generate_overlay(self, rand1, rand2, -30, 150, -35, -70)
