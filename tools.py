import requests


def download_image(image_url, saved_image_location):
    response = requests.get(image_url)
    if response.ok:
        with open(saved_image_location, "wb") as image_file:
            image_file.write(response.content)


def get_file_extension(url):
    filename = url.split("/")[-1]
    file_extension = filename.split(".")[-1]
    return file_extension
