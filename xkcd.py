from random import randint

import requests


def fetch_random_comic_json_url(url_current_comic):
    response = requests.get(url_current_comic)
    if response.status_code == 200:
        count_of_comics = response.json()["num"]
        return "http://xkcd.com/{}/info.0.json".format(randint(1, count_of_comics))


def fetch_comic_image_url(comic_json_url):
    response = requests.get(comic_json_url)
    if response.status_code == 200:
        return response.json()["img"]


def fetch_author_comment(json_url):
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()["alt"]