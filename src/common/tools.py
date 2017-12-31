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


# TODO:
def draw_text(frame, string: str, rect):
    """

    Args:
       frame (:obj:`cv2.Mat`): Een plaatje waarom getekent moet worden
       rect: coordinaten (x, y, w, h)
       string(str): De tekst die op het plaatje moet worden geprint

    Returns:
       Een frame (:obj:`cv2.Mat`) met het teksts
    """
    pass


def draw_image(img):
    """
    Laat het plaatje zien.
    :rtype: void
    :param: plaatje
    """
    cv2.imshow("FYS", img)
    cv2.waitKey()
