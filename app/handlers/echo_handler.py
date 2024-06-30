import logging

from telebot import TeleBot
from telebot.types import Message


class EchoHandler:
    def __init__(self, bot: TeleBot):
        self._bot = bot

    def do_echo(self, message: Message):

        self._logger.info(f"echo message: {message.text}")
        response_text = message.text or "-"
        self._bot.send_message(message.chat.id, response_text)

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
