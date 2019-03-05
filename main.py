import os
import sys

import requests
from dotenv import load_dotenv

VERSION_API = 5.92


def download_image(image_url, saved_image_location):
    response = requests.get(image_url)
    if response.ok:
        with open(saved_image_location, "wb") as image_file:
            image_file.write(response.content)


def get_file_extension(url):
    filename = url.split("/")[-1]
    file_extension = filename.split(".")[-1]
    return file_extension


def fetch_comic_url(json_url):
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()["img"]


def fetch_author_comment(json_url):
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()["alt"]


def get_address_to_upload_photo(token, version_api=VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = 'photos.getWallUploadServer'
    search_params = {
        "access_token": token,
        "v": version_api,

    }
    response = requests.get("{}{}".format(vk_api_url, method_name), params=search_params)
    try:
        return response.json()["response"]["upload_url"]
    except KeyError:
        return response.json()["error"]["error_code"]


def upload_image_on_server_vk(photo, address_to_upload_photo):
    image_file_descriptor = open(photo, 'rb')
    files = {'photo': (photo, image_file_descriptor)}
    response = requests.post(address_to_upload_photo, files=files)
    image_file_descriptor.close()
    return response.json()["server"], response.json()["photo"], response.json()["hash"]


def save_uploaded_image(token, server_id_vk, uploaded_photo_data, hash_image, version_api = VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = 'photos.saveWallPhoto'
    search_params = {
        "photo": uploaded_photo_data,
        "server": server_id_vk,
        "hash": hash_image,
        "access_token": token,
        "v": version_api,

    }
    response = requests.post("{}{}".format(vk_api_url, method_name), params=search_params)
    return response.json()


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")

    json_url = "https://xkcd.com/353/info.0.json"
    comic_url = fetch_comic_url(json_url)
    if not comic_url:
        sys.exit("Problem with getting a link to a comic")

    saved_image_location = "comic.{}".format(get_file_extension(comic_url))
    download_image(comic_url, saved_image_location)

    author_comment = fetch_author_comment(json_url)
    if not author_comment:
        sys.exit("Could not get author's comment.")

    address_to_upload_photo = get_address_to_upload_photo(token)
    server_id_vk, uploaded_image_data, hash_image = upload_image_on_server_vk("comic.png", address_to_upload_photo)
    print(save_uploaded_image(token, server_id_vk, uploaded_image_data, hash_image))


if __name__ == "__main__":
    main()
