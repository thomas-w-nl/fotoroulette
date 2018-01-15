from time import sleep

import numpy as np
import cv2
from src.common.log import *

def generate_overlay(game):
    """
    Generates the final image with the faces and overlays

    Args:
         game: the [Game] object

    Returns:
        returns the final image as np.array
    """
    # the overlay to place on top of the image with background and faces
    final_overlay = cv2.imread(game.overlay)
    final_overlay_height, final_overlay_width, final_overlay_channels = final_overlay.shape

    # image with game background
    place_holder_image = np.empty((final_overlay_height, final_overlay_width, 3), np.uint8)
    if game.background_color is not None:
        place_holder_image[:, :] = game.background_color
    elif game.extra_background is not None:
        place_holder_image = cv2.imread(game.extra_background)

    cv2.imshow('output', place_holder_image)
    print('===place_holder_image===')
    cv2.waitKey()

    for index, face in enumerate(game.faces):
        face_offset = game.offsets[index]
        face.image = _resize_fit(face.image, int(final_overlay_width / 2) - face_offset['minus_image_width'],
                                 final_overlay_height - face_offset['minus_image_width'])

        face_height, face_width, face_channels = face.image.shape

        offset_x = face_offset['offset_x']
        offset_y = face_offset['offset_y']

        if (offset_x < -100) or (offset_x < -100):
            raise ValueError('offset more than 100%')

        # negative numbers from -100 to 1 are percentage offsets
        if offset_y < 0:
            offset_y_percentage = offset_y * -0.01
            offset_y = int((final_overlay_height - face_width) * offset_y_percentage)

        if offset_x < 0:
            offset_x_percentage = offset_x * -0.01
            offset_x = int((final_overlay_width - face_height) * offset_x_percentage)

        if (face_height > final_overlay_height) or (face_width > final_overlay_width):
            raise ValueError('Overlay bigger than background')

        if ((offset_y + face_height) > final_overlay_height) or ((offset_x + face_width) > final_overlay_width):
            raise ValueError('offset too big')

        roi_height_end = offset_y + face_height
        roi_width_end = offset_x + face_width

        # PLACE FACE
        # Create mask, remove mask and place overlay on [background]
        # place_holder_image[offset_y:roi_height_end, offset_x:roi_width_end] = face.image
        #
        # cv2.imshow('output', place_holder_image)
        # print('===place_holder_image with face===')
        # cv2.waitKey()
        #
        # gray_fg = cv2.cvtColor(final_overlay, cv2.COLOR_BGR2GRAY)
        #
        # cv2.imshow('output', gray_fg)
        # print('===gray_fg===')
        # cv2.waitKey()
        #
        # _, mask = cv2.threshold(gray_fg, 0, 255, cv2.THRESH_BINARY)
        #
        # cv2.imshow('output', mask)
        # print('===mask===')
        # cv2.waitKey()
        #
        # mask_inv = cv2.bitwise_not(mask)
        #
        # over_bg = cv2.bitwise_and(place_holder_image, place_holder_image, mask=mask_inv)
        # over_bg = cv2.add(over_bg, final_overlay)
        #
        # cv2.imshow('output', over_bg)
        # print('===over_bg===')
        # cv2.waitKey()

        # place_holder_image = over_bg
        place_holder_image = transparent_overlay(place_holder_image, cv2.imread(game.overlay))


    return place_holder_image


def transparent_overlay(src, overlay, pos=(0, 0), scale=1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            # alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            alpha = .9
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


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

