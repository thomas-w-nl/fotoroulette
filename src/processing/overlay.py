from cv2 import cv2

import numpy as np

# todo moet ook image path en face image offsets bevatten voor elke game type
from src.processing.get_faces import Face


class GameType:
    VERSUS = 0
    SUPERHEROES = 1
    LOVEMETER = 3


def apply_overlay(bg, fg, offset_x, offset_y, on_top=True):
    rows_fg, cols_fg, channels_fg = fg.shape
    rows_bg, cols_bg, channels_bg = bg.shape

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

    cv2.destroyAllWindows()

    return background


def resize_fit(image: np.array, max_width: int, max_height: int) -> np.array:
    height, width, channels = image.shape

    scale_width = max_width / width
    scale_height = max_height / width

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    return res
