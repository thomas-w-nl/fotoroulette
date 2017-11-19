import cv2
import numpy as np

from src.hardware import camera
from src.processing.collect_photos import collect_photos
from src.processing.photo_data import PhotoData

# face confidence threshold
MIN_FACE_CONFIDENCE = 0.5
OPENCV_WEIGHT = 0.7

RANGE_SENSOR_WEIGHT = 1 - OPENCV_WEIGHT
OPENCV_MAX_FACE_CONFIDENCE = 10  # er is geen documentatie voor, het lijkt er op dat dit de max wel is


def get_faces(photos_with_data: PhotoData) -> list:
    all_faces = []

    for single_photo in photos_with_data:
        photo = single_photo[0]
        photo_angle = single_photo[1]

        imgGrey = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier("../../haarCascades/haarcascade_frontalface_default.xml")

        if face_cascade == None:
            print("Face cascade failed to load!")
            quit(1)

        # https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
        faces_with_levels = face_cascade.detectMultiScale3(
            imgGrey,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            outputRejectLevels=True
        )

        faces = faces_with_levels[0]
        confidences = faces_with_levels[2]

        for face, confidence in zip(faces, confidences):
            img_width = len(photo[0])
            angle = location_to_angle(img_width, photo_angle, face)
            cropped_face = crop_image(photo, face)

            sensor_confidence = photos_with_data.get_sensor_confidence(angle)
            opencv_confidence = confidence / OPENCV_MAX_FACE_CONFIDENCE
            total_confidence = (sensor_confidence * RANGE_SENSOR_WEIGHT) + (opencv_confidence * OPENCV_WEIGHT)

            print("sensor confidence: " + str(sensor_confidence))
            print("opencv confidence: " + str(opencv_confidence))
            print("total  confidence: " + str(total_confidence))

            if total_confidence > MIN_FACE_CONFIDENCE:
                all_faces.append((cropped_face, angle))

    pass


def crop_image(img: np.array, rect: list) -> np.array:
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]

    return img[y:(y + h), x:(x + w)]


def location_to_angle(img_width, photo_angle, rect: list) -> int:
    center = round(rect[0] + (rect[2] / 2))
    OldRange = img_width
    NewRange = camera.CAMERA_H_ANGLE
    NewMin = photo_angle - int(camera.CAMERA_H_ANGLE / 2)
    angle = round((((center) * NewRange) / OldRange) + NewMin)
    return angle


photo_data = collect_photos()
get_faces(photo_data)
