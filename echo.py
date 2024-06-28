#!/usr/bin/env python3
"""
example echo bot
"""
from pathlib import Path

import telebot

BOT_TOKEN = Path(".token").read_text().strip()


bot = telebot.TeleBot(BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""",
    )


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    # bot.polling(none_stop=True)
    bot.infinity_polling()
