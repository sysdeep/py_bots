#!/usr/bin/env python3
import os
from pathlib import Path

import telebot

from app.handlers.admin_handler import AdminHandler
from app.handlers.echo_handler import EchoHandler
from app.handlers.fin_handler import FinHandler
from app.handlers.health_handler import HealthHandler
from app.handlers.start_handler import StartHandler
from app.logger.logger_configurator import LoggerConfigurator
from app.services.health_service.health_service import HealthService
from app.settings.application_settings_reader import ApplicationSettingsReader


def main():

    logger = LoggerConfigurator.configure("INFO")
    logger.info("start application")

    # create bot
    application_settings = ApplicationSettingsReader.read_from_env()
    bot = telebot.TeleBot(application_settings.token)

    self_dir = Path(os.path.realpath(__file__)).parent
    version = _get_version(self_dir)
    logger.info(f"version: {version}")

    # services
    health_service = HealthService()

    # handlers
    start_handler = StartHandler(bot)
    echo_handler = EchoHandler(bot)
    fin_handler = FinHandler(bot)
    admin_handler = AdminHandler(bot, version)
    health_handler = HealthHandler(bot, health_service)

    # register
    bot.message_handler(commands=["help", "start"])(start_handler.do_send_welcome)
    bot.message_handler(commands=["fin"])(fin_handler.do_valutes)
    bot.message_handler(commands=["health"])(health_handler.do_main_health)
    bot.message_handler(commands=["admin"])(admin_handler.do_admin)
    bot.message_handler(content_types=["text"])(echo_handler.do_echo)

    # start bot
    bot.polling(none_stop=True)
    # bot.infinity_polling()


def _get_version(base_dir_path: Path) -> str:
    file_path = base_dir_path / "Version"
    return file_path.read_text().strip()


if __name__ == "__main__":
    main()
