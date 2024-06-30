import logging
import sys
import time

default_log_format = "%(asctime)s.%(msecs)d [%(name)s] %(levelname)s %(message)s"


class LoggerConfigurator:

    @classmethod
    def configure(cls, log_level: str, log_format: str | None = None):
        if not log_format:
            log_format = default_log_format

        logging.getLogger().setLevel(log_level)

        if isinstance(log_level, str):
            log_level = logging.getLevelName(log_level)

        formatter = logging.Formatter(log_format)

        formatter.converter = time.gmtime  # UTC
        logging.basicConfig(stream=sys.stdout, level=log_level)

        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setFormatter(formatter)
