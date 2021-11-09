import argparse
import datetime
import logging
import os
import random
import time
import urllib
from urllib.parse import urlparse

import requests
import telegram

from dotenv import load_dotenv
from telegram import TelegramError


def get_container_links(url, token):
    data = {"api_key": token}
    response = requests.get(url, params=data)
    response.raise_for_status()
    logging.warning(response.status_code)
    return response.json()


def get_file_path(dir_name):
    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.abspath(dir_name)
    return file_path


def get_apod_images(token):
    dirname = "apod"
    url = "https://api.nasa.gov/planetary/apod"
    container_links = get_container_links(url=url, token=token)
    file_path = get_file_path(dir_name=dirname)
    for image_url_number, image_url in enumerate([container_links]):
        if image_url["media_type"] == "image":
            response_image = requests.get(image_url["url"])
            response_image.raise_for_status()
            logging.warning(response_image.status_code)
            cut_path_url = urlparse(image_url["url"])
            cut_path_clean = urllib.parse.unquote(cut_path_url.path)
            name_file_url = os.path.split(cut_path_clean)
            tail_url = os.path.splitext(name_file_url[-1])[-1]
            with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
                file.write(response_image.content)


def fetch_spacex_last_launch(token):
    dirname = "last_launch"
    url = "https://api.spacexdata.com/v3/launches/55"
    container_links = get_container_links(url=url, token=token)
    file_path = get_file_path(dir_name=dirname)
    for image_url_number, image_url in enumerate(container_links["links"]["flickr_images"]):
        response_image = requests.get(image_url)
        response_image.raise_for_status()
        logging.warning(response_image.status_code)
        cut_path_url = urlparse(image_url)
        cut_path_clean = urllib.parse.unquote(cut_path_url.path)
        name_file_url = os.path.split(cut_path_clean)
        tail_url = os.path.splitext(name_file_url[-1])[-1]
        with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
            file.write(response_image.content)


def get_earth_images(url_archive, token, year, month, day):
    dirname = "earth"
    container_links = get_container_links(url=url_archive, token=token)
    if not container_links:
        logging.warning("Нет данных")
        print("Нет данных")
        exit()
    file_path = get_file_path(dir_name=dirname)
    for image_url_number, image_url in enumerate(container_links):
        data = {"api_key": token}
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/" \
                    f"{year}/{month}/{day}/png/{image_url['image']}.png"
        response_image = requests.get(url_image, params=data)
        response_image.raise_for_status()
        logging.warning(response_image.status_code)
        cut_path_url = urlparse(url_image)
        cut_path_clean = urllib.parse.unquote(cut_path_url.path)
        name_file_url = os.path.split(cut_path_clean)
        tail_url = os.path.splitext(name_file_url[-1])[-1]
        with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
            file.write(response_image.content)
    return file_path


def publish_photo(token, token_bot, year, month, day, url, timeout, chat_id):
    file_path = get_earth_images(
        url_archive=url,
        token=token,
        year=year,
        month=month,
        day=day,
    )
    file_images = random.choice(os.listdir(file_path))
    token_bot = token_bot
    bot = telegram.Bot(token=token_bot)
    while True:
        try:
            file_images_nasa = os.path.join(file_path, file_images)
            bot.send_photo(chat_id=chat_id, photo=open(file_images_nasa, "rb"))
            time.sleep(int(timeout))
        except TelegramError as exc:
            logging.warning(exc)


def get_period_from_user():
    parser = argparse.ArgumentParser(
        description="The script sends a photo of the planet to"
                    " the telegram channel with a specified frequency."
    )
    parser.add_argument(
        "-hh", "--hours", help="Set the update period in hours use arguments: '-hh or --hours'"
    )
    parser.add_argument(
        "-s", "--seconds", help="Set the update period in seconds use arguments: '-s or --seconds'"
    )
    parser.add_argument(
        "-a", "--apod", help="Uploads a photo of space day use arguments: '-a or --apod' and command: APOD"
    )
    parser.add_argument(
        "-l", "--last", help="Uploads photos of the last NASA launch use arguments: '-l or --last' and command: LAST"
    )
    args_timeout_hours = parser.parse_args().hours
    args_timeout_seconds = parser.parse_args().seconds
    args_apod = parser.parse_args().apod
    args_last_launch = parser.parse_args().last

    if args_timeout_hours:
        return int(args_timeout_hours)
    elif args_timeout_seconds:
        return float(args_timeout_seconds) / 60 / 60
    elif args_apod:
        get_apod_images(token=os.getenv("API_KEY_NASA"))
        exit()
    elif args_last_launch:
        fetch_spacex_last_launch(token=os.getenv("API_KEY_NASA"))
        exit()
    else:
        return 24


def defines_timeout_user():
    timeout_user = get_period_from_user()
    timeout = 60 * 60 * timeout_user
    return timeout


def main():
    logging.basicConfig(
        level=logging.WARNING,
        filename="logs.log",
        filemode="w",
        format="%(asctime)s - [%(levelname)s] - %(message)s",
    )
    load_dotenv()
    today = datetime.date.today()
    if today.day < 10:
        today_day = f"0{today.day - 2}"
    url_archive = f"https://api.nasa.gov/EPIC/api/natural/date/" \
                  f"{today.year}-{today.month}-{today_day}"
    timeout = defines_timeout_user()

    publish_photo(
        token=os.getenv("API_KEY_NASA"),
        token_bot=os.getenv("API_KEY_BOT"),
        year=today.year,
        month=today.month,
        day=today_day,
        url=url_archive,
        timeout=timeout,
        chat_id=os.getenv("CHAT_ID"),
    )


if __name__ == "__main__":
    main()
