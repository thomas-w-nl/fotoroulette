import cv2
from log import *

# TODO: Dit bestand moet nog gedocumenteerd worden, en miss moeten wat namen duidelijker en return waardes op videoCapture enzo.

def getFace(frame):
    log.debug(frame)
    imgGrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarCascades/haarcascade_frontalface_alt.xml")
    if face_cascade == None:
        log.error("Face cascade failed to load!")
    # mijn C lijn, TODO: uitzoeken wat al die shizzel achter imgGrey/faces is.
    # face_cascade.detectMultiScale(imgGrey, faces, 1.1, 2, 0 | cv::CASCADE_SCALE_IMAGE, cv::Size(30, 30));
    faces = face_cascade.detectMultiScale(imgGrey, 1.3, 5)
    return faces


def drawRectangle(frame, rect):
    for (x, y, w, h) in rect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


# Untested omdat het nog steeds niet werkt op mijn pc...
def videoCapture():
    # TODO: deze moet eingelijk een frame returnen ofzo
    cap = cv2.VideoCapture(0)

    if cap.isOpened() == None:
        log.error("Could not open camera")

    while 1:
        ret, frame = cap.read()
        # TODO: dit moet eigenlijk dynamish
        frame = drawRectangle(frame, getFace(frame))
        cv2.imshow("vid", frame)
        if cv2.waitKey(27) >= 0: break


def imgRecon():
    """
    test function
    :return: niks
    """
    # cwd should be the git project root in order to work!

    # get img
    imgName = "arnold.jpg"
    img = cv2.imread("img/" + imgName)

    # display rectangle
    # img = drawRectangle(img, getFace(img))

    # cut
    img = cut(img, getFace(img))

    # write img
    # cv2.imwrite("out/" + imgName, img)

    # display img
    cv2.imshow("I need to find John Connor!", img)
    cv2.waitKey(0)


def cut(frame, rect):
    log.debug(rect)
    for (x, y, w, h) in rect:
        # TODO: Dit moet eigenlijk met arrays werken anders werkt het niet meer meerdere gezichten.
        return frame[y:(y+h), x:(x+w)]


if __name__ == "__main__":
    # only use this for testing!
    # imgRecon()
    videoCapture()
