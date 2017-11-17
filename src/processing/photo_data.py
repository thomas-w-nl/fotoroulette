import random
import cv2
from bisect import bisect_left

# voor alle waarden die binnen de helft van de sensor angle liggen is de data valid
SENSOR_ANGLE_HALF = 15 / 2
# y = -1/((130^2)*1.3)(x - 130)^2 + 0.8
SWEETSPOT = 130  # cm
SWEETSPOT_WIDTH_FACTOR = 1.3
MAX_CONFIDENCE = 0.8


class PhotoData:
    def __init__(self):
        self._photo = []
        self._photo_angle = []
        self._sensor_data = []
        self._sensor_data_angle = []
        self._sorted = True

    def get_sensor_data(self, graden: int) -> int:
        """
        Geeft de confidence score voor de sensor data bij een meegegeven aantal graden
        :param graden: het aantal graden
        :return confidence_score: de zekerheid of er iemand voor staat
        """

        closes_data = self._get_closest(graden)

        if 0 > closes_data > SENSOR_ANGLE_HALF:
            return -1

        afstand = self._sensor_data[closes_data]

        a = -1 / ((SWEETSPOT ** 2) * SWEETSPOT_WIDTH_FACTOR)
        haakjes = (afstand - SWEETSPOT) ** 2

        confidence = round(a * haakjes + MAX_CONFIDENCE, 2)
        confidence = max(confidence, 0)

        # todo dummy data
        # return confidence

        return random.random()

    def _get_closest(self, number):

        out = -1

        if self._sorted:
            """
            Assumes myList is sorted. Returns closest value to myNumber.

            If two numbers are equally close, return the smallest number.
            """
            pos = bisect_left(self._sensor_data_angle, number)
            if pos == 0:
                return self._sensor_data_angle[0]
            if pos == len(self._sensor_data_angle):
                return -1
            before = self._sensor_data_angle[pos - 1]
            after = self._sensor_data_angle[pos]
            if after - number < number - before:
                return after
            else:
                return before

        elif not self._sorted:
            out = min(self._sensor_data_angle, key=lambda x: abs(x - number))

        return out

    def get_photo(self, i):
        # return {self._photo[i], self._photo_angle[i]}

        # todo dummy data, remove import cv2
        dummy_photo = cv2.imread('img/faces.jpg')
        dummy_angle = random.randint(0, 180)
        return {dummy_photo, dummy_angle}

    def set_photo(self, photo, photo_angle):
        self._photo.append(photo)
        self._photo_angle.append(photo_angle)
