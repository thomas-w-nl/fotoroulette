from time import sleep

import numpy as np
import cv2
from src.common.log import *

def generate_overlay(game):
    """
    Generate the overlay with the given parameters

    Args:
         game: the [Game] object

    Returns:
        returns the created overlay
    """
    overlay = cv2.imread(game.overlay)

    overlay_height, overlay_width, overlay_channel = overlay.shape

    for i, face in enumerate(game.faces):
        face_offset = game.offsets[i]

        face.image = _resize_fit(face.image,
                                 int(overlay_width / 2) - face_offset['minus_image_width'],
                                 overlay_height - face_offset['minus_image_width'])

        overlay = _apply_overlay(i, overlay, face.image, face_offset['offset_x'], face_offset['offset_y'], game)

    return overlay


def _apply_overlay(index, bg, fg, offset_x, offset_y, game):
    """
    Adds each face and background to the image

    Args:
        index: the index of the current image in the game faces
        bg: the image background/ overlay. The is mostly the returned image for the previous call
        fg: the current face
        offset_x: the x-axis offset for the face
        offset_y: the y-axis offset for the face
        game: the game type itself

    Returns:
        returns the modified image
    """
    rows_fg, cols_fg, channels_fg = fg.shape
    rows_bg, cols_bg, channels_bg = bg.shape

    # create new image to use as base
    background = np.empty((rows_bg, cols_bg, 3), np.uint8)

    if game.background_color is not None and index is 0:
        background[rows_bg - 1, cols_bg - 1] = game.background_color
    elif game.extra_background is not None and index is 0:
        background = bg

    if (offset_x < -100) or (offset_x < -100):
        raise ValueError('offset more than 100%')

    # negative numbers from -100 to 1 are percentage offsets
    if offset_y < 0:
        offset_y_percentage = offset_y * -0.01
        offset_y = int((rows_bg - rows_fg) * offset_y_percentage)

    if offset_x < 0:
        offset_x_percentage = offset_x * -0.01
        offset_x = int((cols_bg - cols_fg) * offset_x_percentage)

    if (rows_fg > rows_bg) or (cols_fg > cols_bg):
        raise ValueError('Overlay bigger than background')

    if ((offset_y + rows_fg) > rows_bg) or ((offset_x + cols_fg) > cols_bg):
        raise ValueError('offset too big')

    roi_rows_end = offset_y + rows_fg
    roi_cols_end = offset_x + cols_fg

    # if the overlay has transparent parts (on top of the faces)
    # else, just add the faces
    if game.on_top:
        # Create mask, remove mask and place overlay on [background]
        background[offset_y:roi_rows_end, offset_x:roi_cols_end] = fg

        gray_fg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_fg, 0, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        over_bg = cv2.bitwise_and(background, background, mask=mask_inv)
        over_bg = cv2.add(over_bg, bg)

        background = over_bg
    else:
        background = bg

        background[offset_y:roi_rows_end, offset_x:roi_cols_end] = fg

    return background


def _resize_fit(image: np.array, max_width: int, max_height: int) -> np.array:
    """
    Resize [image] to fit the [max_width] and [max_height] params

    Args:
        image: np.array image
        max_width: max width in pixels
        max_height: max height in pixels

    Returns:
        resized image
    """
    height, width, channels = image.shape
    log.debug("RESIZE IMAGE INFO =====> width:" + str(width) + " height:" + str(height))


    scale_width = max_width / width
    scale_height = max_height / width

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    return res
