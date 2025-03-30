#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import telebot

from app.config.config import Config
from app.config.toml_config_parser import TomlConfigParser
from app.handlers.admin.admin_handler import AdminHandler
from app.handlers.echo_handler import EchoHandler
from app.handlers.fin_handler import FinHandler
from app.handlers.health_handler import HealthHandler
from app.handlers.start_handler import StartHandler
from app.logger.logger_configurator import LoggerConfigurator
from app.services.health_service.health_service import HealthService
from app.settings.application_settings_reader import ApplicationSettingsReader
from cclient import CClient, CClientSettings


def main(config: Config):

    print(config)

    logger = LoggerConfigurator.configure("INFO")
    logger.info("start application")

    # cclients
    cclients = _create_cclients(config)

    # create bot
    application_settings = ApplicationSettingsReader.read_from_env()
    bot = telebot.TeleBot(application_settings.token)

    self_dir = Path(os.path.realpath(__file__)).parent
    version = _get_version(self_dir)
    logger.info("version: %s", version)

    # services
    health_service = HealthService()

    # handlers
    start_handler = StartHandler(bot)
    echo_handler = EchoHandler(bot)
    fin_handler = FinHandler(bot)
    admin_handler = AdminHandler(bot, version, cclients)
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


def _parse_config(file_path: str) -> Config:
    return TomlConfigParser(file_path).parse()


def _create_cclients(config: Config) -> list[CClient]:
    if not config.vps:
        return []

    with open(config.cc_access_token, encoding="utf-8") as fd:
        token = fd.read()

    clients = []
    for vps in config.vps:

        cclient = CClient(CClientSettings(server=vps.address, token=token.rstrip(), name=vps.name))

        clients.append(cclient)

    return clients


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NIA py bot", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--config", type=str, required=True, help="path to configuration file")

    args = parser.parse_args()

    config = _parse_config(args.config)

    main(config)
