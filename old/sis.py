#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import requests
# from tornado import tornado
import os
import random
import time
from pathlib import Path

import telebot

BOT_TOKEN = Path(".token").read_text().strip()


bot = telebot.TeleBot(BOT_TOKEN)


def get_images(dir_name):
    spath = os.path.abspath(os.path.dirname(__file__))
    ipath = os.path.join(spath, dir_name)
    files = os.listdir(ipath)
    return [os.path.join(ipath, fd) for fd in files]


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=False, resize_keyboard=True
    )
    for x in ["/start", "/flovers", "/tits"]:
        markup.add(x)

    # bot.reply_to(message, """\
    bot.send_message(message.chat.id, "Привет - выбери команду...", reply_markup=markup)


@bot.message_handler(commands=["flovers"])
def send_flover(message):
    images = get_images("cats")
    img = random.choice(images)

    with open(img, "rb") as photo:
        res = bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "попробуем ещё раз???")


@bot.message_handler(commands=["tits"])
def send_tits(message):
    images = get_images("tits")
    img = random.choice(images)

    with open(img, "rb") as photo:
        res = bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "попробуем ещё раз???")


# @bot.message_handler(commands=['imgs'])
# def send_images(message):
# 	images = get_images()
# 	# img = random.choice(images)

# 	for img in images:

# 		with open(img, 'rb') as photo:
# 			bot.send_photo(message.chat.id, photo)

# 		time.sleep(3)


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
# 	bot.reply_to(message, message.text)


@bot.message_handler(func=lambda message: True)
# @bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
    # get_images()
