
import pickle

import cv2

from PIL import Image
# import os
# os.chdir("/mnt/project/")

from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces
# from src.processing.overlay import generate_overlay
from src.processing.spel import *


    #
    # with open('real_2_personen_new.pkl', 'wb') as output:
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    # with open('real_2_personen_new.pkl', 'rb') as input:
    #     data = pickle.load(input)

    data = collect_photos()

    photos_with_angels, range_sensor = data.get()

    faces = get_faces(data)

    print("======END======")
    print("Number of faces found:", len(faces))

    games = []

    games.append(game_by_type(Games.VERSUS, faces).gen_overlay())

    # for face in faces:
    #     cv2.imshow("output", face.image)
    #     cv2.waitKey()

    for game in games:
        cv2.imshow("output", game)
        cv2.imwrite("game.jpg", game)
        cv2.waitKey()
