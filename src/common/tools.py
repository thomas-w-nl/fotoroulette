import os

import cv2


# Tools die gewoon handig zijn




# TODO: Wat is de punt van deze functie?
def draw_rectangle(frame, rect):
    """
    draw een vierkantje op de gewenste lokatie

    Args:
       frame (:obj:`cv2.Mat`): Een foto om op te tekenen
       rect: De coordinaten om te rekenen

    Returns:
       Een plaatje (:obj:`cv2.Mat`) met een vierkantje
    """
    for (x, y, w, h) in rect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


def draw_image(img):
    """
    Laat het plaatje zien.
    :rtype: void
    :param: plaatje
    """
    cv2.imshow("FYS", img)
    cv2.waitKey()


def draw_text(img, text, pos, size=1):
    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = 1
    cv2.putText(img, text, pos, font, size, (255, 255, 255), thickness, cv2.LINE_AA)
    return img


def visualize_angle_in_image(img, offset, angle):
    v, h, _ = img.shape
    text_offset = offset
    if h - offset < 30:
        text_offset = offset - (25 * len(str(angle)))

    cv2.line(img, (offset, 0), (offset, v), (255, 0, 0), 2)
    img = draw_text(img, str(angle), (text_offset + 4, 100))
    return img
