import os
import sys
from random import randint

import requests
from requests.exceptions import ConnectionError, HTTPError

from logging import config, getLogger

URL_LAST_COMIC = "https://xkcd.com/info.0.json"

config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
logger = getLogger(__file__)


def download_image(image_url, saved_image_location):
    response = requests.get(image_url)
    if response.ok:
        with open(saved_image_location, "wb") as image_file:
            image_file.write(response.content)


def get_file_extension(url):
    filename = url.split("/")[-1]
    file_extension = filename.split(".")[-1]
    return file_extension


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
        response.raise_for_status()
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.error(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        return response.json()["img"]


def fetch_author_comment():
    # TODO поменять комментарии
    try:
        comic_url = fetch_random_comic_url(URL_LAST_COMIC)
        response = requests.get(comic_url)
        response.raise_for_status()
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.error(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        return response.json()["alt"]


def download_image_comic():
    random_comic_url = fetch_random_comic_url(URL_LAST_COMIC)
    image_comic_url = fetch_comic_image_url(random_comic_url)
    file_extension = get_file_extension(image_comic_url)
    saved_image_location = f"comic.{file_extension}"
    download_image(image_comic_url, saved_image_location)


def get_saved_image_location():
    image_extension = [
        'bmp',
        'jpeg',
        'jpg',
        'png',
    ]

    files = os.listdir(os.getcwd())
    for filename in files:
        if get_file_extension(filename) in image_extension:
            return os.path.abspath(filename)