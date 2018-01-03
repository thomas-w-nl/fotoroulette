import random
import uuid
from enum import Enum

import os
from src.processing import overlay as ov

PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Games(Enum):
    VERSUS = 0
    SUPERHEROES = 1
    LOVEMETER = 2
    WANTED = 3


def game_by_type(game_type, faces):
    """
    This returns the [Game] object associated with the [game_type]

    Args:
        game_type: a [Games] type which represents the game type
        faces: the collected faces

    Returns:
         the corresponding [Game] object
    """
    if game_type is Games.VERSUS:
        return Versus(faces)
    elif game_type is Games.SUPERHEROES:
        return Superheroes(faces)
    elif game_type is Games.LOVEMETER:
        return LoveMeter(faces)
    elif game_type is Games.WANTED:
        return Wanted(faces)


class Game:
    def __init__(self, faces):
        self._game_id = uuid.uuid4()
        self.overlay = None
        self.on_top = False
        self.background_color = None
        self.faces = faces
        self.player_count = 2
        self.offsets = []
        self.extra_background = None

    def _random_images(self):
        """
        This will pick 2 different random indexes of the [_face] property

        Returns:
             tuple with the 2 indexes
        """
        if self.player_count > len(self.faces):
            raise ValueError("To few faces to generate an overlay")

        random.shuffle(self.faces)

        diff = len(self.faces) - self.player_count

        self.faces = self.faces[diff:]


class Versus(Game):
    def __init__(self, faces):
        super(Versus, self).__init__(faces)

        self.on_top = True
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

        super(Versus, self)._random_images()

        return ov.generate_overlay(self)


class Wanted(Game):
    def __init__(self, faces):
        super(Wanted, self).__init__(faces)

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

        super(Wanted, self)._random_images()

        return ov.generate_overlay(self)


class Superheroes(Game):
    def __init__(self, faces):
        super(Superheroes, self).__init__(faces)

        self.player_count = 7
        self.on_top = True
        self.extra_background = "assets/overlays/superheroes_solid.png"
        self.overlay = "assets/overlays/superheroes_transparent.png"
        self.offsets = [
            {
                'offset_y': -10,
                'offset_x': -47,
                'minus_image_width': 270
            },
            {
                'offset_y': -35,
                'offset_x': -29,
                'minus_image_width': 270
            },
            {
                'offset_y': -36,
                'offset_x': -67,
                'minus_image_width': 270
            },
            {
                'offset_y': -52,
                'offset_x': -19,
                'minus_image_width': 275
            },
            {
                'offset_y': -50,
                'offset_x': -80,
                'minus_image_width': 280
            },
            {
                'offset_y': -64,
                'offset_x': -91,
                'minus_image_width': 275
            },
            {
                'offset_y': -56.5,
                'offset_x': -9,
                'minus_image_width': 280
            }
        ]

    def gen_overlay(self):
        """
        This will start the scenario.
        It is possible here to add user interation
        """

        super(Superheroes, self)._random_images()

        return ov.generate_overlay(self)


class LoveMeter(Game):
    def __init__(self, faces):
        super(LoveMeter, self).__init__(faces)

        self.overlay = "assets/overlays/lovemeter.png"
        self.background_color = [249, 81, 161]
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

        super(LoveMeter, self)._random_images()

        return ov.generate_overlay(self)
