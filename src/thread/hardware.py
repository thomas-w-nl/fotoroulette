from src.thread.fricp import FRICP


# TODO code testen


# client code
# TODO: owner is nu altijd PROCESSING terwijl GUI het ook zou kunnen aanroepen
class Servo:

    # TODO: het zou helemaal mooi zijn als dit een getter en setter was.
    @staticmethod
    def set_position(graden: int, sleep:float=0.4) -> FRICP.Response:
        """
        verstuurd `HARDWARE_SET_SERVO_POSITION` naar de Hardware FRICP server.
        Draai de servo naar `graden`.
        kan een FRICP.ValidationError exception throwen
        Args:
            graden(int): naar welke graad moet hij draaien

        Returns:
            FRICP.Response: response van de server
        """
        data = [graden, sleep]
        servo = FRICP(FRICP.Request.HARDWARE_SET_SERVO_POSITION,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST,
                      data)
        response = servo.send()
        return response.response

    @staticmethod
    def get_position() -> int:
        """
        verstuurd `HARDWARE_GET_SERVO_POSITION` naar de Hardware FRICP server.
        krijg de servo positie van de hardware server.
        kan een FRICP.ValidationError exception throwen
        Returns:
            int: servo positie
        """
        distance = FRICP(FRICP.Request.HARDWARE_GET_SERVO_POSITION,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        response = distance.send()
        return response.data


class Camera:
    @staticmethod
    def get_frame() -> object:
        # TODO: thomas moet checken of het wel het return type goed is
        """
        verstuurd `HARDWARE_GET_CAMERA` naar de Hardware FRICP server.
        maakt een foto met de camera en returnt deze.
        kan een FRICP.ValidationError exception throwen
        Returns:
            ARGB_Numpady_Arrays: foto gemaakt met de server
        """
        photo = FRICP(FRICP.Request.HARDWARE_GET_CAMERA,
                      FRICP.Owner.PROCESSING,
                      FRICP.Owner.HARDWARE,
                      FRICP.Response.REQUEST)
        response = photo.send()
        return response.data


class RangeSensor:
    @staticmethod
    def get_distance() -> int:
        """
        verstuurd `HARDWARE_GET_RANGE_SENSOR_DISTANCE` naar de Hardware FRICP server.
        krijg de afstand van de range sensor
        kan een FRICP.ValidationError exception throwen
        Returns:
            int: gemete afstand
        """
        distance = FRICP(FRICP.Request.HARDWARE_GET_RANGE_SENSOR_DISTANCE,
                         FRICP.Owner.PROCESSING,
                         FRICP.Owner.HARDWARE,
                         FRICP.Response.REQUEST)
        response = distance.send()
        return response.data
