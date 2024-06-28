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


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=False, resize_keyboard=True
    )
    # for x in ["/start", "/flovers", "/tits"]:
    for x in ["/health"]:
        markup.add(x)

    # bot.reply_to(message, """\
    bot.send_message(message.chat.id, "Привет...", reply_markup=markup)


#     bot.reply_to(
#         message,
#         """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """,
#     )
#


@bot.message_handler(commands=["health"])
def health_handler(message):

    health_data = health_service.get_health()

    response = f"cpu count: {health_data.cpu_count}\n"
    response += f"mem: {health_data.mem_prc}%\n"

    bot.send_message(message.chat.id, response)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
    # bot.infinity_polling()
