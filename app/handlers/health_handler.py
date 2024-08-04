import datetime
import logging

from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from app.services.health_service.health_service import Health, HealthService


class HealthHandler:
    def __init__(self, bot: TeleBot, health_service: HealthService) -> None:
        self._bot = bot
        self._health_service = health_service

        # register more handlers
        self._bot.callback_query_handler(
            func=lambda call: call.data == "show_health_procs"
        )(self._on_show_health_procs)

    def do_main_health(self, message: Message):

        try:
            health = self._health_service.get_health()
            response_text = self.format_main_health(health)
        except Exception as e:
            self._logger.exception(e)
            response_text = "Error: " + str(e)

        # buttons
        kbd = InlineKeyboardMarkup()
        button_show_procs = InlineKeyboardButton(
            text="Show procs", callback_data="show_health_procs"
        )
        kbd.add(
            button_show_procs,
            # more buttons
        )

        self._bot.send_message(message.chat.id, response_text, reply_markup=kbd)

    def _on_show_health_procs(self, call: CallbackQuery):

        message = call.message
        chat_id = message.chat.id
        self._bot.answer_callback_query(call.id, "Ответ")
        self._bot.send_message(chat_id, "Процессы:")

        # TODO: processes list

    @classmethod
    def format_main_health(cls, health: Health) -> str:
        """format health model to plain text"""
        cpu_text = f"cpu count: {health.cpu_count}\n"
        mem_text = f"mem used: {health.mem_prc}%\n"

        # boot time
        boot_time = datetime.datetime.fromtimestamp(health.boot_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        boot_time_text = f"boot: {boot_time}\n"

        part_template = "\t{:>4.1f}% {}\n"  # 23.1% /home
        disk_text = "disks:\n"
        for part in health.disk_info:
            text = part_template.format(part.usage.percent, part.mount_point)
            disk_text += text

        result = boot_time_text + cpu_text + mem_text + disk_text

        return result

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)


if __name__ == "__main__":

    def print_format_example():
        health = HealthService().get_health()
        print(HealthHandler.format_main_health(health))

    print_format_example()
