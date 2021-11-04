import urllib
from pprint import pprint

import requests
import os
from urllib.parse import urlparse


def get_container_links(url):
    API_KEY = "xFuLodNSHjwSREoFpnsTKYZnjBbdHKd2UJxShsWa"
    start_date = "2021-10-01"
    data = {"api_key": API_KEY, "start_date": start_date}
    response = requests.get(url, params=data)
    response.raise_for_status()
    return response.json()


def fetch_spacex_last_launch(dir_name):
    container_links = get_container_links(url=url)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    file_path = os.path.abspath(dir_name)
    for image_url_number, image_url in enumerate(container_links):
        if image_url["media_type"] == "image":
            response_image = requests.get(image_url["url"])
            response_image.raise_for_status()
            cut_path_url = urlparse(image_url["url"])
            name_file_url = os.path.split(cut_path_url.path)
            tail_url = os.path.splitext(name_file_url[-1])[-1]
            with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
                file.write(response_image.content)
                print(f"{image_url_number + 1} - картинка загружена")


if __name__ == "__main__":
    dirname = "images"
    url = "https://api.nasa.gov/planetary/apod"
    fetch_spacex_last_launch(dir_name=dirname)


def get_extention_image(url):
    API_KEY = "xFuLodNSHjwSREoFpnsTKYZnjBbdHKd2UJxShsWa"
    start_date = "2021-10-01"
    data = {"api_key": API_KEY, "start_date": start_date}
    response = requests.get(url, params=data)
    response.raise_for_status()
    url_image = response.json()
    for item in url_image:
        if item["media_type"] == "image":
            print(item["url"])
    # cut_path_url = urlparse(url_image).path
    # name_file_url = os.path.split(cut_path_url)
    # name_file = urllib.parse.unquote(os.path.splitext(name_file_url[1])[0], encoding='utf-8', errors='replace')
    # print(name_file)
    # print(os.path.splitext(name_file_url[-1])[-1])


    # return response.json()['links']['flickr_images']

# url = "https://api.nasa.gov/planetary/apod"
# url = "https://example.com/txt/hello%20world.txt?v=9#python"
# print(os.path.splitext(url))
# print(os.path.split(url))
# print(urlparse(url))
# print()
# x = urlparse(url).path
# y = os.path.split(x)
# print(os.path.split(x))
# p=os.path.splitext(y[1])
# print(p[0])
# print()
# t = urllib.parse.unquote(os.path.splitext(y[1])[0], encoding='utf-8', errors='replace')
# print(t)
# print(os.path.splitext(y[-1]))
# print(os.path.splitext(y[-1])[-1])
# get_extention_image(url=url)