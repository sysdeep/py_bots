from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup


class StartHandler:
    def __init__(self, bot: TeleBot) -> None:
        self._bot = bot

    def do_send_welcome(self, message: Message):
        markup = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

        # button_support = telebot.types.KeyboardButton(text="Написать в поддержку")

        for x in ["/start", "/health", "/fin", "/admin"]:
            markup.add(x)

        response_text = "Hello"
        if message.from_user:
            response_user_text = (
                f"user: {message.from_user.username}({message.from_user.id})"
            )
            response_text += f"\n{response_user_text}"

        self._bot.send_message(message.chat.id, response_text, reply_markup=markup)
