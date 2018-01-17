import pickle

import cv2

from PIL import Image
# import os
# os.chdir("/mnt/project/")

from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces
# from src.processing.overlay import generate_overlay
from src.processing.spel import *

if __name__ == "__main__":
    print("====== THIS FILE IS DEPRECATED ======")
    print("Please use the proper files to start fotoroulette")

    with open('real_2_personen_new.pkl', 'rb') as pickleinput:

        data = pickle.load(pickleinput)

        photos_with_angels, range_sensor = data.get()

        game_type = Games.VERSUS

        faces = get_faces(data, game_type)

        games = [game_by_type(game_type, faces).gen_overlay()]

        for game in games:
            game.show()
