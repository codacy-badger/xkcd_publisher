import os
from logging import config, getLogger

from post_vkontakte import post_vkontakte
from xkcd import (
    download_image_comic,
    fetch_author_comment,
    get_saved_image_location,
)


def main():
    config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
    logger = getLogger(__file__)

    logger.info("Download a random comic...")

    download_image_comic(logger)

    logger.info("Upload the comic to the group...")
    saved_image_location = get_saved_image_location()

    post_vkontakte(
        fetch_author_comment(logger),
        saved_image_location,
    )

    logger.info("The comic is successfully uploaded to the group!")

    os.remove(saved_image_location)


if __name__ == "__main__":
    main()
