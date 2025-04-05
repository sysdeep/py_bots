from typing import Callable

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telebot.callback_data import CallbackData

from cclient import CClient, Service, Action


from .vps_page import VPSPage


class VPSGroup:
    def __init__(self, bot: TeleBot, cclients: list[CClient], go_parent_handler: Callable[[Message], None]):
        self._bot = bot
        self._cclients = cclients
        self._go_parent_handler = go_parent_handler

        self._vps_page = VPSPage(bot, go_parent_handler=go_parent_handler)  # TODO

        self._bot.callback_query_handler(func=lambda call: call.data == "vps:go_main")(self._on_go_main)
        self._bot.callback_query_handler(func=lambda call: call.data.startswith("vps_page_go"))(self._on_go_vps)

    def start(self, cb: CallbackQuery):
        """"""
        result_text = self._make_header("VPS")

        chat_id = cb.message.chat.id
        self._bot.answer_callback_query(cb.id, "VPS main")

        result_text += "\n"
        result_text += "-" * 20 + "\n"

        kbd = InlineKeyboardMarkup()
        buttons = []
        for i, cclient in enumerate(self._cclients):
            buttons.append(
                InlineKeyboardButton(
                    text=f"{cclient.settings.name}",
                    callback_data=f"vps_page_go:{i}",
                )
            )

        kbd.add(
            *buttons,
            InlineKeyboardButton(text="Back", callback_data="vps:go_main"),
        )

        self._bot.send_message(chat_id, result_text, reply_markup=kbd)

        # NOTE: замещает тек. сообщение
        # self._bot.edit_message_text(
        #     chat_id=chat_id, message_id=cb.message.message_id, text=result_text, reply_markup=kbd
        # )

    def _on_go_main(self, cb: CallbackQuery):
        self._bot.answer_callback_query(cb.id, "go main")

        self._go_parent_handler(cb.message)

    def _on_go_vps(self, cb: CallbackQuery):
        _, client_index = cb.data.split(":")

        self._bot.answer_callback_query(cb.id, str(client_index))

        # VPSPage.start(self._bot, cclient=self._cclients[int(client_index)], call=cb)

        # self._go_parent_handler(cb.message)

        self._vps_page.start(cclient=self._cclients[int(client_index)], cb=cb)

    @classmethod
    def _make_header(cls, text: str) -> str:
        return "\n".join([text, cls._make_dash(), ""])

    @classmethod
    def _make_dash(cls) -> str:
        return "-" * 20


# def back_keyboard():
#     return InlineKeyboardMarkup(
#         keyboard=[
#             [
#                 InlineKeyboardButton(text="⬅", callback_data="back"),
#             ],
#         ]
#     )
