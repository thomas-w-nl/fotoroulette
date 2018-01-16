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
    # data = collect_photos()
    # with open('real_2_personen_new.pkl', 'wb') as output:
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    fakedata = open('real_2_personen_new.pkl', 'rb')
    data = pickle.load(fakedata)

    photos_with_angels, range_sensor = data.get()

    faces = get_faces(data)

    games = []

    games.append(game_by_type(Games.VERSUS, faces).gen_overlay())

    # for face in faces:
    #     cv2.imshow("output", face.image)
    #     cv2.waitKey()

    for game in games:
        cv2.imshow("output", game)
        cv2.imwrite("game.jpg", game)
        cv2.waitKey()
