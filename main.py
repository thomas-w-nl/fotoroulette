import numpy as np
import cv2
import time

def gen_photo(camera):
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, 0)
        yield frame


def save_photo(photo_gen):
    while True:
        photo_name, frame = (yield)
        print("Saving file: %s" % photo_name)
        cv2.imwrite(photo_name, frame)


if __name__ == "__main__":
    cam = cv2.VideoCapture(-1)
    photo_gen = gen_photo(cam)
    save = save_photo(photo_gen)
    next(save)

    while True:
        photo = next(photo_gen)
        cv2.imshow('image', photo)

        k = cv2.waitKey(0)
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('s'):
            save.send(("test_file.png", photo))
