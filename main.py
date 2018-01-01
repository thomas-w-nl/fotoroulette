import os
import pickle

import cv2

os.chdir("/mnt/project/")

from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces

if __name__ == "__main__":

    # data = collect_photos()
    # with open('real_2_personen_new.pkl', 'wb') as output:
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    with open('real_2_personen_new.pkl', 'rb') as input:
        data = pickle.load(input)

        photos_with_angels, range_sensor = data.get()

        faces = get_faces(data)

        print("======END======")
        print("Number of faces found:", len(faces))

        for face in faces:
            cv2.imshow("output", face.image)
            cv2.waitKey()
