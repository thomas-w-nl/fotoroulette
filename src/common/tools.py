import cv2


# Tools die gewoon handig zijn

# TODO
def select_random(source, amount: int):
    """
    Select 'amount' random uit de array en returnt deze.
    :rtype: array
    """
    # pick = random.randrange(0, len(image_list))
    pass


def draw_rectangle(frame, rect):
    """
    draw een vierkantje op de gewenste lokatie
    :param: frame: cv2 Mat om op te tekenen
    :param: rect: (x, y, w, h)
    :rtype: cv2.Mat
    :return: plaatje met vierkantje
    """
    for (x, y, w, h) in rect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame


# TODO
def draw_text(frame, string: str, rect):
    """
    :arg: frame: Het plaatje waarom getekent moet worden
    :arg: rect: locatie (x, y, w, h)
    :arg: string: de tekst die op het plaatje moet worden geprint
    :rtype: cv2.Mat
    :return: frame met het tekstje
    """
    pass


def get_image(path: str):
    """
    laad een plaatje in!
    :arg: dir naar het plaatje
    :rtype: cv2.Mat
    :return: Het plaatje
    """
    return cv2.imread(path)


def draw_image(img):
    """
    Laat het plaatje zien.
    :rtype: void
    :param: plaatje
    """
    cv2.imshow("FYS", img)
    # cv2.waitKey(0)

