import argparse
import logging
import os
import random
import time
import urllib
from datetime import timedelta, datetime
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


def get_file_path(dir_name="spase_images"):
    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.abspath(dir_name)
    return file_path


def get_tail_url(url):
    parse_path_url = urlparse(url)
    path_clean = urllib.parse.unquote(parse_path_url.path)
    url_file_name = os.path.split(path_clean)
    url_tail = os.path.splitext(url_file_name[-1])[-1]
    return url_tail


def get_apod_images(token):
    url = "https://api.nasa.gov/planetary/apod"
    container_links = get_container_links(url=url, token=token)
    file_path = get_file_path()
    for image_url_number, image_url in enumerate([container_links]):
        if image_url["media_type"] == "image":
            image_response = requests.get(image_url["url"])
            image_response.raise_for_status()
            logging.warning(image_response.status_code)
            url_tail= get_tail_url(url=image_url["url"])
            with open(f"{file_path}/{'apod-'}{image_url_number}{url_tail}", "wb") as file:
                file.write(image_response.content)


def fetch_spacex_last_launch():
    url = "https://api.spacexdata.com/v3/launches/55"
    container_links = get_container_links(url=url, token=None)
    file_path = get_file_path()
    for image_url_number, image_url in enumerate(container_links["links"]["flickr_images"]):
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        logging.warning(image_response.status_code)
        url_tail = get_tail_url(url=image_url)
        with open(f"{file_path}/{'spacex-'}{image_url_number}{url_tail}", "ab") as file:
            file.write(image_response.content)


def get_earth_images(archive_url, token, date):
    container_links = get_container_links(url=archive_url, token=token)
    if not container_links:
        logging.warning("Нет данных")
        return
    file_path = get_file_path()
    for image_url_number, image_url in enumerate(container_links):
        data = {"api_key": token}
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/" \
                    f"{date}/png/{image_url['image']}.png"
        image_response = requests.get(url_image, params=data)
        image_response.raise_for_status()
        logging.warning(image_response.status_code)
        url_tail = get_tail_url(url=url_image)
        with open(f"{file_path}/{'earth-'}{image_url_number}{url_tail}", "ab") as file:
            file.write(image_response.content)


def publish_photo(token_bot, timeout, chat_id):
    file_path = get_file_path()
    bot = telegram.Bot(token=token_bot)
    while True:
        file_images = random.choice(os.listdir(file_path))
        try:
            file_images_nasa = os.path.join(file_path, file_images)
            with open(file_images_nasa, "rb") as file_photo:
                bot.send_photo(chat_id=chat_id, photo=file_photo)
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
    args = parser.parse_args()
    timeout_hours = args.hours
    timeout_seconds = args.seconds

    if timeout_hours:
        return int(timeout_hours) * 60 * 60
    elif timeout_seconds:
        return int(timeout_seconds)
    else:
        return 86400


def main():
    logging.basicConfig(
        level=logging.WARNING,
        filename="logs.log",
        filemode="w",
        format="%(asctime)s - [%(levelname)s] - %(message)s",
    )
    load_dotenv()
    timeout = get_period_from_user()
    today = datetime.now()
    data_delay = 3
    delayed = timedelta(data_delay)
    delayed_day = today - delayed
    date_natural = delayed_day.strftime("%Y-%m-%d")
    archive_url = f"https://api.nasa.gov/EPIC/api/natural/date/{date_natural}"
    get_apod_images(token=os.getenv("API_KEY_NASA"))
    date_arhive = delayed_day.strftime("%Y/%m/%d")
    get_earth_images(
        archive_url=archive_url,
        token=os.getenv("API_KEY_NASA"),
        date=date_arhive,
    )
    fetch_spacex_last_launch()
    publish_photo(
        token_bot=os.getenv("API_KEY_BOT"),
        timeout=timeout,
        chat_id=os.getenv("CHAT_ID"),
    )


if __name__ == "__main__":
    main()
