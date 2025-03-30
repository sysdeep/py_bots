import logging

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from cclient import CClient, Service, Action


# TODO: необходимо расширить менюшку, появился самостоятельный раздел с VPS
# TODO: что то типа StateMachine
class AdminHandler:
    def __init__(self, bot: TeleBot, version: str, cclients: list[CClient]):
        self._bot = bot
        self._version = version
        self._cclients = cclients
        self._cclient = self._cclients[0]  # tests

        self._kbd: InlineKeyboardMarkup = self._make_kbd()

        # register more handlers
        self._bot.callback_query_handler(func=lambda call: call.data == "show_nginx_status")(self._on_show_nginx_status)

        self._bot.callback_query_handler(func=lambda call: call.data == "show_wireguard_status")(
            self._on_show_wireguard_status
        )

        self._bot.callback_query_handler(func=lambda call: call.data == "stop_wireguard")(self._on_stop_wireguard)

        self._bot.callback_query_handler(func=lambda call: call.data == "start_wireguard")(self._on_start_wireguard)

    def do_admin(self, message: Message):

        resp_text = self._make_header("Админка - главная")

        resp_text += "\n"

        resp_text += "VPS:\n"
        for cclient in self._cclients:
            resp_text += f"{cclient.settings.name}\n"

        resp_text += "\n"
        self._send_response(message.chat.id, resp_text)

    def _on_show_nginx_status(self, call: CallbackQuery):

        result_text = self._make_header("Nginx status")

        try:
            result_text += self._cclient.service(Service.nginx, Action.status)
        except Exception as e:
            result_text += str(e)

        message = call.message
        chat_id = message.chat.id
        self._bot.answer_callback_query(call.id, "Ответ")
        # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
        self._send_response(chat_id, result_text)

    def _on_show_wireguard_status(self, call: CallbackQuery):

        try:
            result_text = self._cclient.service(Service.wireguard, Action.status)
        except Exception as e:
            result_text = str(e)

        message = call.message
        chat_id = message.chat.id
        self._bot.answer_callback_query(call.id, "Ответ")
        # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
        self._send_response(chat_id, result_text)

    def _on_stop_wireguard(self, call: CallbackQuery):

        try:
            result_text = self._cclient.service(Service.wireguard, Action.stop)
        except Exception as e:
            result_text = str(e)

        message = call.message
        chat_id = message.chat.id
        self._bot.answer_callback_query(call.id, "Ответ")
        # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
        self._send_response(chat_id, result_text)

    def _on_start_wireguard(self, call: CallbackQuery):

        try:
            result_text = self._cclient.service(Service.wireguard, Action.start)
        except Exception as e:
            result_text = str(e)

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

    def _make_header(self, text: str) -> str:
        return "\n".join([text, self._make_dash(), ""])

    def _make_dash(self) -> str:
        return "-" * 20

    @classmethod
    def _make_kbd(cls) -> InlineKeyboardMarkup:
        kbd = InlineKeyboardMarkup()
        button_show_procs = InlineKeyboardButton(text="Show nginx", callback_data="show_nginx_status")
        kbd.add(
            button_show_procs,
            # more buttons
            InlineKeyboardButton(text="Show wireguard", callback_data="show_wireguard_status"),
            InlineKeyboardButton(text="Stop wireguard", callback_data="stop_wireguard_status"),
            InlineKeyboardButton(text="Start wireguard", callback_data="start_wireguard_status"),
        )

        return kbd

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
