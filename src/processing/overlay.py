from time import sleep

import numpy as np
import cv2
from PIL import Image, ImageMode
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
        face.image = _resize_fit(face.image, int(final_overlay_width / 2) - face_offset['minus_image_width'],
                                 final_overlay_height - face_offset['minus_image_width'])

        f = Image.fromarray(cv2.cvtColor(face.image, cv2.COLOR_BGR2RGB))

        face_height, face_width = f.size

        offset_x = face_offset['offset_x']
        offset_y = face_offset['offset_y']
        #
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

        place_holder_image.paste(f, (offset_x, offset_y))

        place_holder_image = Image.alpha_composite(place_holder_image, final_overlay)

    return place_holder_image


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

