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
    WANTED = 3


class Game:
    def __init__(self):
        self._game_id = uuid.uuid4()
        self.overlay = None
        self.on_top = False
        self.faces = []
        self.player_count = 2
        self.offsets = []

    def _get_faces(self):
        """
        This will start taking pictures and cutting the faces out of them to use in the image
        """
        self.faces = get_faces.get_faces(collect_photos.collect_photos())
        if len(self.faces) < 2:
            raise ValueError("Cannot play with less than 2 faces")

    def _random_images(self):
        """
        This will pick 2 different random indexes of the [_face] property
        :return: tuple with the 2 indexes
        """
        if self.player_count > len(self.faces):
            raise ValueError("To few faces to generate an overlay")

        random.shuffle(self.faces)

        diff = len(self.faces) - self.player_count

        self.faces = self.faces[diff:]


def new_game(game_type: Games) -> Game:
    """
    Returns a new [Game] object based on the [game_type] parameter
    :param game_type:
    :param overlay:
    :return:
    """
    if game_type == Games.VERSUS:
        return Versus()
    elif game_type == Games.SUPERHEROES:
        return Superheroes()
    elif game_type == Games.LOVEMETER:
        return LoveMeter()
    elif game_type == Games.WANTED:
        return Wanted()


class Versus(Game):
    def __init__(self):
        super(Versus, self).__init__()

        self.overlay = "assets/overlays/versus.png"
        self.player_count = 2
        self.offsets = [
            {
                'offset_y': -50,
                'offset_x': 0,
                'minus_image_width': 0
            },
            {
                'offset_y': -50,
                'offset_x': -100,
                'minus_image_width': 0
            }
        ]

    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Versus, self)._get_faces()
        super(Versus, self)._random_images()

        return ov.generate_overlay(self)


class Wanted(Game):
    def __init__(self):
        super(Wanted, self).__init__()

        self.overlay = "assets/overlays/wanted.png"
        self.on_top = True
        self.player_count = 1
        self.offsets = [
            {
                'offset_y': -50,
                'offset_x': -50,
                'minus_image_width': 120
            },
        ]

    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Wanted, self)._get_faces()
        super(Wanted, self)._random_images()

        return ov.generate_overlay(self)


class Superheroes(Game):
    def __init__(self):
        super(Superheroes, self).__init__()

        self.overlay = "assets/overlays/superheroes.png"
        self.player_count = 3
        self.offsets = [
            {
                'offset_y': -45,
                'offset_x': -41,
                'minus_image_width': 220
            },
            {
                'offset_y': -45,
                'offset_x': -58,
                'minus_image_width': 220
            },
            {
                'offset_y': -85,
                'offset_x': -41,
                'minus_image_width': 220
            },
            {
                'offset_y': -85,
                'offset_x': -58,
                'minus_image_width': 220
            },
            {
                'offset_y': -45,
                'offset_x': -24,
                'minus_image_width': 220
            },
            {
                'offset_y': -45,
                'offset_x': -75,
                'minus_image_width': 220
            },
            {
                'offset_y': -85,
                'offset_x': -24,
                'minus_image_width': 220
            },
            {
                'offset_y': -85,
                'offset_x': -75,
                'minus_image_width': 220
            },
        ]

    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Superheroes, self)._get_faces()
        super(Superheroes, self)._random_images()

        return ov.generate_overlay(self)


class LoveMeter(Game):
    def __init__(self):
        super(LoveMeter, self).__init__()

        self.overlay = "assets/overlays/lovemeter.png"
        self.on_top = True
        self.player_count = 2
        self.offsets = [
            {
                'offset_y': -30,
                'offset_x': -35,
                'minus_image_width': 150
            },
            {
                'offset_y': -30,
                'offset_x': -70,
                'minus_image_width': 150
            },
        ]

    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(LoveMeter, self)._get_faces()
        super(LoveMeter, self)._random_images()

        return ov.generate_overlay(self)
