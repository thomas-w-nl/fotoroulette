from src.hardware import range_sensor, servo
from src.hardware.camera import Camera
from src.processing import photo_data
from src.processing.photo_data import PhotoData

START_ANGLE = 0
STOP_ANGLE = 180

# de step size voor de volgende meeting
RANGE_SENSOR_MEASURE_OFFSET = range_sensor.SENSOR_ANGLE


def collect_photos() -> photo_data:
    # todo do not move based on current position, move to planed position and decide which planned position is first
    data = PhotoData(RANGE_SENSOR_MEASURE_OFFSET)
    cam = Camera()

    photo = cam.take_picture()
    distance = range_sensor.get_distance()

    cur_pos = START_ANGLE

    data.set_photo(photo, cur_pos)
    data.set_sensor_data(distance)

    move_to_next_pic_angle = cur_pos + int(Camera.CAMERA_H_ANGLE / 2)
    move_to_next_range_angle = cur_pos + RANGE_SENSOR_MEASURE_OFFSET

    # while we can still collect images or sensor data
    while move_to_next_range_angle < STOP_ANGLE or move_to_next_pic_angle < STOP_ANGLE:

        # move for picture
        if move_to_next_pic_angle < move_to_next_range_angle:
            servo.goto_position(move_to_next_pic_angle)
            cur_pos = move_to_next_pic_angle
            move_to_next_pic_angle = cur_pos + int(Camera.CAMERA_H_ANGLE / 2)

            photo = cam.take_picture()
            data.set_photo(photo, cur_pos)

        # move for range
        elif move_to_next_range_angle < move_to_next_pic_angle:
            servo.goto_position(move_to_next_range_angle)
            cur_pos = move_to_next_range_angle
            move_to_next_range_angle = cur_pos + RANGE_SENSOR_MEASURE_OFFSET

            distance = range_sensor.get_distance()
            data.set_sensor_data(distance)

        else:
            raise EnvironmentError("Critical: Cannot move to picture or range angle")

    return data


collect_photos()
