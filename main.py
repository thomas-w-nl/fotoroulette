# from common import tools, log ?
import os

import pickle

os.chdir("/mnt/project/")

from src.common.log import *
from src.hardware.camera import Camera
from src.processing.collect_photos import collect_photos
from src.processing.get_faces import get_faces

import src.common.tools as tools
import cv2

if __name__ == "__main__":

    # data = collect_photos()
    # with open('real_data_2_personen.pkl', 'wb') as output:
    #
    #
    #     pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    with open('real_data_2_personen.pkl', 'rb') as input:
        data = pickle.load(input)

        photos_with_angels, range_sensor = data.get()

        faces = get_faces(data)

        print("======END======")
        print("Number of faces found:", len(faces))

        for face in faces:
            cv2.imshow("output", face.image)
            cv2.waitKey()
