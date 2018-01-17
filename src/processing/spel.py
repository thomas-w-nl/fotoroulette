import yaml
import random
import uuid
from enum import Enum
from src.thread import FRICP

from src.processing import overlay as ov

with open("games.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile)


class Games(Enum):
    VERSUS = 0
    SUPERHEROES = 1
    LOVEMETER = 2
    WANTED = 3


class Game:
    def __init__(self, faces):
        self._game_id = uuid.uuid4()
        self.overlay = None
        self.background_color = None
        self.faces = faces
        self.player_count = 2
        self.offsets = []
        self.extra_background = None

    def gen_overlay(self):
        """
        Just for auto-completion purposes
        """
        try:
            self._random_images()
        except ValueError:
            raise FRICP.Request.HANDLING_NOT_ENOUGH_FACES_ERROR

        return ov.generate_overlay(self)

    def _random_images(self):
        """
        This will shuffle the faces array
        """

        if len(self.faces) == 0:
            raise ValueError("No faces found")

        random.shuffle(self.faces)


def game_by_type(game_type, faces) -> Game:
    """
    This returns the [Game] object associated with the [game_type]

    Args:
        game_type: a [Games] type which represents the game type
        faces: the collected faces

    Returns:
         the corresponding [Game] object
    """
    type_str = str(game_type).split(".")[1]
    game_config = config[type_str]

    game = Game(faces=faces)
    game.overlay = game_config.get("overlay")
    game.offsets = game_config.get("offsets")
    game.player_count = game_config.get("player_count")
    game.background_color = game_config.get("background_color")
    game.extra_background = game_config.get("extra_background")

    return game