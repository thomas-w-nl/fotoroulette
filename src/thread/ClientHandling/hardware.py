from src.thread.fricp import FRICP

class servo:
    @staticmethod
    def goto_position(graden: int):
        servo = FRICP(FRICP.Request.HARDWARE_POST_SERVO_POSITION,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST,
                      next_pic_angle)
        servo.send()

        return servo.data

    @staticmethod
    def get_position():
        distance = FRICP(FRICP.Request.HARDWARE_GET_SERVO_POSITION,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        distance.send()

        return distance.data

class Camera:
    @staticmethod
    def get_frame():
        photo = FRICP(FRICP.Request.HARDWARE_GET_CAMERA,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST)
        photo.send()
        return photo.data

class range_sensor:
    @staticmethod
    def get_distance():
        distance = FRICP(FRICP.Request.HARDWARE_GET_RANGE_SENSOR,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        distance.send()

        return distance.data
