import numpy as np
import cv2
import time
import serial

def gen_photo(camera):
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, 0)
        yield frame


def save_photo(photo_name, frame):
    print("Saving file: %s" % photo_name)
    cv2.imwrite(photo_name, frame)

if __name__ == "__main__":
    cam = cv2.VideoCapture(-1)
    photo_gen = gen_photo(cam)
    device = serial.Serial('/dev/ttyACM3', 9600, timeout=0)

    while True:
        message = device.readline().decode("utf-8")
        photo = next(photo_gen)
        # photo = add_median(photo)
        cv2.imshow('image', photo)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if message != "":
            save_photo(str(time.clock_gettime(0)) + '.png', photo)

    cam.release()
    cv2.destroyAllWindows()
