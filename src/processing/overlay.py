from time import sleep

import numpy as np
import cv2
from PIL import Image, ImageMode
from src.common.log import *

DEBUG = False


def generate_overlay(game):
    """
    Generates the final image with the faces and overlays

    Args:
         game: the [Game] object

    Returns:
        returns the final image as np.array
    """
    # the overlay to place on top of the image with background and faces
    final_overlay = Image.open(game.overlay)
    final_overlay_width, final_overlay_height = final_overlay.size

    # image with game background
    place_holder_image = None
    if game.background_color is not None:
        place_holder_image = Image.new('RGBA', (final_overlay_width, final_overlay_height), game.background_color)
    elif game.extra_background is not None:
        place_holder_image = Image.open(game.extra_background)
    else:
        place_holder_image = Image.new('RGBA', (final_overlay_width, final_overlay_height))

    for index, face in enumerate(game.faces):
        face_offset = game.offsets[index]

        resize_max_width = int(final_overlay_width / 2) - face_offset['minus_image_width']
        resize_max_height = int(final_overlay_height - face_offset['minus_image_width'])

        face.image = _resize_fit(face.image, resize_max_width, resize_max_height)

        f = Image.fromarray(cv2.cvtColor(face.image, cv2.COLOR_BGR2RGB))

        face_width, face_height = f.size

        offset_x = face_offset['offset_x']
        offset_y = face_offset['offset_y']
        #
        if (offset_x < -100) or (offset_x < -100):
            raise ValueError('offset more than 100%')

        # negative numbers from -100 to 1 are percentage offsets
        if offset_y < 0:
            offset_y_percentage = offset_y * -0.01
            offset_y = int((final_overlay_height - face_height) * offset_y_percentage)

        if offset_x < 0:
            offset_x_percentage = offset_x * -0.01
            offset_x = int((final_overlay_width - face_width) * offset_x_percentage)

        if ((offset_y + face_height) > final_overlay_height) or ((offset_x + face_width) > final_overlay_width):
            err = "\nDetailed description of vague error:\n"
            err += "offset_y = " + str(offset_x) + "\n"
            err += "face_height = " + str(face_width) + "\n"

            err += "offset_x = " + str(offset_x) + "\n"
            err += "face_width = " + str(face_width) + "\n"

            err += "((offset_y + face_height) > final_overlay_height) = " + str(offset_y + face_height) + \
                   ">" + str(final_overlay_height) + "\n"
            err += "OR\n"
            err += "(offset_x + face_width) > final_overlay_width) = " + str(offset_x + face_width) + \
                   ">" + str(final_overlay_width) + "\n"
            log.error(err)

            raise ValueError('Face is out of image bounds')

        place_holder_image.paste(f, (offset_x, offset_y))

        place_holder_image = Image.alpha_composite(place_holder_image, final_overlay)

    return cv2.cvtColor(np.array(place_holder_image), cv2.COLOR_RGB2BGR)


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
    if DEBUG:
        log.debug("image to resize width:" + str(width) + " height:" + str(height))

    scale_width = max_width / width
    scale_height = max_height / height

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    return res
