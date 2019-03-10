import os
from logging import config, getLogger

from post_vkontakte import post_vkontakte
from xkcd import download_image_comic, fetch_author_comment, get_saved_image_location

config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
logger = getLogger(__file__)


def main():
    logger.info("Download a random comic...")

    download_image_comic()
    saved_image_location = get_saved_image_location()

    logger.info("Upload the comic to the group...")

    author_comment = fetch_author_comment()
    post_vkontakte(
        author_comment,
        saved_image_location,
    )

    logger.info("The comic is successfully uploaded to the group!")

    os.remove(saved_image_location)


if __name__ == "__main__":
    main()
