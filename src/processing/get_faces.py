import cv2
import numpy as np

from src.common.log import *
from src.hardware import camera
from src.processing.collect_photos import collect_photos
from src.processing.photo_data import PhotoData, Photo
from typing import List, Tuple
from src.common import tools

# todo dit moet vanuit git config

from src.processing.photo_data import RangeSensor

#: De drempelwaarde voor gezichts herkenning. 0.65 is voor de huidige fotos een goede waarde.
MIN_FACE_CONFIDENCE = 0.2

#: OpenCV gezichts detectie instellingen
OPENCV_MIN_FACE_SIZE = 50
OPENCV_SCALE_FACTOR = 1.1
OPENCV_MIN_NEIGHBORS = 4

#: Het maximum verschil waarbij twee gezichten als een wordt gezien in graden
NEARBY_FACE_ANGLE_DIFF_MAX = 2

#: De waarde van opencv vs de range sensor en is een waarde van :math:`1.0 <= x <= 0.0`.
OPENCV_WEIGHT = 0.7
RANGE_SENSOR_WEIGHT = 1 - OPENCV_WEIGHT
OPENCV_MAX_FACE_CONFIDENCE = 10  # er is geen documentatie voor, het lijkt er op dat dit de max wel is

HAAR_CASCADE_PATH = "haarCascades/haarcascade_frontalface_default.xml"
DEBUG = True

CUTOUT_PADDING_FACTOR = 3.5


class Face:
    def __init__(self, opencv_face, photo_angle: float, face_image: np.array):
        """
        Een datatype voor een gezicht

        Args:
            face_pos: positie van het gezicht (x, y, w, h)
            angle: hoek ten opzichte van het start van de camera in graden
            confidence: De zekerheid of het een gezicht is
            face_image: De uitgeknipte foto
        """
        face_pos, opencv_confidence = opencv_face
        avg_pos = round(face_pos[0] + (face_pos[2] / 2))
        self.pos = face_pos
        self.confidence = opencv_confidence / OPENCV_MAX_FACE_CONFIDENCE
        self.angle = _location_to_angle(photo_angle, avg_pos)
        self.avg_pos = avg_pos
        self.image = face_image


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

    photos, range_sensor = photos_with_data.get()

    for photo, angle in photos:
        if DEBUG:
            print("\n----- next photo ----- \n")
        for opencv_face in _opencv_get_faces(photo):

            face = Face(opencv_face, angle, None)

            if not _confident(face, range_sensor):
                continue

            face.image = _cut_out_head(face, photo)
            if DEBUG:
                cv2.imshow(str(face.angle), face.image)
                cv2.waitKey()

            _append_or_replace(all_faces, face)

    if DEBUG:
        print("number of faces found:", len(all_faces))
    return all_faces


def _confident(face: Face, range_sensor: RangeSensor) -> bool:
    # scale opencv confidence naar 0 tot 1
    opencv_confidence = face.confidence

    range_confidence = range_sensor.get_confidence(face.avg_pos)

    total_confidence = (range_confidence * RANGE_SENSOR_WEIGHT) + (opencv_confidence * OPENCV_WEIGHT)

    if total_confidence > MIN_FACE_CONFIDENCE:
        return True

    if DEBUG:
        print("discarding a face, not confident enough (", total_confidence, ")")
    return False


def _append_or_replace(all_faces: List[Face], cur_face: Face) -> bool:
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

    photo_width, _ = camera.CAMERA_RESOLUTION

    for other_face in all_faces:

        if DEBUG:
            print("Comparing: other:", other_face.angle, "current:", cur_face.angle)
        # if het huidige gezicht dicht bij een oud gezicht zit
        if abs(other_face.angle - cur_face.angle) < NEARBY_FACE_ANGLE_DIFF_MAX:
            if DEBUG:
                print("> Face might get replaced")

            # if het huidige gezicht dichter bij het midden van de camera is, vervang het oude gezicht
            other_face_dist_to_photo_center = abs(other_face.avg_pos - (photo_width / 2))
            cur_face_dist_to_photo_center = abs(cur_face.avg_pos - (photo_width / 2))

            if other_face_dist_to_photo_center > cur_face_dist_to_photo_center:
                if DEBUG:
                    print("Replacing face")
                all_faces.remove(other_face)
                all_faces.append(cur_face)
                return False

            if DEBUG:
                print("Skipping face, not best position")
            return True

    #
    all_faces.append(cur_face)
    return False


# Refactor into photo class
def _opencv_get_faces(photo: np.array):
    """
    Geeft alle gezichten terug die door opencv gevonden worden in de foto, met de confidence score voor elk gezicht

    Args:
       photo: De foto met gezichten

    Returns:
       Een list met de coordinaten van de gezichten en een lijst met confidence scores
    """
    img_gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

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

    if DEBUG and len(faces):
        print("got " + str(len(faces)) + " faces! (in one foto)")

    # Moet een tuple zijn
    return zip(faces, confidences)


def _crop_image(img: np.array, rect: list, padding: int) -> np.array:
    """
    Knip een vierkant uit een array zoals aangegeven in rect, met padding in pixels

    Args:
       img: foto
       rect: (x,y,w,h) (top left xt coordinates, width and height)

    Returns:
       De uitgeknipte foto.
    """
    x, y, w, h = rect
    return img[y:(y + h), x:(x + w)]


def _cut_out_head(face: Face, photo: Photo) -> np.array:
    """
    Haalt een gezicht uit de foto en geeft die weer terug als een aparte foto

    Args:
        opencv_face: De locatie van het gezicht gedetecteerd door openCV en de range sensor
        photo: De volledige foto waaruit je wilt knippen

    Returns:
        De gezicht als een aparte foto
    """
    x, y, w, h = face.pos
    padding = int(round(w * CUTOUT_PADDING_FACTOR))
    cutout = _crop_image(photo, face.pos, padding)

    return cutout


def _location_to_angle(photo_angle: float, position: int) -> float:
    """
    Zet een locatie op een foto gemaakt op hoek photo_angle om naar de hoek van de locatie.

    Args:
       photo_angle: De hoek waarop de foto is gemaakt
       position: De locatie als int

    Returns:
       De hoek van de locatie ten opzichte van het startpunt van de camera
    """

    # scale van range(0, img_width) naar range(-camera.CAMERA_H_FOV/2, camera.CAMERA_H_FOV/2) met offset photo_angle
    img_width, _ = camera.CAMERA_RESOLUTION
    OldRange = img_width
    NewRange = camera.CAMERA_H_FOV
    NewMin = photo_angle - int(camera.CAMERA_H_FOV / 2)
    angle = ((position * NewRange) / OldRange) + NewMin
    angle = round(angle, 1)

    if DEBUG:
        print("\n==start angle decoding==")
        print("image width:", img_width)
        print("face pos", position)
        print("photo angle:", photo_angle)
        print("result:", angle)

        print("==stop angle decoding==\n")

    return angle
