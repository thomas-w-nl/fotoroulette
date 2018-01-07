from src.thread.fricp import FRICP
from src.hardware.camera import Camera
from src.hardware import servo, range_sensor

class HardwareHandling:

    @staticmethod
    def handle(fricp: FRICP):
        if fricp.request == FRICP.Request.HARDWARE_GET_CAMERA:
            camera = Camera()
            data = camera.get_frame()

        if fricp.request == FRICP.Request.HARDWARE_POST_SERVO_POSITION:
            data = servo.goto_position(fricp.data)

        if fricp.request == FRICP.Request.HARDWARE_GET_SERVO_POSITION:
            data = servo.get_position()

        if fricp.request == FRICP.Request.HARDWARE_GET_RANGE_SENSOR:
            data = range_sensor.get_distance()

        return data