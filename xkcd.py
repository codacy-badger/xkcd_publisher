import os
import sys
from secrets import SystemRandom

import requests
from requests.exceptions import ConnectionError, HTTPError

URL_LAST_COMIC_DATA = "https://xkcd.com/info.0.json"


def download_image(image_url, saved_image_location, logger):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.critical(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        with open(saved_image_location, "wb") as image_file:
            image_file.write(response.content)


def get_file_extension(url):
    filename = url.split("/")[-1]
    file_extension = filename.split(".")[-1]
    return file_extension


def fetch_random_comic_url(url_last_comic_data, logger):
    try:
        response = requests.get(url_last_comic_data)
        response.raise_for_status()
    except ConnectionError:
        logger.critical("It seems the xkcd.com is not available")
        sys.exit(1)
    except HTTPError as error:
        logger.critical(f"HTTP error occurred: {error}")
        sys.exit(1)
    else:
        count_of_comics = response.json()["num"]
        return f"http://xkcd.com/{SystemRandom().randrange(1, count_of_comics)}/info.0.json"


def fetch_comic_image_url(comic_url, logger):
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


def fetch_author_comment(logger):
    try:
        comic_url = fetch_random_comic_url(URL_LAST_COMIC_DATA, logger)
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


def download_image_comic(logger):
    random_comic_url = fetch_random_comic_url(URL_LAST_COMIC_DATA, logger)
    image_comic_url = fetch_comic_image_url(random_comic_url, logger)
    file_extension = get_file_extension(image_comic_url)
    saved_image_location = f"comic.{file_extension}"
    download_image(image_comic_url, saved_image_location, logger)


def get_saved_image_location():
    image_extension = [
        "bmp",
        "jpeg",
        "jpg",
        "png",
    ]

    files_of_project = os.listdir(os.getcwd())
    for file_of_project in files_of_project:
        if get_file_extension(file_of_project) in image_extension:
            return os.path.abspath(file_of_project)
