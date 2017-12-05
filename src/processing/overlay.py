from cv2 import cv2

import numpy as np


def generate_overlay(game, index_left_face: int, index_right_face: int, offset_y: int, minus_image_width: int,
                     offset_left_face: int, offset_right_face: int):
    """
    Generate the overlay with the given parameters
    :param game: the [Game] object
    :param index_left_face: index of the [Game]'s [faces] array for the left image
    :param index_right_face: index of the [Game]'s [faces] array for the right image
    :param offset_y: the y-axis offset, in pixels, for both faces
    :param minus_image_width: use this of images need to be smaller, in pixels
    :param offset_left_face: the offset for the left image in pixels, or in percentages if negative number
    :param offset_right_face: the offset for the right image in pixels, or in percentages if negative number
    :return: returns the created overlay
    """
    overlay = cv2.imread(game.overlay)

    overlay_height, overlay_width, overlay_channel = overlay.shape

    for i in [index_left_face, index_right_face]:
        face = game.faces[i]

        face.face_image = _resize_fit(face.face_image, int(overlay_width / 2) - minus_image_width, overlay_height - minus_image_width)

        fg_offset_y = offset_y
        fg_offset_x = offset_left_face
        if i is index_right_face:
            fg_offset_x = offset_right_face

        overlay = _apply_overlay(overlay, face.face_image, fg_offset_x, fg_offset_y, False)

    return overlay


def _apply_overlay(bg, fg, offset_x, offset_y, on_top=True):
    rows_fg, cols_fg, channels_fg = fg.shape
    rows_bg, cols_bg, channels_bg = bg.shape

    # create new image to use as base
    background = np.zeros((rows_bg, cols_bg, 3), np.uint8)

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
    if on_top:
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
    :param image: np.array image
    :param max_width: max width in pixels
    :param max_height: max height in pixels
    :return: resized image
    """
    height, width, channels = image.shape

    scale_width = max_width / width
    scale_height = max_height / width

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    return res
