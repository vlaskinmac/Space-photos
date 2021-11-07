import argparse
import datetime
import logging
import os
import time
from urllib.parse import urlparse

import requests
import telegram

from telegram import TelegramError
from dotenv import load_dotenv


def get_container_links(url, token):
    data = {"api_key": token}
    response = requests.get(url, params=data)
    response.raise_for_status()
    logging.warning(response.status_code)
    return response.json()


def fetch_spacex_last_launch(*args, **kwargs):
    container_links = get_container_links(url=kwargs["url_archive"], token=kwargs["token"])
    if not container_links:
        logging.warning("Нет данных")
        print("Нет данных")
        exit()
    if not os.path.exists(kwargs["dir_name"]):
        os.mkdir(kwargs["dir_name"])
    file_path = os.path.abspath(kwargs["dir_name"])
    for image_url_number, image_url in enumerate(container_links):
        data = {"api_key": kwargs["token"]}
        url_image = f"https://api.nasa.gov/EPIC/archive/natural/" \
                    f"{kwargs['year']}/{kwargs['month']}/{kwargs['day']}/png/{image_url['image']}.png"
        response_image = requests.get(url_image, params=data)
        response_image.raise_for_status()
        logging.warning(response_image.status_code)
        cut_path_url = urlparse(url_image)
        name_file_url = os.path.split(cut_path_url.path)
        tail_url = os.path.splitext(name_file_url[-1])[-1]

        with open(f"{file_path}/{image_url_number}{tail_url}", "wb") as file:
            file.write(response_image.content)
            print(f"{image_url_number + 1} - картинка загружена")
    return file_path


def publish_photo(*args, **kwargs):
    file_path = fetch_spacex_last_launch(*args, **kwargs)
    file_images = os.listdir(file_path)
    token_bot = kwargs["token_bot"]
    bot = telegram.Bot(token=token_bot)

    while True:
        try:
            bot.send_message(text="Добрый день!", chat_id=kwargs["chat_id"])
            bot.send_message(text=f"Фотки за {kwargs['today_date']} число!", chat_id=kwargs["chat_id"])
            count = 0
            for image in file_images:
                count += 1
                file_images_nasa = os.path.join(file_path, image)
                bot.send_message(text=f"Фотка № {count}:", chat_id=kwargs["chat_id"])
                bot.send_photo(chat_id=kwargs["chat_id"], photo=open(file_images_nasa, "rb"))
                time.sleep(10)
            bot.send_message(text=f"Ожидание следующей публикации!", chat_id=kwargs["chat_id"])
            bot.send_message(
                text=f"Следующая публикация через {kwargs['timeout_user_info']}",
                chat_id=kwargs["chat_id"],
            )
            time.sleep(int(kwargs["timeout"]))
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
    args_timeout_hours = parser.parse_args().hours
    args_timeout_seconds = parser.parse_args().seconds

    if args_timeout_hours:
        return int(args_timeout_hours)
    if args_timeout_seconds:
        return float(args_timeout_seconds) / 60 / 60
    else:
        return 24


def defines_timeout_user():
    timeout_user = get_period_from_user()
    timeout = 60 * 60 * timeout_user
    if (int(timeout_user) > 1) and (float(timeout) / 60 / 60 != 24):
        print(f"--- Выбрана публикация раз в {timeout_user} часа ---")
        timeout_user = timeout
        timeout_user_info = f"{timeout_user} часа"
    elif float(timeout_user) < 1:
        print(f"--- Выбрана публикация раз в {int(timeout)} секунд ---")
        timeout_user = int(timeout)
        timeout_user_info = f"{int(timeout)} секунд"
    else:
        print(f"--- Публикация по умолчанию раз в {timeout_user} часа ---")
        timeout_user = timeout_user
        timeout_user_info = f"{timeout_user} часа"
    return timeout, timeout_user, timeout_user_info


def main():
    logging.basicConfig(
        level=logging.WARNING,
        filename="logs.log",
        filemode="w",
        format="%(asctime)s - [%(levelname)s] - %(message)s",
    )

    CHAT_ID = -1001647060957
    load_dotenv()
    today = datetime.date.today()
    timeout, timeout_user, timeout_user_info = defines_timeout_user()

    parameters = {
        "token": os.getenv("API_KEY_NASA"),
        "token_bot": os.getenv("API_KEY_BOT"),
        "dir_name": "NASA_images",
        "year": f"{today.year}",
        "month": f"{today.month}",
        "day": f"{today.day}",
        "today_date": f"{today}",
        "url_archive": f"https://api.nasa.gov/EPIC/api/natural/date/"
                       f"{today.year}-{today.month}-{today.day}",
        "timeout": timeout,
        "timeout_user": timeout_user,
        "timeout_user_info": timeout_user_info,
        "chat_id": CHAT_ID,
    }

    publish_photo(**parameters)


if __name__ == "__main__":
    main()
