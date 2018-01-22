from src.hardware.camera import Camera as hw_camera
from src.hardware import servo as hw_servo, range_sensor as hw_range_sensor
from src.common.log import *
from src.hardware.collect_photos_hardware import collect_photos
from src.thread.fricp import FRICP

# TODO: dit moet eigenlijk een class zijn.
camera = None
DEBUG = False


def init() -> int:
    global camera
    camera = hw_camera()

    if camera is None:
        log.error("Unable to open camera!")
        return 1
    else:
        return 0


def delete() -> int:
    global camera

    if camera is not None:
        camera.close()
        return 0
    else:
        log.warning("Camera not open when closing!")
        return 1


def handle(fricp: FRICP) -> object:
    """
    Een functie om data op te vragen van de hardware handeler.
    Kan een FRICP.ValidationError exception throwen

    Args:
        fricp(FRICP): het object wat gehandled moet worden

    Returns:
        object: data van het gevraagde object

    """
    try:
        if fricp.request == FRICP.Request.HARDWARE_GET_CAMERA:
            data = camera.get_frame()

        if fricp.request == FRICP.Request.HARDWARE_SET_SERVO_POSITION:
            if DEBUG:
                log.debug(fricp.data)

            position, sleep = fricp.data
            data = hw_servo.goto_position(position, sleep)

        if fricp.request == FRICP.Request.HARDWARE_GET_SERVO_POSITION:
            data = hw_servo.get_position()

        if fricp.request == FRICP.Request.HARDWARE_GET_RANGE_SENSOR_DISTANCE:
            data = hw_range_sensor.get_distance()

        if fricp.request == FRICP.Request.HARDWARE_COLLECT_PHOTOS:
            data = collect_photos()
    except Exception as error:
        log.error("Error while handeling request: %s", error)
        raise FRICP.ValidationError(FRICP.Response.UNKNOWN_HANDLING_ERROR, fricp)
    return data
