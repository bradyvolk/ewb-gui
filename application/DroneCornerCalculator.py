import numpy as np
import math


def calculate_corners(gps_coordinate, orientation, rel_height, camera_angle):
    """
    gps_coordinate - tuple - tuple of gps coordinate of drone
    orientation - float - orientation clockwise from north in degrees
    rel_height - float - height of the drone relative to ground in meters
    camera_angle - tuple - the angle of the camera, how much it flares out in degrees for (x, y)
    """
    half_x_of_image = math.tan(math.radians(
        camera_angle[0])) * rel_height    # = rel_height
    half_y_of_image = math.tan(math.radians(
        camera_angle[1])) * rel_height    # = rel_height
    print(half_x_of_image, half_y_of_image)

    # degrees over meters conversion
    alpha = 0.00001 / 1.11

    half_x_of_image *= alpha
    half_y_of_image *= alpha

    distance_to_corner = math.sqrt(
        half_x_of_image**2 + half_y_of_image**2)  # = rel_height * sqrt(2)
    print(distance_to_corner)

    # determine case for arctan
    temp = orientation % 180            # = 90
    first_angle = orientation % 90      # = 0

    if (temp < 45 or temp > 135):
        third_angle = math.degrees(
            math.atan(half_x_of_image / half_y_of_image))
    else:
        third_angle = math.degrees(
            math.atan(half_y_of_image / half_x_of_image))

    if (first_angle < 45):
        second_angle = 90 - first_angle - third_angle
    else:
        second_angle = first_angle - third_angle

    lat = distance_to_corner * math.cos(math.radians(second_angle))  # 1
    lon = distance_to_corner * math.sin(math.radians(second_angle))

    print(lat, lon)

    if (orientation < 90):
        tr = (lat, lon)
        br = ((-1) * lon, lat)
        bl = ((-1) * lat, (-1) * lon)
        tl = (lon, (-1) * lat)
    elif (orientation < 180):
        br = (lat, lon)
        tr = (lon, (-1) * lat)
        bl = ((-1) * lat, lon)
        tl = ((-1) * lon, (-1) * lat)
    elif (orientation < 270):
        bl = (lat, lon)
        tl = (lat + 2 * half_y_of_image, lon)
        tr = (lat + 2 * half_y_of_image, lon + 2 * half_x_of_image)
        br = (lat, lon + 2 * half_x_of_image)
    else:
        tl = (lat, lon)
        bl = (lat - 2 * half_y_of_image, lon)
        br = (lat - 2 * half_y_of_image, lon + 2 * half_x_of_image)
        tr = (lat, lon + 2 * half_x_of_image)

    tl = (gps_coordinate[0] + tl[0], gps_coordinate[1] + tl[1])
    tr = (gps_coordinate[0] + tr[0], gps_coordinate[1] + tr[1])
    bl = (gps_coordinate[0] + bl[0], gps_coordinate[1] + bl[1])
    br = (gps_coordinate[0] + br[0], gps_coordinate[1] + br[1])
    print(bl, tl, br, tr)

    return [bl, tl, br, tr]


calculate_corners((20, 20), 10, 110000, (45, 45))
