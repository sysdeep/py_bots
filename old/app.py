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


def get_images():
    spath = os.path.abspath(os.path.dirname(__file__))
    ipath = os.path.join(spath, "images")
    files = os.listdir(ipath)
    return [os.path.join(ipath, fd) for fd in files]


def generate_markup(right_answer, wrong_answers):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    # Склеиваем правильный ответ с неправильными
    all_answers = "{},{}".format(right_answer, wrong_answers)
    # Создаем лист (массив) и записываем в него все элементы
    list_items = []
    for item in all_answers.split(","):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    # shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=False, resize_keyboard=True
    )
    for x in ["/start", "/help", "/img", "/imgs"]:
        markup.add(x)

    # bot.reply_to(message, """\
    bot.send_message(message.chat.id, "Hi there, I am Bot.", reply_markup=markup)


@bot.message_handler(commands=["game"])
def send_image(message):

    markup = generate_markup("yes", "/no,go,pass,yes")

    images = get_images()
    img = random.choice(images)

    with open(img, "rb") as photo:
        res = bot.send_photo(message.chat.id, photo, reply_markup=markup)


@bot.message_handler(commands=["img"])
def send_image(message):
    images = get_images()
    img = random.choice(images)

    keyboard_hider = telebot.types.ReplyKeyboardRemove()

    with open(img, "rb") as photo:
        res = bot.send_photo(message.chat.id, photo, reply_markup=keyboard_hider)


# 	file_id = 'AAAaaaZZZzzz'
# 	bot.send_photo(message.chat.id, file_id)
# #     bot.reply_to(message, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)


@bot.message_handler(commands=["imgs"])
def send_images(message):
    images = get_images()
    # img = random.choice(images)

    for img in images:

        with open(img, "rb") as photo:
            bot.send_photo(message.chat.id, photo)

        time.sleep(3)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): 									# Название функции не играет никакой роли, в принципе
#     bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=["test"])
def find_file_ids(message):
    bot.send_message(message.chat.id, "testzsdzsdzd")
    # for file in os.listdir('music/'):
    #     if file.split('.')[-1] == 'ogg':
    #         f = open('music/'+file, 'rb')
    #         res = bot.send_voice(message.chat.id, f, None)
    #         print(res)
    #     time.sleep(3)


# def


if __name__ == "__main__":
    bot.polling(none_stop=True)
    # get_images()
