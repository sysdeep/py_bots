from abc import ABC, abstractmethod

from telebot.types import Message


class Page(ABC):

    @abstractmethod
    def show(self, chat_id: int):
        pass

    @classmethod
    def make_dash(cls) -> str:
        return "-" * 20

    @classmethod
    def make_header(cls, text: str) -> str:
        return "\n".join([text, cls.make_dash(), ""])
