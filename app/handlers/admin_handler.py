import logging

from telebot import TeleBot
from telebot.types import Message


class AdminHandler:
    def __init__(self, bot: TeleBot, version: str):
        self._bot = bot
        self._version = version

    def do_admin(self, message: Message):


        response_text = f'Version: {self._version}'

        self._bot.send_message(message.chat.id, response_text)





    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
