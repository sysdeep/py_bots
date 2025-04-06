import logging

from telebot import TeleBot, formatting
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from cclient import CClient

from .vps_group import VPSGroup


class AdminHandler:
    """обработчик админки"""

    route_main = "admin:main"

    def __init__(self, bot: TeleBot, version: str, cclients: list[CClient]):
        self._bot = bot
        self._version = version
        self._cclients = cclients
        self._cclient = self._cclients[0]  # tests

        self._vps_group = VPSGroup(bot, cclients=cclients, parent_route=self.route_main)

        # register more handlers
        self._bot.callback_query_handler(func=lambda call: call.data == self.route_main)(self._on_route_main)
        self._bot.callback_query_handler(func=lambda call: call.data == VPSGroup.route_vps_main)(self._vps_group.start)

    def do_admin(self, message: Message):
        """отобразить главный экран"""
        result_text = formatting.format_text(
            formatting.mbold("Админка - главная"),
            "",
            formatting.escape_markdown(f"Версия: {self._version}"),
            formatting.escape_markdown(f"User: {message.from_user.username}({message.from_user.id})"),
        )

        # kbd
        kbd = InlineKeyboardMarkup()
        kbd.add(InlineKeyboardButton(text="VPS", callback_data=VPSGroup.route_vps_main))

        self._bot.send_message(
            message.chat.id,
            result_text,
            parse_mode="MarkdownV2",
            reply_markup=kbd,
        )

    def _on_route_main(self, call: CallbackQuery):
        self._bot.answer_callback_query(call.id, "")
        self.do_admin(call.message)

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
