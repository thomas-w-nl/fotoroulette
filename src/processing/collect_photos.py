import configparser
import cv2

from src.thread.hardware import RangeSensor, Servo
from src.processing.photo_data import PhotoData

DEBUG = False
FAKE = False


def collect_photos() -> PhotoData:
    """
    Maakt de fotos en meet de afstand om een bepaald aantal graden
    :return: Alle fotos met range sensor data
    """
    data = PhotoData()

    config = configparser.ConfigParser()
    config.read('fotoroulette.conf')

    start_angle = config['Servo'].getint('MIN_SERVO_POS')
    stop_angle = config['Servo'].getint('MAX_SERVO_POS')

    # de step size voor de volgende meeting
    RANGE_SENSOR_STEP_SIZE = config['RangeSensor'].getint('SENSOR_FOV')
    CAMERA_STEP_SIZE = config['General'].getint('CAMERA_STEP_SIZE')

    if FAKE:
        import os
        cam = iter(os.listdir("/home/pi/Documents/python/raspberry-pi/img/"))

    current_pos = start_angle
    next_pic_angle = current_pos
    next_range_angle = current_pos

    Servo.goto_position(current_pos)

    # while we can still collect images or sensor data
    while next_range_angle <= stop_angle or next_pic_angle <= stop_angle:

        # move for picture
        if next_pic_angle <= next_range_angle:

            if DEBUG:
                print("pic at ", next_pic_angle)

            Servo.goto_position(next_pic_angle)
            current_pos = next_pic_angle

            photo = Camera.get_frame()

            if FAKE:
                photo = cv2.imread(next(Camera))

            data.append_photo(photo, current_pos)
            next_pic_angle += CAMERA_STEP_SIZE

        # move for range
        if next_range_angle <= next_pic_angle:

            if DEBUG:
                print("range at ", next_range_angle)

            Servo.goto_position(next_range_angle)
            current_pos = next_range_angle

            next_range_angle += RANGE_SENSOR_STEP_SIZE

            distance = RangeSensor.get_distance()
            data.append_distance(distance, current_pos)

    Servo.goto_position(start_angle, 1)
    return data
