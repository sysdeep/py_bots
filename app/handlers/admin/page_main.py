from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from cclient import CClient
from .page import Page


class PageMain(Page):
    """
    попытка разделить логику по разным страницам
    видимо я что то не понимаю, потому что есть callback и у них другой интерфейс

    пока страница не используется нигде
    """

    Q_VPS = "main:vps"

    def __init__(self, bot: TeleBot, version: str, cclients: list[CClient]):
        self._bot = bot
        self._version = version
        self._cclients = cclients

        self._kbd = self._make_kbd()

        # register more handlers
        self._bot.callback_query_handler(func=lambda call: call.data == self.Q_VPS)(self._on_show_nginx_status)

    def show(self, chat_id: int):
        resp_text = self.make_header("Админка - главная")

        resp_text += "\n"

        resp_text += "VPS:\n"
        for cclient in self._cclients:
            resp_text += f"{cclient.settings.name}\n"

        resp_text += "\n"
        self._send_response(chat_id, resp_text)

    def _on_show_nginx_status(self, call: CallbackQuery):

        result_text = self.make_header("Nginx status")

        # try:
        #     result_text += self._cclients[0].service(Service.nginx, Action.status)
        # except Exception as e:
        #     result_text += str(e)

        message = call.message
        chat_id = message.chat.id
        self._bot.answer_callback_query(call.id, "Ответ")
        # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
        self._send_response(chat_id, result_text)

    def _send_response(self, chat_id, text: str):

        result_text = text + "\n"
        result_text += "-" * 20 + "\n"
        result_text += f"Version: {self._version}"

        self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)

    @classmethod
    def _make_kbd(cls) -> InlineKeyboardMarkup:
        kbd = InlineKeyboardMarkup()
        kbd.add(
            InlineKeyboardButton(text="VPS", callback_data=cls.Q_VPS),
        )

        return kbd
