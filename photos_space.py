from pprint import pprint

import requests
import os
from urllib.parse import urlparse


def get_container_links(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr_images']


def fetch_spacex_last_launch(dir_name):
    container_links = get_container_links(url=url)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    file_path = os.path.abspath(dir_name)
    for image_url_number, image_url in enumerate(container_links):
        response_image = requests.get(image_url)
        response_image.raise_for_status()
        filename = f"{urlparse(image_url).path.split('/')[-2]}.jpg"
        with open(f"{file_path}/{filename}", "wb") as file:
            file.write(response_image.content)
            print(f"{image_url_number + 1} - картинка загружена")

    # url_link = f"{url}/{parsed_link.netloc}{parsed_link.path}"
    # print(parsed_link)
    # print(parsed_link.path.split('/')[-2])


if __name__ == "__main__":
    dirname = "images"
    url = "https://api.spacexdata.com/v3/launches/55"
    fetch_spacex_last_launch(dir_name=dirname)
