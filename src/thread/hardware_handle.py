from src.hardware.camera import Camera as hw_camera
from src.hardware import servo as hw_servo, range_sensor as hw_range_sensor
from src.common.log import *


def handle(fricp: FRICP) -> object:
    """
    functie om data op te vragen van de hardware handeler.
    kan een FRICP.ValidationError exception throwen
    Args:
        fricp(FRICP): het object wat gehandled moet worden

    Returns:
        object: data van het gevraagte object

    """
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
