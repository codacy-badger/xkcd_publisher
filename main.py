import os
import sys
from random import randint

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
    return response.json()


def save_uploaded_image(token, server_id_vk, uploaded_photo_data, hash_image, version_api=VERSION_API):
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


def publish_image_on_wall(token, owner_id, from_group, attachments, message, version_api=VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = 'wall.post'
    search_params = {
        "owner_id": owner_id,
        "from_group": from_group,
        "attachments": attachments,
        "message": message,
        "access_token": token,
        "v": version_api,

    }
    response = requests.get("{}{}".format(vk_api_url, method_name), params=search_params)
    return response.json()


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")

    json_url = "https://xkcd.com/info.0.json"
    random_comic_json_url = fetch_random_comic_json_url(json_url)
    image_comic_url = fetch_comic_image_url(random_comic_json_url)
    if not image_comic_url:
        sys.exit("Problem with getting a link to a comic")

    saved_image_location = "comic.{}".format(get_file_extension(image_comic_url))
    download_image(image_comic_url, saved_image_location)

    author_comment = fetch_author_comment(random_comic_json_url)
    if not author_comment:
        sys.exit("Could not get author's comment.")

    address_to_upload_photo = get_address_to_upload_photo(token)

    response_upload_image_on_server_vk = upload_image_on_server_vk("comic.png", address_to_upload_photo)
    server_id_vk = response_upload_image_on_server_vk["server"]
    uploaded_image_data = response_upload_image_on_server_vk["photo"]
    hash_image = response_upload_image_on_server_vk["hash"]

    response_save_uploaded_image = save_uploaded_image(token, server_id_vk, uploaded_image_data, hash_image)
    owner_id = response_save_uploaded_image["response"][0]["owner_id"]
    image_id = response_save_uploaded_image["response"][0]["id"]
    attachments = "photo{}_{}".format(owner_id, image_id)

    group_id = '179225771'
    response_publish = publish_image_on_wall(
        token,
        "-{}".format(group_id),
        True,
        attachments,
        author_comment,
        version_api=VERSION_API,
    )
    print(response_publish)
    os.remove(saved_image_location)


if __name__ == "__main__":
    main()
