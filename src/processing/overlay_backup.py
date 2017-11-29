def apply_overlay(overlay, face, offset_x, offset_y):
    cv2.imshow('out', overlay)
    cv2.waitKey(0)

    rows_fg, cols_fg, channels_fg = face.shape
    rows_overlay, cols_bg, channels_bg = overlay.shape

    if (offset_x < -100) or (offset_x < -100):
        raise ValueError('offset more than 100%')

    # negative numbers from -100 to 1 are percentage offsets
    if offset_y < 0:
        offset_y_percentage = offset_y * -0.01
        offset_y = int((rows_overlay - rows_fg) * offset_y_percentage)

    if offset_x < 0:
        offset_x_percentage = offset_x * -0.01
        offset_x = int((cols_bg - cols_fg) * offset_x_percentage)

    if (rows_fg > rows_overlay) or (cols_fg > cols_bg):
        raise ValueError('Overlay bigger than background')

    if ((offset_y + rows_fg) > rows_overlay) or ((offset_x + cols_fg) > cols_bg):
        raise ValueError('offset too big')

    roi_rows_end = offset_y + rows_fg
    roi_cols_end = offset_x + cols_fg

    face_face = cv2.bitwise_and(face, face)

    final = overlay

    black_region = np.zeros((roi_rows_end - offset_y, roi_cols_end - offset_x, 3), np.uint8)

    dst = cv2.add(black_region, face_face)

    final[offset_y:roi_rows_end, offset_x:roi_cols_end] = dst

    return final