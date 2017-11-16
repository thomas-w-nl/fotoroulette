import numpy as np

# todo moet ook image path en face image offsets bevatten voor elke game type
class GameType:
    VERSUS = 0
    SUPERHEROES = 1
    ROULETTE = 2
    LOVEMETER = 3


def apply_overlay(frame: np.array, overlay: GameType) -> np.array:
    pass
