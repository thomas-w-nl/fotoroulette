import configparser
from typing import Callable

from src.common.log import log
from src.hardware import servo, range_sensor
from src.hardware.camera import Camera
from src.processing.photo_data import PhotoData


class SensorFactory:
    def __init__(self, current_pos: float, stop_angle: float, step_size: float,
                 data_store_func: Callable,
                 sensor_perform_func: Callable
                 ) -> None:

        self.stop_angle = stop_angle
        self.next_angle = current_pos
        self.step_size = step_size
        self.sensor_perform_func = sensor_perform_func
        self.data_store_func = data_store_func

    def next_action(self, other: 'SensorFactory') -> bool:

        """
        Move the servo to the next position and perform the sensor action. It compares its own next action position
        with the other Sensor to determine which is closest.
        Args:
            other (SensorFactory): The object to 'compete' with for closest perform angle.

        Returns:
            bool: True if still able to perform its action at next angle.

        """
        # only return false if stop_angle has been reached
        if self.next_angle > self.stop_angle:
            return False

        # move to perform at next angle if closer than other
        if self.next_angle <= other.next_angle:
            servo.goto_position(self.next_angle)
            current_pos = self.next_angle

            self.next_angle += self.step_size

            self.data_store_func(self.sensor_perform_func(), current_pos)

        return True


def collect_photos() -> PhotoData:
    """
        Maakt de fotos en meet de afstand om een bepaald aantal graden
        :return: Alle fotos met range sensor data
    """
    data = PhotoData()
    log.info("Using collect photos directly on hardware")

    config = configparser.ConfigParser()
    config.read('settings.conf')

    start_angle = config['Servo'].getint('MIN_SERVO_POS')
    stop_angle = config['Servo'].getint('MAX_SERVO_POS')

    # de step size voor de volgende meeting
    rs_step_size = config['RangeSensor'].getint('SENSOR_FOV')
    c_step_size = config['General'].getint('CAMERA_STEP_SIZE')

    camera = Camera()

    current_pos = start_angle

    servo.goto_position(current_pos, 1)

    rs = SensorFactory(start_angle, stop_angle, rs_step_size, data_store_func=data.append_distance,
                       sensor_perform_func=range_sensor.get_distance)
    c = SensorFactory(start_angle, stop_angle, c_step_size, data_store_func=data.append_photo,
                      sensor_perform_func=camera.get_frame)

    # while we can still collect camera photos or range_sensor data
    c_has_next = rs_has_next = True
    while c_has_next or rs_has_next:
        c_has_next = c.next_action(rs)
        rs_has_next = rs.next_action(c)

    servo.goto_position(current_pos, 1)
    return data
