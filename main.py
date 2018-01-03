
import pickle

import cv2

# import os
# os.chdir("/mnt/project/")

# from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces
from src.processing.overlay import generate_overlay
from src.processing.spel import *

if __name__ == "__main__":

    # data = collect_photos()
    # with open('real_2_personen_new.pkl', 'wb') as output:
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    with open('real_2_personen_new.pkl', 'rb') as input:
        data = pickle.load(input)

        photos_with_angels, range_sensor = data.get()

        faces = get_faces(data)

        list_of_face_images = []
        for face in faces:
            list_of_face_images.append(face)


        print("======END======")
        print("Number of faces found:", len(faces))

        game = Wanted(list_of_face_images).gen_overlay()




        for face in faces:
            cv2.imshow("output", face.image)
            cv2.waitKey()

        cv2.imshow("output", game)
        cv2.waitKey()
