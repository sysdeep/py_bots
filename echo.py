#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot

BOT_TOKEN = "349973004:AAEZYylLlwfcIyLwxkaE-veGWjRB9YPBcVM"



bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 									# Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
    bot.polling(none_stop=True)
