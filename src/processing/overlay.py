from cv2 import cv2

import numpy as np

# todo moet ook image path en face image offsets bevatten voor elke game type
from src.processing.get_faces import Face


class GameType:
    VERSUS = 0
    SUPERHEROES = 1
    ROULETTE = 2
    LOVEMETER = 3


def apply_overlay(bg, fg, offset_x, offset_y, on_top=True):
    rows_fg, cols_fg, channels_fg = fg.shape
    rows_bg, cols_bg, channels_bg = bg.shape

    background = np.zeros((rows_bg, cols_bg, 3), np.uint8)

    print("BG:", bg.shape)
    print("FG:", fg.shape)
    print("BACKGROUND", background.shape)

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

    # I want to put logo on top-left corner, So I create a Region of interest (ROI)
    roi_rows_end = offset_y + rows_fg
    roi_cols_end = offset_x + cols_fg

    # cv2.imshow('out', bg)
    # cv2.waitKey(0)

    # cv2.imshow('out', fg)
    # cv2.waitKey(0)

    roi = background[offset_y:roi_rows_end, offset_x:roi_cols_end]

    # cv2.imshow('out', roi)
    # cv2.waitKey(0)

    if on_top:
        # Now create a mask and create its inverse mask also
        gray_fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
        # 0 en 255 zijn cutoff values, we nemen nu de hele fg
        _, mask = cv2.threshold(gray_fg, 0, 255, cv2.THRESH_BINARY)

        cv2.imshow('out', mask)
        cv2.waitKey(0)

        mask_inv = cv2.bitwise_not(mask)

        cv2.imshow('out', mask_inv)
        cv2.waitKey(0)

        # Now black-out the area of logo in ROI
        bg_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        cv2.imshow('out', bg_bg)
        cv2.waitKey(0)

        # Take only region of logo from logo image.
        fg_fg = cv2.bitwise_and(fg, fg, mask=mask)
        # Put logo in ROI and modify the main image

        cv2.imshow('out', fg_fg)
        cv2.waitKey(0)
        #
        dst = cv2.add(bg_bg, fg_fg)

        cv2.imshow('out', dst)
        cv2.waitKey(0)

        background[offset_y:roi_rows_end, offset_x:roi_cols_end] = dst

        # Create mask, remove mask and place overlay on [background]

        background[offset_y:roi_rows_end, offset_x:roi_cols_end] = fg
        cv2.imshow('out', background)
        cv2.waitKey(0)

        gray_fg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_fg, 0, 255, cv2.THRESH_BINARY)

        cv2.imshow('out', mask)
        cv2.waitKey(0)

        mask_inv = cv2.bitwise_not(mask)

        cv2.imshow('out', mask_inv)
        cv2.waitKey(0)

        over_bg = cv2.bitwise_and(background, background, mask=mask_inv)
        cv2.imshow('out', over_bg)
        cv2.waitKey(0)

        over_bg = cv2.add(over_bg, bg)
        cv2.imshow('out', over_bg)
        cv2.waitKey(0)

        background = over_bg
    else:
        background = bg

        background[offset_y:roi_rows_end, offset_x:roi_cols_end] = fg

    cv2.destroyAllWindows()

    return background


def resize_fit(image: np.array, max_width: int, max_height: int) -> np.array:
    height, width, channels = image.shape

    print("Max: ", max_width, max_height)
    print("Actual: ", width, height)

    scale_width = max_width / width
    scale_height = max_height / width

    print("Scale: ", scale_width, scale_height)

    final_scale = scale_width

    if scale_width > scale_height:
        final_scale = scale_height

    res = cv2.resize(image, None, fx=final_scale, fy=final_scale, interpolation=cv2.INTER_CUBIC)

    res_width, res_height, res_channels = res.shape

    print("Final: ", res_width, res_height)

    return res
