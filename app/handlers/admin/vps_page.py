from typing import Callable

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from cclient import CClient, Service, Action


# class VPSPage:

# @classmethod
# def start(cls, bot: TeleBot, cclient: CClient, call: CallbackQuery):

#     kbd = InlineKeyboardMarkup()
#     buttons = []

#     kbd.add(
#         *buttons,
#         InlineKeyboardButton(text="Back", callback_data="vps:go_main"),
#     )

#     bot.send_message(call.message.chat.id, "result_text", reply_markup=kbd)


# ------------------------------------------------------------------------------------------------------------------------


class VPSPage:
    def __init__(self, bot: TeleBot, go_parent_handler: Callable[[Message], None]):
        self._bot = bot
        self._go_parent_handler = go_parent_handler

        self._bot.callback_query_handler(func=lambda call: call.data == "vps:go_main")(self._on_go_main)

        # self._bot.callback_query_handler(func=lambda call: call.data == "show_nginx_status")(self._on_show_nginx_status)

        # self._bot.callback_query_handler(func=lambda call: call.data == "show_wireguard_status")(
        #     self._on_show_wireguard_status
        # )

        # self._bot.callback_query_handler(func=lambda call: call.data == "stop_wireguard")(self._on_stop_wireguard)

        # self._bot.callback_query_handler(func=lambda call: call.data == "start_wireguard")(self._on_start_wireguard)

    def start(self, cclient: CClient, cb: CallbackQuery):
        """"""
        result_text = self._make_header(f"VPS: {cclient.settings.name}")

        # self._bot.answer_callback_query(cb.id, "VPS")

        # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
        # self._send_response(chat_id, result_text)

        result_text += "\n"
        result_text += "-" * 20 + "\n"
        # result_text += f"Version: {self._version}"

        kbd = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton(text="Show nginx", callback_data="vps_page_action:show_nginx_status"),
            # more buttons
            InlineKeyboardButton(text="Show wireguard", callback_data="vps_page_action:show_wireguard_status"),
            InlineKeyboardButton(text="Stop wireguard", callback_data="vps_page_action:stop_wireguard_status"),
            InlineKeyboardButton(text="Start wireguard", callback_data="vps_page_action:start_wireguard_status"),
        ]
        # for cclient in self._cclients:
        #     buttons.append(InlineKeyboardButton(text=f"{cclient.settings.name}", callback_data="admin:go_vps"))

        kbd.add(
            *buttons,
            InlineKeyboardButton(text="Back", callback_data="vps:go_main"),
        )

        self._bot.send_message(cb.message.chat.id, result_text, reply_markup=kbd)

        # NOTE: замещает тек. сообщение
        # self._bot.edit_message_text(
        #     chat_id=chat_id, message_id=cb.message.message_id, text=result_text, reply_markup=kbd
        # )

    def _on_go_main(self, cb: CallbackQuery):
        self._bot.answer_callback_query(cb.id, "go main")

        self._go_parent_handler(cb.message)

    # def _on_show_nginx_status(self, call: CallbackQuery):

    #     result_text = self._make_header("Nginx status")

    #     try:
    #         result_text += self._cclient.service(Service.nginx, Action.status)
    #     except Exception as e:
    #         result_text += str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     # self._send_response(chat_id, result_text)

    # def _on_show_wireguard_status(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.status)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     # self._send_response(chat_id, result_text)

    # def _on_stop_wireguard(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.stop)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     # self._send_response(chat_id, result_text)

    # def _on_start_wireguard(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.start)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     # self._send_response(chat_id, result_text)

    @classmethod
    def _make_header(cls, text: str) -> str:
        return "\n".join([text, cls._make_dash(), ""])

    @classmethod
    def _make_dash(cls) -> str:
        return "-" * 20
