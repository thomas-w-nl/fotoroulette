import cv2


# Tools die gewoon handig zijn


# TODO: Gebruik of geen type annotations of ALLEEN type annotations.
def select_random(source, amount: int):
    """
    Select 'amount' random uit de array en returnt deze.
    """
    # pick = random.randrange(0, len(image_list))
    pass


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


# TODO: De punt hiervan?
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
    cv2.waitKey()
