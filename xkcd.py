import sys
from random import randint

import requests
from requests.exceptions import ConnectionError, HTTPError

from logging import config, getLogger

config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
logger = getLogger(__file__)


def fetch_random_comic_url(url_last_comic):
    try:
        response = requests.get(url_last_comic)
        response.raise_for_status()
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.error(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        count_of_comics = response.json()["num"]
        return f"http://xkcd.com/{randint(1, count_of_comics)}/info.0.json"


def fetch_comic_image_url(comic_url):
    # TODO поменять комментарии
    try:
        response = requests.get(comic_url)
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.error(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        return response.json()["img"]


def fetch_author_comment(comic_url):
    # TODO поменять комментарии
    try:
        response = requests.get(comic_url)
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.error(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        return response.json()["alt"]
