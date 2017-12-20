import cv2
import numpy as np

from common.log import *
from hardware import camera
from processing.collect_photos import collect_photos
from processing.photo_data import PhotoData, Photo
from typing import List, Tuple
from common import tools

#: De drempelwaarde voor gezichts herkenning. 0.65 is voor de huidige fotos een goede waarde.
MIN_FACE_CONFIDENCE = 0.65

#: OpenCV gezichts detectie instellingen
OPENCV_MIN_FACE_SIZE = 50
OPENCV_SCALE_FACTOR = 1.1
OPENCV_MIN_NEIGHBORS = 4

#: Het maximum verschil waarbij twee gezichten als een wordt gezien in graden
NEARBY_FACE_ANGLE_DIFF_MAX = 5

#: De waarde van opencv vs de range sensor en is een waarde van :math:`1.0 <= x <= 0.0`.
OPENCV_WEIGHT = 0.7
RANGE_SENSOR_WEIGHT = 1 - OPENCV_WEIGHT
OPENCV_MAX_FACE_CONFIDENCE = 10  # er is geen documentatie voor, het lijkt er op dat dit de max wel is


class Faces:
    def __init__(self, face_pos: List[int], angle: float, confidence: float, face_image: np.array):
        """
        Een datatype voor een gezicht

        Args:
            face_pos: positie van het gezicht (x, y, w, h)
            angle: hoek ten opzichte van het start van de camera in graden
            confidence: De zekerheid of het een gezicht is
            face_image: De uitgeknipte foto
        """
        self.face_pos = face_pos
        self.confidence = confidence
        self.angle = angle
        self.pos_in_photo = round(face_pos[0] + (face_pos[2] / 2))
        self.face_image = face_image


def get_faces(photos_with_data: PhotoData) -> List[Face]:
    """
    Returned de uniek gezichten uit meerder fotos die voldoen aan een bepaalde drempelwaarde.

    Args:
       photos_with_data: De fotos met sensor en orientatie data

    Returns:
       Een lijst met de gezichten.
    """

    all_faces = []

    for single_photo in photos_with_data:
        photo = single_photo[0]
        photo_angle = single_photo[1]
        photo_width = len(photo[0])

        cv_faces, cv_confidences = _opencv_get_faces(photo)

        for cv_face_pos, cv_confidence in zip(cv_faces, cv_confidences):
            face_angle = _location_to_angle(photo_width, photo_angle, cv_face_pos)

            total_confidence = _get_total_confidence(photos_with_data, face_angle, cv_confidence)

            if total_confidence > MIN_FACE_CONFIDENCE:
                cutout = _crop_image(photo, cv_face_pos)
                face = Face(cv_face_pos, face_angle, total_confidence, cutout)

                _append_face_if_unique_and_centered(all_faces, face, photo_width)

    return all_faces


def _append_face_if_unique_and_centered(all_faces: List[Face], cur_face: Face, photo_width: int):
    """
    Voegt een gezicht toe aan all_faces als het gezicht uniek is. Als
    het gezicht beter in beeld is dan een oud gezicht wordt deze
    vervangen

    Args:
       all_faces: list met alle gezichten
       cur_face: Het gezicht om toe te voegen
       photo_width: De breedte van de foto
    """

    added_face = False
    for other_face in all_faces:

        # if het huidige gezicht dicht bij een oud gezicht zit
        if abs(other_face.angle - cur_face.angle) < NEARBY_FACE_ANGLE_DIFF_MAX:

            # if if het huidige gezicht dichter bij het midden van de camera is, vervang het oude gezicht
            other_face_dist_to_photo_center = abs(other_face.pos_in_photo - (photo_width / 2))
            cur_face_dist_to_photo_center = (abs(cur_face.pos_in_photo - (photo_width / 2)))

            if other_face_dist_to_photo_center > cur_face_dist_to_photo_center:
                all_faces.remove(other_face)
                all_faces.append(cur_face)
                added_face = True

    if not added_face:
        all_faces.append(cur_face)


def _get_total_confidence(photos_with_data: PhotoData, current_face_angle: float, cv_confidence: float) -> float:
    """
    Voeg de opencv en range sensor confidence score samen to een confidence score

    Args:
       photos_with_data: fotos met de data
       current_face_angle: De hoek ten opzichte van het startpunt van de camera in graden
       cv_confidence: De confidence van openCV

    Returns:
       De totale confidence als float
    """
    sensor_confidence = photos_with_data.get_sensor_confidence(current_face_angle)
    opencv_confidence = cv_confidence / OPENCV_MAX_FACE_CONFIDENCE

    # if sensor data niet beschikbaar
    if sensor_confidence == -1:
        total_confidence = opencv_confidence
    else:
        total_confidence = (sensor_confidence * RANGE_SENSOR_WEIGHT) + (opencv_confidence * OPENCV_WEIGHT)

    return total_confidence


def _opencv_get_faces(photo: np.array) -> list:
    """
    Geeft alle gezichten terug die door opencv gevonden worden in de foto, met de confidence score voor elk gezicht

    Args:
       photo: De foto met gezichten

    Returns:
       Een list met de coordinaten van de gezichten en een lijst met confience scores
    """
    img_gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    # TODO Deze shizzel moet vanuit de git-root, niet twee mapjes terug. Dit is error prone!
    face_cascade = cv2.CascadeClassifier("haarCascades/haarcascade_frontalface_default.xml")

    if face_cascade is None:
        message = "Face cascade failed to load!"
        log.error(message)
        raise FileNotFoundError(message)

    # https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
    cv_faces, _ignore, cv_confidences = face_cascade.detectMultiScale3(
        img_gray,
        scaleFactor=OPENCV_SCALE_FACTOR,
        minNeighbors=OPENCV_MIN_NEIGHBORS,
        minSize=(OPENCV_MIN_FACE_SIZE, OPENCV_MIN_FACE_SIZE),
        outputRejectLevels=True
    )

    # Moet een tuple zijn
    return [cv_faces, cv_confidences]


def _crop_image(img: np.array, rect: list) -> np.array:
    """
    Knip een vierkant uit een array zoals aangegeven in rect

    Args:
       img: foto
       rect: (x,y,w,h) (?)

    Returns:
       De uitgeknipte foto.
    """
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]

    return img[y:(y + h), x:(x + w)]


def _location_to_angle(img_width: int, photo_angle: float, rect: list) -> float:
    """
    Zet een locatie op een foto gemaakt op hoek photo_angle om naar de hoek van de locatie.

    Args:
       img_width: De breedte van de foto
       photo_angle: De hoek waarop de foto is gemaakt
       rect: De locatie als (x, y, w, h)

    Returns:
       De hoek van de locatie ten opzichte van het startpunt van de camera
    """

    # scale van range(0, img_width) naar range(-camera.CAMERA_H_FOV/2, camera.CAMERA_H_FOV/2) met offset photo_angle
    center = round(rect[0] + (rect[2] / 2))
    OldRange = img_width
    NewRange = camera.CAMERA_H_FOV
    NewMin = photo_angle - int(camera.CAMERA_H_FOV / 2)
    angle = ((center * NewRange) / OldRange) + NewMin
    angle = round(angle, 1)
    return angle
