from src.thread.fricp import FRICP
from src.hardware.camera import Camera as hw_camera
from src.hardware import servo as hw_servo, range_sensor as hw_range_sensor
from src.common.log import *


# TODO: documentatie
# TODO: RP libary errors fixen
# TODO code testen

def handle(fricp: FRICP):
    try:
        if fricp.request == FRICP.Request.HARDWARE_GET_CAMERA:
            camera = hw_camera()
            data = camera.get_frame()

        if fricp.request == FRICP.Request.HARDWARE_SET_SERVO_POSITION:
            data = hw_servo.goto_position(fricp.data)

        if fricp.request == FRICP.Request.HARDWARE_GET_SERVO_POSITION:
            data = hw_servo.get_position()

        if fricp.request == FRICP.Request.HARDWARE_GET_RANGE_SENSOR_DISTANCE:
            data = hw_range_sensor.get_distance()
    except Exception as error:
        log.error("Error while handeling request: %s", error)
        raise FRICP.ValidationError(FRICP.Response.UNKNOWN_HANDLING_ERROR, fricp)
    return data


# client code

class Servo:
    @staticmethod
    def goto_position(graden: int):
        servo = FRICP(FRICP.Request.HARDWARE_SET_SERVO_POSITION,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST,
                      graden)
        return servo.send()

    @staticmethod
    def get_position():
        distance = FRICP(FRICP.Request.HARDWARE_GET_SERVO_POSITION,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        return distance.send()


class Camera:
    @staticmethod
    def get_frame():
        photo = FRICP(FRICP.Request.HARDWARE_GET_CAMERA,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST)
        return photo.send()


class RangeSensor:
    @staticmethod
    def get_distance():
        distance = FRICP(FRICP.Request.HARDWARE_GET_RANGE_SENSOR_DISTANCE,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        return distance.send()
