
import pickle

import cv2

# import os
# os.chdir("/mnt/project/")

# from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces
# from src.processing.overlay import generate_overlay
from src.processing.spel import *
from src.processing.overlay import transparent_overlay

if __name__ == "__main__":

    # data = collect_photos()
    # with open('real_2_personen_new.pkl', 'wb') as output:
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    overlay_fresh = cv2.imread('assets/overlays/lovemeter.tif', -1) # -1 for: cv2.IMREAD_UNCHANGED, Loads image as such including alpha channel
    overlay = cv2.cvtColor(overlay_fresh, cv2.COLOR_BGR2BGRA)
    base = cv2.cvtColor(cv2.imread('assets/overlays/superheroes_solid.png'), cv2.COLOR_BGR2BGRA)

    w, h, c = overlay_fresh.shape

    for i in range(0, w - 1):
        for j in range(0, h):

            if overlay[i, j][3] != 0:
                base[i, j] = overlay[i, j]

    cv2.imshow('output', base)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # with open('real_2_personen_new.pkl', 'rb') as input:
    #     data = pickle.load(input)
    #
    #     photos_with_angels, range_sensor = data.get()
    #
    #     faces = get_faces(data)
    #
    #
    #     print("======END======")
    #     print("Number of faces found:", len(faces))
    #
    #     games = []
    #
    #     games.append(game_by_type(Games.LOVEMETER, faces).gen_overlay())
    #
    #
    #
    #
    #     # for face in faces:
    #     #     cv2.imshow("output", face.image)
    #     #     cv2.waitKey()
    #
    #     for game in games:
    #         cv2.imshow("output", game)
    #         cv2.waitKey()
