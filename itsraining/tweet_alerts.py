#!/usr/bin/python
# Sends a tweet to a recipient if it's raining at specific locations

import re
from tempfile import gettempdir
from os import path, listdir
from urllib import urlopen, urlretrieve

from twitter import Twitter, OAuth

from lat_long_to_pixels import get_image_coordinates
from data_from_image import get_rainfall_at


RADAR_PREFIX = 'IDR024'
RADAR_PAGE_URL = 'http://www.bom.gov.au/products/IDR024.loop.shtml'
RADAR_IMAGE_HOST = 'http://www.bom.gov.au'
RE_IMAGE_URL = re.compile('^theImageNames\[[0-5]\]\s=\s\"(.*?)\";$')

OAUTH_TOKEN = None
OAUTH_SECRET = None
CONSUMER_KEY = None
CONSUMER_SECRET = None

# Tweet alert at this twitter account
TWEET_RECIPIENT = None
# Check these locations for rain activity
LOCATIONS = [
    ('York Butter Factory', -37.818705, 144.956988),
    ('Inspire9', -37.823957, 144.991105),
]


def update_radar_images():
    """
    Ensures that we locally have a copy of the latest radar image
    """

    # Download the radar webpage
    html = urlopen(RADAR_PAGE_URL)

    # Match lines '''theImageNames[0] = "/radar/IDR024.T.201302280718.png";'''
    image_urls = list()
    for line in html:
        match = RE_IMAGE_URL.match(line)
        if match:
            rel_url = match.groups()[0]
            image_urls.append(RADAR_IMAGE_HOST + rel_url)

    # Order by timestamp descending
    image_urls.sort(reverse=True)

    # Download newest image to tempdir
    newest_file = image_urls[0].split('/')[-1]
    dest_path = path.join(gettempdir(), newest_file)
    if not path.exists(dest_path):
        print "Downloading '%s'" % dest_path
        urlretrieve(image_urls[0], dest_path)


def get_latest_image():
    # Returns the path of the newest radar image available

    all_images = [f for f in listdir(gettempdir()) if f.startswith(RADAR_PREFIX)]
    all_images.sort(reverse=True)

    image_path = path.join(gettempdir(), all_images[0])

    return image_path


def compose_alert(location, alertee, rainfall):
    """
    Compose and send an alert for a rainfall event
    """

    msg = "%s It's raining at %s now" % (alertee, location[0])

    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
    t.statuses.update(status=msg)


def send_rain_warning(location, alertee):
    """
    Sends a current raining warning to an alertee if it's raining at the given location
    Arguments:
    - location (3-tuple): of label, latitude, longitude)
    - alertee (string): twitter handle of alert recipient
    """

    update_radar_images()
    latest_image = get_latest_image()

    coords = get_image_coordinates(location[1], location[2])
    rainfall = get_rainfall_at(latest_image, coords[0], coords[1])

    if rainfall > 0:
        compose_alert(location, alertee, rainfall)


def assert_defaults_set():
    """Ensures that certain variables are populated at run time."""

    if TWEET_RECIPIENT is None:
        print 'Value for TWEET_RECIPIENT is not set'
        exit(-1)

    if None in [OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET]:
        print 'Values for twitter access (OAUTH_* and CONSUMER_*) is not set'
        exit(-1)


if __name__ == '__main__':
    assert_defaults_set()

    alertee = TWEET_RECIPIENT
    locations = LOCATIONS

    for location in locations:
        send_rain_warning(location, alertee)
