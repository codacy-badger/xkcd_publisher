import sys

import requests


def download_image(image_url, saved_image_location):
    response = requests.get(image_url)
    if response.ok:
        with open(saved_image_location, "wb") as image_file:
            image_file.write(response.content)


def get_file_extension(url):
    filename = url.split('/')[-1]
    file_extension = filename.split('.')[-1]
    return file_extension


def fetch_comic_url(json_url):
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()["img"]


def main():
    json_url = "https://xkcd.com/353/info.0.json"
    comic_url = fetch_comic_url(json_url)
    if not comic_url:
        sys.exit('Problem with getting a link to a comic')
    saved_image_location = 'comic.{}'.format(get_file_extension(comic_url))
    download_image(comic_url, saved_image_location)


if __name__ == "__main__":
    main()
