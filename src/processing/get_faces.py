import configparser
from typing import List

import numpy as np

from src.common.log import *
from src.common.tools import *
from src.processing.photo_data import PhotoData, Photo, RangeSensor

DEBUG = 0  # 2

config = configparser.ConfigParser()
config.read('fotoroulette.conf')


class Face:
    def __init__(self, opencv_face, photo_angle: float, face_image: np.array):
        """
        Bevat een uitgeknipt gezicht met positie informatie

        Args:
            face_pos: positie van het gezicht (x, y, w, h)
            angle: hoek ten opzichte van het start van de camera in graden
            confidence: De zekerheid of het een gezicht is
            face_image: De uitgeknipte foto
        """
        OPENCV_MAX_FACE_CONFIDENCE = 12  # er is geen documentatie voor, het lijkt er op dat dit de max wel is

        face_pos, opencv_confidence = opencv_face
        avg_pos = round(face_pos[0] + (face_pos[2] / 2))
        self.pos = face_pos
        self.confidence = opencv_confidence[0] / OPENCV_MAX_FACE_CONFIDENCE
        self.angle = _location_to_angle(photo_angle, avg_pos)
        self.avg_pos = avg_pos
        self.image = face_image


class Faces:
    def __init__(self, photos_with_data: PhotoData):
        """
        Een datatype voor de uniek gezichten uit meerder fotos die voldoen aan een bepaalde drempelwaarde
        uit het PhotoData object.

        Args:
            photos_with_data: De fotos met sensor en orientatie data als PhotoData object
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

    if DEBUG >= 2:
        first = True
        for photo, angle in photos:
            # print center line in image
            v, h, _ = photo.shape
            h = int(h / 2)
            calculated_angle = _location_to_angle(angle, h)
            calculated_angle = int(round(calculated_angle, 0))
            visualize_angle_in_image(photo, h, calculated_angle)

            # print minimum face size and scale factor
            if first:
                first = False
                min_face_size = config['FaceDetection'].getint('OPENCV_MIN_FACE_SIZE')
                scale_factor = config['FaceDetection'].getfloat('OPENCV_SCALE_FACTOR')
                photo = draw_rectangle(photo, (0, 0, min_face_size, min_face_size),
                                       ("  min face size (" + str(min_face_size) + ")", ""))
                photo = draw_rectangle(photo,
                                       (0, 0, int(min_face_size * scale_factor), int(min_face_size * scale_factor)),
                                       ("", " detection step size (" + str(scale_factor) + ")"))

    for photo, angle in photos:
        if DEBUG:
            print("\n----- next photo ----- ")

        for opencv_face in _opencv_get_faces(photo):

            face = Face(opencv_face, angle, None)

            if not _confident(face, range_sensor):
                continue

            face.image = _cut_out_head(face, photo)
            _append_or_replace(all_faces, face)

            # mark a detected face
            if DEBUG >= 2:
                x, y, w, h = face.pos
                photo = draw_rectangle(photo, face.pos, (
                    str(face.angle) + "deg", str(round(face.confidence, 2)), str(w) + "x" + str(h) + " px"))

                # calculate face size in degrees
                left_bound = _location_to_angle(angle, x)
                right_bound = _location_to_angle(angle, x + w)
                print("Face size (in degrees):", abs(left_bound - right_bound))

    # display debug info with photos
    if DEBUG >= 1:
        for photo, angle in photos:
            cv2.imshow("img", photo)
            cv2.waitKey()

    if DEBUG >= 1:
        print("number of faces found:", len(all_faces))
    return all_faces


def _confident(face: Face, range_sensor: RangeSensor) -> bool:
    """
    Bereken de confidence score van een gezicht aan de hand van OpenCV en de range sensor
    Args:
        face: Het gezicht
        range_sensor: De range sensor data

    Returns:
        Of het gezicht voldoet

    """
    opencv_confidence = face.confidence

    OPENCV_WEIGHT = config['FaceDetection'].getfloat('OPENCV_WEIGHT')

    range_sensor_weight = 1 - OPENCV_WEIGHT

    MIN_FACE_CONFIDENCE = config['FaceDetection'].getfloat('MIN_FACE_CONFIDENCE')
    range_confidence = range_sensor.get_confidence(face.avg_pos)

    total_confidence = (range_confidence * range_sensor_weight) + (opencv_confidence * OPENCV_WEIGHT)

    if total_confidence > MIN_FACE_CONFIDENCE:
        return True

    if DEBUG >= 1:
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
       Of de foto is toegevoegd
    """

    photo_width = config['Camera'].getint('CAMERA_RESOLUTION_H')
    nearby_face_angle_diff_max = config['FaceDetection'].getfloat('NEARBY_FACE_ANGLE_DIFF_MAX')

    if DEBUG >= 1:
        print("- Comparing", len(all_faces), " faces to current face -")

    for other_face in all_faces:

        if DEBUG >= 2:
            print("Comparing face: other:", other_face.angle, "current:", cur_face.angle)
        # if het huidige gezicht dicht bij een oud gezicht zit
        if abs(other_face.angle - cur_face.angle) < nearby_face_angle_diff_max:

            # if het huidige gezicht dichter bij het midden van de camera is, vervang het oude gezicht
            other_face_dist_to_photo_center = abs(other_face.avg_pos - (photo_width / 2))
            cur_face_dist_to_photo_center = abs(cur_face.avg_pos - (photo_width / 2))

            if other_face_dist_to_photo_center > cur_face_dist_to_photo_center:
                if DEBUG >= 2:
                    print("Nearby faces: Replacing face")
                all_faces.remove(other_face)
                all_faces.append(cur_face)
                return True

            if DEBUG >= 2:
                print("Nearby faces: Skipping face, not best position")
            return False

    # als er geen andere gezichten zijn of die zijn allemaal ver dan voegen we het gezicht toe
    all_faces.append(cur_face)
    return True


def _opencv_get_faces(photo: np.array):
    """
    Geeft alle gezichten terug die door opencv gevonden worden in de foto, met de confidence score voor elk gezicht

    Args:
       photo: De foto met gezichten

    Returns:
       Een list met de coordinaten van de gezichten en een lijst met confidence scores
    """
    img_gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(config['FaceDetection']['HAAR_CASCADE_PATH'])

    if face_cascade is None:
        message = "Face cascade failed to load!"
        log.error(message)
        raise FileNotFoundError(message)

    opencv_min_face_size = config['FaceDetection'].getint('OPENCV_MIN_FACE_SIZE')

    faces, _, confidences = face_cascade.detectMultiScale3(
        img_gray,
        scaleFactor=config['FaceDetection'].getfloat('OPENCV_SCALE_FACTOR'),
        minNeighbors=config['FaceDetection'].getint('OPENCV_MIN_NEIGHBORS'),
        minSize=(opencv_min_face_size, opencv_min_face_size),
        outputRejectLevels=True
    )

    if DEBUG and len(faces):
        print("got " + str(len(faces)) + " faces! (in one foto)")

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
    x -= padding
    y -= padding
    w += (padding * 2)
    h += (padding * 2)
    return img[y:(y + h), x:(x + w)]


def _cut_out_head(face: Face, photo: Photo) -> np.array:
    """
    Haalt een gezicht uit de foto en geeft die weer terug als een aparte foto

    Args:
        face: Het gezicht met locatie
        photo: De volledige foto waaruit je het gezicht wilt knippen

    Returns:
        Het gezicht als een aparte foto
    """
    CUTOUT_PADDING_FACTOR = config['FaceDetection'].getfloat('CUTOUT_PADDING_FACTOR')
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

    # todo misschien de foto mee geven en photo.shape gebruiken
    CAMERA_H_FOV = config['Camera'].getfloat('CAMERA_H_FOV')

    # scale van range(0, img_width) naar range(-CAMERA_H_FOV/2, CAMERA_H_FOV/2) met offset photo_angle
    OldRange = config['Camera'].getint('CAMERA_RESOLUTION_H')
    NewRange = CAMERA_H_FOV
    NewMin = 0 - int(CAMERA_H_FOV / 2)
    angle = ((position * NewRange) / OldRange) + NewMin
    angle = round(angle, 1)

    # 0px wordt 31 en 1600px wordt -31, dus flippen
    angle = 0 - angle

    # van local angle in de foto (30
    global_angle = photo_angle + angle

    return global_angle
