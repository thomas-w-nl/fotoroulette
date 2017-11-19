import random
import cv2
from bisect import bisect_left


# y = -1/((130^2)*1.3)(x - 130)^2 + 1
from src.hardware import range_sensor

SWEETSPOT = 130  # cm
SWEETSPOT_WIDTH_FACTOR = 1.3
MAX_CONFIDENCE = 1


class PhotoData:
    def __init__(self, sensor_data_step_size):
        self._photos = []
        self._photo_angle = []
        self._sensor_data = []
        self._sensor_data_step_size = sensor_data_step_size

    def __iter__(self):
        for photo, photo_angle in zip(self._photos, self._photo_angle):
            yield (photo, photo_angle)

    def get_sensor_confidence(self, graden: int) -> int:
        """
        Geeft de confidence score voor de sensor data bij een meegegeven aantal graden
        :param graden: de hoek waar de data wordt opgevraagd
        :return confidence_score: de zekerheid of er iemand voor staat
        """

        afstand = self._angle_to_data(graden)

        a = -1 / ((SWEETSPOT ** 2) * SWEETSPOT_WIDTH_FACTOR)
        haakjes = (afstand - SWEETSPOT) ** 2

        confidence = round(a * haakjes + MAX_CONFIDENCE, 2)
        confidence = max(confidence, 0)

        # todo dummy data
        # return confidence

        return random.uniform(0.35, 0.9)

    def _angle_to_data(self, angle: int) -> int:

        """
        Return de sensor data voor een bepaalde hoek
        :param angle: de hoek waar de data wordt opgevraagd
        :return: de afstand
        """
        # het aantal stappen genomen om bij de juiste meting uit te komen
        steps = int(round(angle / self._sensor_data_step_size, 0))

        if steps < 0 or steps > (len(self._sensor_data) - 1):
            return 0

        data = self._sensor_data[steps]
        return data

    def get_photo(self, i):
        # return (self._photo[i], self._photo_angle[i])

        # todo dummy data
        dummy_photo = cv2.imread('img/faces.jpg')
        dummy_angle = random.randint(0, 180)
        return (dummy_photo, dummy_angle)

    def set_photo(self, photo, photo_angle):
        self._photos.append(photo)
        self._photo_angle.append(photo_angle)

    def set_sensor_data(self, sensor_data):
        self._sensor_data.append(sensor_data)
