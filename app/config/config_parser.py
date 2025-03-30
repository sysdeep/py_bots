from abc import ABC, abstractmethod

from .config import Config


class ConfigParser:

    @abstractmethod
    def parse(self) -> Config:
        pass
