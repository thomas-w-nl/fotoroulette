import random
from typing import List, Tuple

import cv2
import numpy as np

# y = -1/((130^2)*1.3)(x - 130)^2 + 1
from src.hardware import range_sensor

# todo get from config
SWEETSPOT = 130  # cm
SWEETSPOT_WIDTH_FACTOR = 1.3
MAX_CONFIDENCE = 1


class PhotoData:
    def __init__(self):
        self.rs = RangeSensor()
        self.p = Photo()

    def append_photo(self, photo: np.array, photo_angle: float):
        self.p.append(photo, photo_angle)

    def append_distance(self, distance: float, distance_angle: float):
        self.rs.append(distance, distance_angle)

    def __iter__(self) -> Tuple[Photo, RangeSensor]:
        yield self.p, self.rs


class RangeSensor:
    def __init__(self):
        self._distance = []
        self._distance_angle = []

    def append(self, distance: float, distance_angle: float):
        self._distance.append(distance)
        self._distance_angle.append(distance_angle)

    def get_confidence(self, angle: float) -> float:
        """
        Geeft de confidence score voor de sensor data bij een aantal graden ten opzichte van het startpunt van de camera

        Args:
           angle: De hoek ten opzichte van het startpunt van de camera

        Returns:
           De zekerheid of er iemand voor staat in floats
        """

        distance = self._angle_to_distance(angle)

        confidence = self._calculate_confidence(distance)

        # het minimum is 0
        confidence = max(confidence, 0)

        return confidence

    def _calculate_confidence(self, distance: float, sweetspot: float = SWEETSPOT,
                              width_factor: float = SWEETSPOT_WIDTH_FACTOR,
                              max_confidence: float = MAX_CONFIDENCE) -> float:
        """
        Bereken een parabool voor de confidence score.

        Args:
           distance: De gemeten afstand
           sweetspot: De positie waarop de confidence maximaal is
           width_factor: De factor waarmee de breedte van de sweetspot vergroot wordt
           max_confidence : De maximum confidence van de range sensor

        """

        return -1 / (sweetspot ** 2 * width_factor) * (distance - sweetspot) ** 2 + max_confidence

    def _angle_to_distance(self, angle: float) -> float:

        """
        Returnt de gemeten afstand voor een bepaalde hoek. Returnt -1 als die niet beschikbaar is.

        Args:
            angle: De hoek waar de data wordt opgevraagd

        Returns:
            De afstand als float of -1 als die niet beschikbaar is
        """

        RANGE_SENSOR_FOV_HALF = range_sensor.SENSOR_FOV / 2

        # als deze buiten berijk is return error
        if angle < (self._distance_angle[0] - RANGE_SENSOR_FOV_HALF):
            return -1

        for index, range_angle in enumerate(self._distance_angle):

            if angle < range_angle:

                # kies de dichtsbijzijnde meting
                if self._distance_angle[index] - angle < self._distance_angle[index - 1] - angle:
                    return self._distance[index]
                else:
                    return self._distance[index - 1]

        # als de angle nog binnen de laatste meting valt

        last_element = self._distance_angle[len(self._distance_angle) - 1]

        if angle < (last_element + RANGE_SENSOR_FOV_HALF):
            return self._distance[len(self._distance_angle) - 1]

        return -1


class Photo:
    def __init__(self):
        self._photo = []
        self._photo_angle = []

    def append(self, photo: np.array, photo_angle: float):
        self._photo.append(photo)
        self._photo_angle.append(photo_angle)

    def __iter__(self) -> Tuple[np.array, float]:
        yield self._photo, self._photo_angle
