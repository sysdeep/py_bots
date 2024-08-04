import logging

from telebot import TeleBot
from telebot.types import Message


class AdminHandler:
    def __init__(self, bot: TeleBot, version: str):
        self._bot = bot
        self._version = version

    def do_admin(self, message: Message):

        response_text = f"Version: {self._version}"

        self._bot.send_message(message.chat.id, response_text)

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)


# admin -----------------------------------------------------------------------
# @bot.message_handler(commands=["admin"])
# def admin_handler(message):
#
#     response = "this is admin page"
#
#     kbd = telebot.types.InlineKeyboardMarkup()
#     button_save = telebot.types.InlineKeyboardButton(
#         text="Сохранить", callback_data="save_data"
#     )
#     button_change = telebot.types.InlineKeyboardButton(
#         text="Изменить", callback_data="change_data"
#     )
#     kbd.add(button_save, button_change)
#
#     bot.send_message(message.chat.id, response, reply_markup=kbd)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "save_data")
# def save_btn(call: telebot.types.CallbackQuery):
#     # message = call.message
#     # chat_id = message.chat.id
#     # bot.send_message(chat_id, f'Данные сохранены', disable_notification=True)
#     bot.answer_callback_query(call.id, "Данные сохранены", show_alert=True)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "change_data")
# def change_btn(call: telebot.types.CallbackQuery):
#     message = call.message
#     chat_id = message.chat.id
#     bot.answer_callback_query(call.id, f"Изменение данных.")
#     bot.send_message(chat_id, f"Изменение данных.")
#
