#!/usr/bin/python

import sys
from math import cos, floor


LATITUDE = -37.852
LONGITUDE = 144.752


PIXELS_PER_KM = 0.25

# Functions for lat/long -> (x, y) conversion for 64km Melbourne radar image
# Radar image is centered at lat_center, lon_center
# Location being queries is lat, lon
# Logic devired by reverse engineering methods in http://www.bom.gov.au/scripts/radar/IDR.loop.v12.0.js


def get_image_y(lat_center, lat):
    # Calculate the distance (in km) between lat and lat_center
    return 1.1111 * 100 * (lat - lat_center)


def get_image_x(lon_center, lon, lat):
    # Calculate the distance (in km) between lon and lon_center
    return 1.1111 * 100 * cos(100 * lat / 5729) * (lon - lon_center)

def get_image_coordinates(lat, lon):
    # For a given location, return the pixel coordinates on the Melbourne radar image
    # Arguments:
    # - lat (float): the latitude of the arugment location
    # - lon (float): the longitude of the argument location
    #
    # Returns:
    # (int, int) coordinates of the location on the image

    x_delta_km = get_image_x(LONGITUDE, lon, lat)
    y_delta_km = get_image_y(LATITUDE, lat)

    x = int(floor(256 + x_delta_km / PIXELS_PER_KM))
    y = int(floor(256 - y_delta_km / PIXELS_PER_KM))

    return (x, y)


if __name__ == '__main__':
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])

    coords = get_image_coordinates(latitude, longitude)

    print 'You are at exactly (x, y) of (%s, %s) on the radar image' % coords
