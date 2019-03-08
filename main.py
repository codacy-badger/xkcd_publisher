import os
from logging import config, getLogger

from post_vkontakte import post_vkontakte
import xkcd
import tools

config.fileConfig(fname="logger.cfg", disable_existing_loggers=False)
logger = getLogger(__file__)


def main():
    logger.info("Download a random comic...")

    random_comic_url = xkcd.fetch_random_comic_url("https://xkcd.com/info.0.json")
    image_comic_url = xkcd.fetch_comic_image_url(random_comic_url)
    file_extension = tools.get_file_extension(image_comic_url)
    saved_image_location = f"comic.{file_extension}"
    tools.download_image(image_comic_url, saved_image_location)

    logger.info("Upload the comic to the group...")

    post_vkontakte(
        xkcd.fetch_author_comment(random_comic_url),
        saved_image_location,
    )

    logger.info("The comic is successfully uploaded to the group!")

    os.remove(saved_image_location)


if __name__ == "__main__":
    main()
