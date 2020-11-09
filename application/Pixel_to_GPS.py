import numpy as np


def pixel_to_GPS(image, H, W, tl, tr, bl):
    GPS_coords = np.zeros((H, W))
    GPS_coords[0][0] = tl
    GPS_coords[0][W-1] = tr
    GPS_coords[H-1][0] = bl
    GPS_coords = fill_array(GPS_coords, H, W, tl, tr, bl)
    return GPS_coords


def fill_array(GPS_coords, H, W, tl, tr, bl):
    bl_x, bl_y = bl
    tr_x, tr_y = tr
    tl_x, tl_y = tl

    slope1x = (tr_x - tl_x) / W  # How much to increment x by for line 1
    slope2y = (bl_y - tl_y) / H  # How much to incrememnt y by for line 2

    slope1 = (tr_y-tl_y) / (tr_x - tl_x)  # Slope of Line 1
    slope2 = (bl_x-tl_x) / (bl_y-tl_y)  # Slope of Line 2

    for i in range(W-1):
        x_scaled = slope1x*i
        GPS_coords[0][i] = (x_scaled, x_scaled*slope1)
        GPS_coords[H-1][i] = (bl_x + x_scaled, bl_y + (x_scaled*slope1))

    for j in range(H-1):
        y_scaled = slope2y*j
        GPS_coords[j][0] = (y_scaled*slope2, y_scaled)
        GPS_coords[j][W-1] = (tr_x + (y_scaled*slope2), tr_y + y_scaled)

    for z in range(H-1):
        x, y = GPS_coords[z][0]
        for i in range(W-1):
            x_scaled = slope1x*i
            GPS_coords[z][i] = (x + x_scaled, y + (x_scaled*slope1))

    return GPS_coords
