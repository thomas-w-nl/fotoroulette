import random
from typing import List, Tuple

import cv2
import numpy as np

# y = -1/((130^2)*1.3)(x - 130)^2 + 1
from hardware import range_sensor

SWEETSPOT = 130  # cm
SWEETSPOT_WIDTH_FACTOR = 1.3
MAX_CONFIDENCE = 1


class PhotoData:
    def __init__(self, sensor_data_step_size: float):
        """
        Photo data houd de fotos met sensor data en hoek ten opzichte van de start bij

        Args:
           sensor_data_step_size: De groote van de stap in graden
        """
        # TODO: 1 lijst met een tuple
        self._photos = []
        self._photo_angle = []
        self._sensor_data = []
        self._sensor_data_step_size = sensor_data_step_size

    def __iter__(self):
        for photo, photo_angle in zip(self._photos, self._photo_angle):
            yield (photo, photo_angle)

    # TODO: Beter documenteren
    def get_sensor_confidence(self, graden: float) -> float:
        """
        Geeft de confidence score voor de sensor data bij een aantal graden ten opzichte van het startpunt van de camera

        Args:
           graden: De hoek ten opzichte van het startpunt van de camera

        Returns:
           De zekerheid of er iemand voor staat in floats
        """

        afstand = self._angle_to_data(graden)

        # dit  is een parabool, boven staat de formule die in google gevisualiseerd kan worden
        a = -1 / ((SWEETSPOT ** 2) * SWEETSPOT_WIDTH_FACTOR)
        haakjes = (afstand - SWEETSPOT) ** 2

        confidence = round(a * haakjes + MAX_CONFIDENCE, 2)
        confidence = max(confidence, 0)

        return confidence

    def _angle_to_data(self, angle: float) -> float:

        """
        Returnt de sensor data voor een bepaalde hoek. Returnt -1 als die niet beschikbaar is.

        Args:
            angle: De hoek waar de data wordt opgevraagd

        Returns:
            De afstand als int of -1 als die niet beschikbaar is
        """
        # het aantal stappen genomen om bij de juiste meting uit te komen
        steps = int(round(angle / self._sensor_data_step_size, 0))

        # als deze buiten berijk is return error
        if steps < 0 or steps > (len(self._sensor_data) - 1):
            return -1

        data = self._sensor_data[steps]
        return data

    def get_photo(self, i: int) -> list:
        """
        Vraag een foto op.

        Args:
           i: De index van de foto

        Returns:
           De foto met de hoek ten opzichte van de startpunt van de camera
        """
        # TODO: Tuple
        return [self._photo[i], self._photo_angle[i]]


    def set_photo(self, photo: np.array, photo_angle: float):
        """
        Zet een foto

        Args:
           photo: De foto
           photo_angle: De hoek ten opzichte van de startpunt van de camera waarop de foto
        """
        self._photos.append(photo)
        self._photo_angle.append(photo_angle)

    # TODO: Hernoem naar gemeten afstand
    def set_sensor_data(self, sensor_data: int):
        """
        Zet sensor data, de hoek tussen de metingen wordt in de constructor aangegeven

        Args:
           sensor_data: De gemeten afstand
        """
        self._sensor_data.append(sensor_data)
