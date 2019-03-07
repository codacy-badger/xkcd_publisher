from random import randint

import requests


def fetch_random_comic_json_url(url_last_comic):
    response = requests.get(url_last_comic)
    if response.ok:
        count_of_comics = response.json()["num"]
        return f"http://xkcd.com/{randint(1, count_of_comics)}/info.0.json"


def fetch_comic_image_url(comic_url):
    response = requests.get(comic_url)
    if response.ok:
        return response.json()["img"]


def fetch_author_comment(comic_url):
    response = requests.get(comic_url)
    if response.ok:
        return response.json()["alt"]
