from src.hardware import range_sensor, servo, camera
from src.hardware.camera import Camera
from src.processing import photo_data
from src.processing.photo_data import PhotoData
from src.thread.fricp import FRICP

START_ANGLE = 0
STOP_ANGLE = 180  # todo should be 180
TOTAL_ANGLE = STOP_ANGLE - START_ANGLE

# de step size voor de volgende meeting
RANGE_SENSOR_STEP_SIZE = range_sensor.SENSOR_ANGLE
CAMERA_STEP_SIZE = int(camera.CAMERA_H_FOV / 2)


def collect_photos() -> photo_data:
    """
    Maakt de fotos en meet de afstand om een bepaald aantal graden

    Return:
      Alle fotos met range sensor data
    """
    data = PhotoData(RANGE_SENSOR_STEP_SIZE)
    # cam = Camera()

    cam_step = 0
    range_step = 0

    next_pic_angle = 0
    next_range_angle = 0

    current_pos = START_ANGLE

    # while we can still collect images or sensor data
    while next_range_angle <= STOP_ANGLE or next_pic_angle <= STOP_ANGLE:

        # move for picture
        if next_pic_angle <= next_range_angle:
            servo = FRICP(FRICP.Request.HARDWARE_POST_SERVO_POSITION,
                          FRICP.Owner.PROCESSING,
                          FRICP.Owner.HARDWARE,
                          FRICP.Response.REQUEST,
                          next_pic_angle)
            servo.send()
            # servo.goto_position(next_pic_angle)
            current_pos = next_pic_angle

            cam_step += 1

            photo = FRICP(FRICP.Request.HARDWARE_GET_CAMERA,
                          FRICP.Owner.PROCESSING,
                          FRICP.Owner.HARDWARE,
                          FRICP.Response.REQUEST)
            photo.send()
            # photo = cam.get_dummy_frame()
            data.set_photo(photo, current_pos)

        # move for range
        if next_range_angle <= next_pic_angle:
            servo = FRICP(FRICP.Request.HARDWARE_POST_SERVO_POSITION,
                          FRICP.Owner.PROCESSING,
                          FRICP.Owner.HARDWARE,
                          FRICP.Response.REQUEST,
                          next_range_angle)
            servo.send()

            range_step += 1
            distance = FRICP(FRICP.Request.HARDWARE_GET_SERVO_POSITION,
                             FRICP.Owner.PROCESSING,
                             FRICP.Owner.HARDWARE,
                             FRICP.Response.REQUEST)
            distance.send()
            # distance = range_sensor.get_distance()
            data.set_sensor_data(distance.data)

        next_pic_angle = CAMERA_STEP_SIZE * cam_step
        next_range_angle = RANGE_SENSOR_STEP_SIZE * range_step

    return data
