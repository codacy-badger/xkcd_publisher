import os
import sys
from logging import config, getLogger

import requests
from dotenv import load_dotenv

VERSION_API = 5.92


def print_error_message(json_schema, logger):
    error_code = json_schema["error"]["error_code"]
    error_message = json_schema["error"]["error_msg"]
    logger.error(f"{error_code} - {error_message}")


def get_address_to_upload_photo(token, version_api=VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = "photos.getWallUploadServer"
    search_params = {"access_token": token, "v": version_api}
    return requests.get(
        f"{vk_api_url}{method_name}",
        params=search_params,
    ).json()


def upload_image_on_server_vk(photo, address_to_upload_photo):
    image_file_descriptor = open(photo, "rb")
    files = {"photo": (photo, image_file_descriptor)}
    response = requests.post(address_to_upload_photo, files=files)
    image_file_descriptor.close()
    return response.json()


def save_uploaded_image(
        token, server_id_vk, uploaded_photo_data, hash_image, version_api=VERSION_API
):
    vk_api_url = "https://api.vk.com/method/"
    method_name = "photos.saveWallPhoto"
    search_params = {
        "photo": uploaded_photo_data,
        "server": server_id_vk,
        "hash": hash_image,
        "access_token": token,
        "v": version_api,
    }
    return requests.post(
        f"{vk_api_url}{method_name}", params=search_params
    ).json()


def publish_image_on_wall(token, owner_id, from_group, attachments, message, version_api=VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = "wall.post"
    search_params = {
        "owner_id": owner_id,
        "from_group": from_group,
        "attachments": attachments,
        "message": message,
        "access_token": token,
        "v": version_api,
    }
    response = requests.get(
        f"{vk_api_url}{method_name}", params=search_params
    )
    return response.json()


def post_vkontakte(fetch_author_comment, saved_image_location):
    config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
    logger = getLogger("post_vkontakte.py")

    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")

    if not token:
        logger.critical("write the token in .env file")
        sys.exit(1)

    response_get_address_to_upload_photo = get_address_to_upload_photo(token)

    if not response_get_address_to_upload_photo.get("response"):
        print_error_message(response_get_address_to_upload_photo, logger)
        sys.exit(1)
    address_to_upload_photo = response_get_address_to_upload_photo["response"]["upload_url"]

    response_upload_image_on_server_vk = upload_image_on_server_vk(
        saved_image_location, address_to_upload_photo,
    )
    server_id_vk = response_upload_image_on_server_vk["server"]
    uploaded_image_data = response_upload_image_on_server_vk["photo"]
    hash_image = response_upload_image_on_server_vk["hash"]

    response_save_uploaded_image = save_uploaded_image(
        token, server_id_vk, uploaded_image_data, hash_image,
    )

    if not response_save_uploaded_image.get("response"):
        print_error_message(response_save_uploaded_image, logger)
        sys.exit(1)

    owner_id = response_save_uploaded_image["response"][0]["owner_id"]
    image_id = response_save_uploaded_image["response"][0]["id"]
    attachments = f"photo{owner_id}_{image_id}"

    json_schema_publish_image_on_wall = publish_image_on_wall(
        token,
        f"-{group_id}",
        1,
        attachments,
        fetch_author_comment,
        version_api=VERSION_API,
    )

    if not json_schema_publish_image_on_wall.get("response"):
        print_error_message(response_save_uploaded_image, logger)
        sys.exit(1)
