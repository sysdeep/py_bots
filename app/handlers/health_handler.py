import datetime
import logging

from telebot import TeleBot
from telebot.types import Message

from app.services.health_service.health_service import Health, HealthService


class HealthHandler:
    def __init__(self, bot: TeleBot, health_service: HealthService) -> None:
        self._bot = bot
        self._health_service = health_service

    def do_main_health(self, message: Message):

        try:
            health = self._health_service.get_health()
            response_text = self.format_main_health(health)
        except Exception as e:
            self._logger.exception(e)
            response_text = "Error: " + str(e)

        self._bot.send_message(message.chat.id, response_text)

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
