import logging
import os

import requests

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from urllib.parse import urlparse


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token="2127492642:AAFC4-Ey3WTtFNCcSzbDN7Z7y1ePaw8IbTU", use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)


def hi(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


hi_handler = CommandHandler("hi", hi)
dispatcher.add_handler(hi_handler)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def caps(update, context):
    text_caps = " ".join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler("caps", caps)
dispatcher.add_handler(caps_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
# updater.stop()


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
    # fetch_spacex_last_launch(dir_name=dirname)


