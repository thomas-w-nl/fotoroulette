import cv2
import numpy as np

from common.log import *
from hardware import camera
from processing.collect_photos import collect_photos
from processing.photo_data import PhotoData, Photo
from typing import List, Tuple
from common import tools

# todo dit moet vanuit git config
#: De drempelwaarde voor gezichts herkenning. 0.65 is voor de huidige fotos een goede waarde.
from src.processing.photo_data import RangeSensor

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


class Face:
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


class Faces:
    def __init__(self, photos_with_data: PhotoData):
        """
        Een datatype voor de uniek gezichten uit meerder fotos die voldoen aan een bepaalde drempelwaarde
        uit het PhotoData object.

        Args:
            photos_with_data: De fotos met sensor en orientatie data
        """

        self.faces = get_faces(photos_with_data)

    def __iter__(self):
        yield self.faces


def get_faces(photos_with_data: PhotoData) -> List[np.array]:
    """
    Returned de uniek gezichten uit meerdere fotos die voldoen aan een bepaalde drempelwaarde.

    Args:
       photos_with_data: De fotos met sensor en orientatie data

    Returns:
       Een lijst met de gezichten.
    """
    # dit is misschien iets te pro, er gaat toch best wat logic door heen en dat is miss niet zo handig in 1 regel
    # Rewrite is_unique as a filter so we can make this a oneliner
    # all_heads = [_cut_out_head(face, photo) for face in photo
    #              for photo in photos_with_data]
    all_faces = []

    for photos, range_sensor in photos_with_data:
        for photo in photos:

            for opencv_face in _opencv_get_faces(photo):

                if not _confident(opencv_face, range_sensor):
                    continue

                head = _cut_out_head(opencv_face, photo)

                _append_or_replace(all_faces, head, len(photo))


    return all_faces


def _confident(opencv_face, range_sensor: RangeSensor) -> bool:
    face_pos, confidence = opencv_face
    # scale opencv confidence naar 0 tot 1
    opencv_confidence = confidence / OPENCV_MAX_FACE_CONFIDENCE
    range_confidence = range_sensor.get_confidence(face_pos)

    total_confidence = (range_confidence * RANGE_SENSOR_WEIGHT) + (opencv_confidence * OPENCV_WEIGHT)

    if total_confidence > MIN_FACE_CONFIDENCE:
        return True
    return False


def _append_or_replace(all_faces: List[Face], cur_face: Face, photo_width: int) -> bool:
    """
    Voegt een gezicht toe aan all_faces als het gezicht uniek is. Als
    het gezicht beter in beeld is dan een oud gezicht wordt deze
    vervangen

    Args:
       all_faces: list met alle gezichten
       cur_face: Het gezicht om toe te voegen
       photo_width: De breedte van de foto

    Returns:
       Of de foto al eerder gezien is
    """

    for other_face in all_faces:
        # if het huidige gezicht dicht bij een oud gezicht zit
        if abs(other_face.angle - cur_face.angle) < NEARBY_FACE_ANGLE_DIFF_MAX:

            # if het huidige gezicht dichter bij het midden van de camera is, vervang het oude gezicht
            other_face_dist_to_photo_center = abs(other_face.pos_in_photo - (photo_width / 2))
            cur_face_dist_to_photo_center = abs(cur_face.pos_in_photo - (photo_width / 2))

            if other_face_dist_to_photo_center > cur_face_dist_to_photo_center:
                all_faces.remove(other_face)
                all_faces.append(cur_face)
                return False

    return True


# Refactor into photo class
def _opencv_get_faces(photo: np.array):
    """
    Geeft alle gezichten terug die door opencv gevonden worden in de foto, met de confidence score voor elk gezicht

    Args:
       photo: De foto met gezichten

    Returns:
       Een list met de coordinaten van de gezichten en een lijst met confidence scores
    """
    img_gray = cv2.cvtColor(photo.get_photo(), cv2.COLOR_BGR2GRAY)

    # TODO Deze shizzel moet vanuit de git-root, niet twee mapjes terug. Dit is error prone!
    face_cascade = cv2.CascadeClassifier("../haarCascades/haarcascade_frontalface_default.xml")

    if face_cascade is None:
        message = "Face cascade failed to load!"
        log.error(message)
        raise FileNotFoundError(message)

    # https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
    faces, _, confidences = face_cascade.detectMultiScale3(
        img_gray,
        scaleFactor=OPENCV_SCALE_FACTOR,
        minNeighbors=OPENCV_MIN_NEIGHBORS,
        minSize=(OPENCV_MIN_FACE_SIZE, OPENCV_MIN_FACE_SIZE),
        outputRejectLevels=True
    )

    # Moet een tuple zijn
    return zip(faces, confidences)


def _crop_image(img: np.array, rect) -> np.array:
    """
    Knip een vierkant uit een array zoals aangegeven in rect

    Args:
       img: foto
       rect: (x,y,w,h) (top left xt coordinates, width and height)

    Returns:
       De uitgeknipte foto.
    """
    x, y, w, h = rect
    return img[y:(y + h), x:(x + w)]


def _cut_out_head(face: np.array, photo: Photo) -> Face:
    """
    Haalt een gezicht uit de foto en geeft die weer terug als een aparte foto

    Args:
        face: De locatie van het gezicht gedetecteerd door openCV en de range sensor
        photo: De volledige foto waaruit je wilt knippen

    Returns:
        De gezicht als een aparte foto
    """

    face_pos, _ = face
    cutout = _crop_image(photo.get_photo(), face_pos)

    return cutout
