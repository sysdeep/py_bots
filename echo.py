#!/usr/bin/env python3
"""
example echo bot
"""
from pathlib import Path

import telebot

from services.health_service.health_service import HealthService

BOT_TOKEN = Path(".token").read_text().strip()


bot = telebot.TeleBot(BOT_TOKEN)
health_service = HealthService()


# start -----------------------------------------------------------------------
@bot.message_handler(commands=["help", "start"])
def send_welcome(message: telebot.types.Message):
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=False, resize_keyboard=True
    )

    # button_support = telebot.types.KeyboardButton(text="Написать в поддержку")

    for x in ["/start", "/health", "/admin"]:
        markup.add(x)


    response_text = 'Hello'
    if message.from_user:
        response_user_text = f'user: {message.from_user.username}({message.from_user.id})'
        response_text += f'\n{response_user_text}'

    bot.send_message(message.chat.id, response_text, reply_markup=markup)



# healt -----------------------------------------------------------------------
@bot.message_handler(commands=["health"])
def health_handler(message):

    health_data = health_service.get_health()

    response = f"cpu count: {health_data.cpu_count}\n"
    response += f"mem: {health_data.mem_prc}%\n"

    bot.send_message(message.chat.id, response)


# admin -----------------------------------------------------------------------
@bot.message_handler(commands=["admin"])
def admin_handler(message):

    response = "this is admin page"

    kbd = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data='save_data')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                     callback_data='change_data')
    kbd.add(button_save, button_change)

    bot.send_message(message.chat.id, response, reply_markup=kbd)


@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call: telebot.types.CallbackQuery):
    # message = call.message
    # chat_id = message.chat.id
    # bot.send_message(chat_id, f'Данные сохранены', disable_notification=True)
    bot.answer_callback_query(call.id, 'Данные сохранены', show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def change_btn(call: telebot.types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    bot.answer_callback_query(call.id, f'Изменение данных.')
    bot.send_message(chat_id, f'Изменение данных.')




# default echo ----------------------------------------------------------------
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
    # bot.infinity_polling()
