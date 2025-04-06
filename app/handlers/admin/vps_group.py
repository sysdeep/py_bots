from typing import Callable

from telebot import TeleBot
from telebot import formatting
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telebot.callback_data import CallbackData

from cclient import CClient, Service, Action


# from .vps_page import VPSPage


class VPSGroup:
    """обработчик VPS запросов"""

    route_vps_main = "vps:main"
    route_vps_node = "vps_node_go"  # NOTE: + ":cclient_index"

    route_nginx_status = "vps_page_action:show_nginx_status"  # NOTE: + ":client_index"

    def __init__(self, bot: TeleBot, cclients: list[CClient], parent_route: str):
        self._bot = bot
        self._cclients = cclients
        self._parent_route = parent_route

        # go to vps
        self._bot.callback_query_handler(func=lambda call: call.data.startswith(self.route_vps_node))(self._on_go_vps)
        self._bot.callback_query_handler(func=lambda call: call.data.startswith(self.route_nginx_status))(
            self._on_show_nginx_status
        )

    def start(self, call: CallbackQuery):
        """главная страница VPS"""

        # NOTE: hide popup
        self._bot.answer_callback_query(call.id, "")

        # prepare agents
        agent_buttons = []
        agent_texts = []
        for i, cclient in enumerate(self._cclients):
            agent_buttons.append(
                InlineKeyboardButton(
                    text=f"{cclient.settings.name}",
                    callback_data=f"{self.route_vps_node}:{i}",
                )
            )

            agent_texts.append(formatting.escape_markdown(f"- {cclient.settings.name} - {cclient.settings.server}"))

        # make kbd
        kbd = InlineKeyboardMarkup()
        kbd.add(*agent_buttons)
        kbd.add(InlineKeyboardButton(text="Back to Admin", callback_data=self._parent_route))

        result_text = formatting.format_text(
            formatting.mbold("Vps main"),
            "",
            "зарегистрированные агенты:",
            *agent_texts,
        )

        self._bot.send_message(
            call.message.chat.id,
            result_text,
            parse_mode="MarkdownV2",
            reply_markup=kbd,
        )

        # NOTE: замещает тек. сообщение
        # self._bot.edit_message_text(
        #     chat_id=chat_id, message_id=cb.message.message_id, text=result_text, reply_markup=kbd
        # )

    def _on_go_vps(self, cb: CallbackQuery):
        """отобразить информацию по заданному агенту"""
        # NOTE: hide popup
        self._bot.answer_callback_query(cb.id, "")

        client_id = self._unpack_agent(cb.data)
        cclient = self._cclients[client_id]

        result_text = formatting.format_text(
            formatting.mbold(cclient.settings.name),
            "",
            formatting.escape_markdown(f"address: {cclient.settings.server}"),
        )

        # kbd
        kbd = self._make_vps_node_kbd(client_id=client_id)

        self._bot.send_message(
            cb.message.chat.id,
            result_text,
            parse_mode="MarkdownV2",
            reply_markup=kbd,
        )

    def _on_show_nginx_status(self, call: CallbackQuery):

        self._bot.answer_callback_query(call.id, "")

        client_id = int(call.data.split(":")[-1])
        client = self._cclients[client_id]

        try:
            client_result = client.service(Service.nginx, Action.status)
        except Exception as e:
            client_result = str(e)

        result_text = formatting.format_text(
            formatting.mbold(f"{client.settings.name} - nginx status"), "", formatting.escape_markdown(client_result)
        )

        # kbd
        kbd = self._make_vps_node_kbd(client_id=client_id)

        self._bot.send_message(
            call.message.chat.id,
            result_text,
            parse_mode="MarkdownV2",
            reply_markup=kbd,
        )

    @classmethod
    def _make_vps_node_kbd(cls, client_id: int) -> InlineKeyboardMarkup:
        kbd = InlineKeyboardMarkup()

        kbd.add(
            InlineKeyboardButton(text="Show nginx", callback_data=f"vps_page_action:show_nginx_status:{client_id}"),
        )
        kbd.add(
            InlineKeyboardButton(text="Show wireguard", callback_data="vps_page_action:show_wireguard_status"),
            InlineKeyboardButton(text="Stop wireguard", callback_data="vps_page_action:stop_wireguard_status"),
            InlineKeyboardButton(text="Start wireguard", callback_data="vps_page_action:start_wireguard_status"),
        )

        kbd.add(InlineKeyboardButton(text="Back to VPS", callback_data=cls.route_vps_main))

        return kbd

    # def _on_show_wireguard_status(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.status)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     self._send_response(chat_id, result_text)

    # def _on_stop_wireguard(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.stop)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     self._send_response(chat_id, result_text)

    # def _on_start_wireguard(self, call: CallbackQuery):

    #     try:
    #         result_text = self._cclient.service(Service.wireguard, Action.start)
    #     except Exception as e:
    #         result_text = str(e)

    #     message = call.message
    #     chat_id = message.chat.id
    #     self._bot.answer_callback_query(call.id, "Ответ")
    #     # self._bot.send_message(chat_id, result_text, reply_markup=self._kbd)
    #     self._send_response(chat_id, result_text)

    @classmethod
    def _make_header(cls, text: str) -> str:
        return "\n".join([text, cls._make_dash(), ""])

    @classmethod
    def _make_dash(cls) -> str:
        return "-" * 20

    @classmethod
    def _pack_agent(cls, aid: int) -> str:
        return cls.route_vps_node + ":" + str(aid)

    @classmethod
    def _unpack_agent(cls, data: str) -> int:
        _, str_client_index = data.split(":")
        return int(str_client_index)


# def back_keyboard():
#     return InlineKeyboardMarkup(
#         keyboard=[
#             [
#                 InlineKeyboardButton(text="⬅", callback_data="back"),
#             ],
#         ]
#     )
