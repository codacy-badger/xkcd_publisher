import requests

VERSION_API = 5.92


def get_address_to_upload_photo(token, version_api=VERSION_API):
    vk_api_url = "https://api.vk.com/method/"
    method_name = "photos.getWallUploadServer"
    search_params = {"access_token": token, "v": version_api}
    response = requests.get(
        f"{vk_api_url}{method_name}", params=search_params
    )
    try:
        return response.json()["response"]["upload_url"]
    except KeyError:
        return response.json()["error"]["error_code"]


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
    response = requests.post(
        f"{vk_api_url}{method_name}", params=search_params
    )
    return response.json()


def publish_image_on_wall(
        token, owner_id, from_group, attachments, message, version_api=VERSION_API
):
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
