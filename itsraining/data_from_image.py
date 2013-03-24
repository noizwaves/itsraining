import png
import sys

RAINFALL_LEGEND = [
    (0, (0, 0, 0, 0)),
    (1, (245, 245, 255, 255)),
    (2, (180, 180, 255, 255)),
    (3, (120, 120, 255, 255)),
    (4, (20, 20, 255, 255)),
    (5, (0, 216, 195, 255)),
    (6, (0, 150, 144, 255)),
    (7, (0, 102, 102, 255)),
    (8, (255, 255, 0, 255)),
    (9, (255, 200, 0, 255)),
    (10, (255, 150, 0, 255)),
    (11, (255, 100, 0, 255)),
    (12, (255, 0, 0, 255)),
    (13, (200, 0, 0, 255)),
    (14, (120, 0, 0, 255)),
    (15, (40, 0, 0, 255)),
]

# convert to VALUE_MAP for value lookup via colour
VALUE_MAP = dict([(c, v) for v, c in RAINFALL_LEGEND])

# ignore these pixels when extracting rainfall values
STANDARD_HEIGHT = 512
STANDARD_WIDTH = 512
HEADER_HEIGHT = 16
FOOTER_HEIGHT = 16


# Extract the rainfall values (as a 2D array, indexed via [x,y]) from a
# standard radar image
def extract_values(filename):
    """
    Extract the rainfall values (as a 2D array, indexed via [x,y]) from a
    standard radar image. Raw data is returned from the image (ie. the header
    and footer areas are removed).
    """

    # load filename
    reader = png.Reader(filename=filename)
    w, h, pixels, metadata = reader.read_flat()
    palette = metadata['palette']
    assert w == STANDARD_WIDTH, 'filename not expected width (%s pixels)' % \
        STANDARD_WIDTH
    assert h == STANDARD_HEIGHT, 'filename not expected height (%s pixels)' % \
        STANDARD_HEIGHT

    # dimensions of our output
    num_rows = w
    num_cols = h - HEADER_HEIGHT - FOOTER_HEIGHT
    values = [[0] * num_cols] * num_rows

    # iterate over data in image, map to rainfall value
    for i in range(HEADER_HEIGHT, h - FOOTER_HEIGHT):
        for j in range(0, w):
            point = (j, i)  # format of (x, y) in the raw data space
            position = get_pixel_position(point[0], point[1], w)
            colour = palette[pixels[position]]
            value = VALUE_MAP[colour]

            target_x, target_y = (j, i - HEADER_HEIGHT)
            values[target_x][target_y] = value

    return values


def get_pixel_position(x, y, w):
    return x + y * w


def get_rainfall_at(filename, x, y):
    """
    Obtain the rainfall value of a given pixel

    Arguments:
    - filename (string): path to a given radar image
    - x (int): x pixel coordinate on the radar image
    - y (int): y pixel coordinate on the radar image

    Returns: (float) representing current rainfall
    """

    values = extract_values(filename)

    # convert pixel coordinate into raw value coordinate
    y -= HEADER_HEIGHT
    # no change to x coord

    return values[x][y]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print extract_values(sys.argv[1])
    if len(sys.argv) == 4:
        filename = sys.argv[1]
        x = int(sys.argv[2])
        y = int(sys.argv[3])
        print get_rainfall_at(filename, x, y)
