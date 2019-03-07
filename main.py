import os
from logging import config, getLogger

from dotenv import load_dotenv

import post_vkontakte
import tools
import xkcd

VERSION_API = 5.92

config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
logger = getLogger(__file__)


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")

    logger.info("Download a random comic...")

    url_last_comic = "https://xkcd.com/info.0.json"
    random_comic_url = xkcd.fetch_random_comic_json_url(url_last_comic)
    image_comic_url = xkcd.fetch_comic_image_url(random_comic_url)
    file_extension = tools.get_file_extension(image_comic_url)
    saved_image_location = f"comic.{file_extension}"
    tools.download_image(image_comic_url, saved_image_location)
    author_comment = xkcd.fetch_author_comment(random_comic_url)

    logger.info("Upload the comic to the group...")
    address_to_upload_photo = post_vkontakte.get_address_to_upload_photo(token)
    response_upload_image_on_server_vk = post_vkontakte.upload_image_on_server_vk(
        "comic.png", address_to_upload_photo,
    )
    server_id_vk = response_upload_image_on_server_vk["server"]
    uploaded_image_data = response_upload_image_on_server_vk["photo"]
    hash_image = response_upload_image_on_server_vk["hash"]

    response_save_uploaded_image = post_vkontakte.save_uploaded_image(
        token, server_id_vk, uploaded_image_data, hash_image,
    )
    owner_id = response_save_uploaded_image["response"][0]["owner_id"]
    image_id = response_save_uploaded_image["response"][0]["id"]
    attachments = f"photo{owner_id}_{image_id}"

    group_id = "179225771"
    post_vkontakte.publish_image_on_wall(
        token,
        f"-{group_id}",
        1,
        attachments,
        author_comment,
        version_api=VERSION_API,
    )
    logger.info("The comic is successfully uploaded to the group!")
    os.remove(saved_image_location)


if __name__ == "__main__":
    main()
