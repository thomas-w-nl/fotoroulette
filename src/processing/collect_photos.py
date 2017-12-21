import cv2
from src.hardware import range_sensor, servo, camera
from src.hardware.camera import Camera
from src.processing import photo_data
from src.processing.photo_data import PhotoData

START_ANGLE = 5
STOP_ANGLE = 175
TOTAL_ANGLE = STOP_ANGLE - START_ANGLE

# de step size voor de volgende meeting
RANGE_SENSOR_STEP_SIZE = range_sensor.SENSOR_FOV
CAMERA_STEP_SIZE = int(camera.CAMERA_H_FOV / 2)


def collect_photos() -> photo_data:
    """
    Maakt de fotos en meet de afstand om een bepaald aantal graden

    Return:
      Alle fotos met range sensor data
    """
    data = PhotoData()
    cam = Camera()

    current_pos = START_ANGLE
    next_pic_angle = current_pos
    next_range_angle = current_pos

    servo.goto_position(current_pos)

    # while we can still collect images or sensor data
    while next_range_angle <= STOP_ANGLE or next_pic_angle <= STOP_ANGLE:

        # move for picture
        if next_pic_angle <= next_range_angle:

            servo.goto_position(next_pic_angle)
            current_pos = next_pic_angle

            photo = cam.get_frame()
            data.append_photo(photo, current_pos)
            # cv2.imwrite('photo_' + str(next_pic_angle / 10) + '.png', photo)
            next_pic_angle += CAMERA_STEP_SIZE

        # move for range
        if next_range_angle <= next_pic_angle:
            servo.goto_position(next_range_angle)
            current_pos = next_range_angle

            distance = range_sensor.get_distance()
            data.append_distance(distance, current_pos)
            # print("distance " + str(distance) + " on step " + str(next_range_angle / 10))
            next_range_angle += RANGE_SENSOR_STEP_SIZE

    servo.goto_position(START_ANGLE)
    return data


if __name__ == "__main__":
    collect_photos()
