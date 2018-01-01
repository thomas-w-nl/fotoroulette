import os

import cv2


# Tools die gewoon handig zijn


def draw_rectangle(frame, rect, texts=("")):

    height, width, _ = frame.shape
    x, y, w, h = rect
    letter_size_px = 25
    text_margin_px = 2

    # float text left or right of rect, based on the longest text

    longest_text = 0
    for text in texts:
        if len(text) > longest_text:
            longest_text = len(text)

    text_size = letter_size_px * longest_text
    text_offset = int(x + w + text_margin_px)
    if width - text_offset < text_size:
        text_offset = int(x - text_size - text_margin_px)

    text_nr = 1
    for text in texts:
        frame = draw_text(frame, text, (text_offset, int(y + (text_nr * letter_size_px))))
        text_nr += 1

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

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
    cv2.putText(img, text, pos, font, size, (0, 0, 255), thickness, cv2.LINE_AA)
    return img


def visualize_angle_in_image(img, offset, angle):
    v, h, _ = img.shape
    text_offset = offset
    if h - offset < 30:
        text_offset = offset - (25 * len(str(angle)))

    cv2.line(img, (offset, 0), (offset, v), (255, 0, 0), 2)
    img = draw_text(img, str(angle), (text_offset + 4, 30))
    return img
