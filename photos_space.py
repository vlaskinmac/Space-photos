import os

import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_container_links(url):
    data = {"api_key": token}
    response = requests.get(url, params=data)
    response.raise_for_status()
    return response.json()


def fetch_spacex_last_launch(dir_name):
    container_links = get_container_links(url=url_archive)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    file_path = os.path.abspath(dir_name)
    for image_url_number, image_url in enumerate(container_links):
        data = {"api_key": token}
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/" \
                    f"{year}/{month}/{day}/png/{image_url['image']}.png"
        response_image = requests.get(url_image, params=data)
        response_image.raise_for_status()

        cut_path_url = urlparse(url_image)
        name_file_url = os.path.split(cut_path_url.path)
        tail_url = os.path.splitext(name_file_url[-1])[-1]
        with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
            file.write(response_image.content)
            print(f"{image_url_number + 1} - картинка загружена")


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("API_KEY_NASA")
    dirname = "NASA_images"
    year = "2021"
    month = "07"
    day = "03"
    url_archive = f"https://api.nasa.gov/EPIC/api/natural/date/{year}-{month}-{day}"
    fetch_spacex_last_launch(dir_name=dirname)


