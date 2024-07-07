import logging

from telebot import TeleBot
from telebot.types import Message

from app.services.fin_service.fin_service import FinService

class FinHandler:
    NEED_VALUTES = ['USD', 'EUR']
    def __init__(self, bot: TeleBot):
        self._bot = bot
        self._service = FinService()

    def do_valutes(self, message: Message):
        """show valutes"""

        try:    
            valutes_result = self._service.get_valute()

            response_text = f"Котировки валют на {valutes_result.date} \n"

            for v in valutes_result.valutes:
                trend_sign = '+' if v.trend > 0 else '-'
                response_text += f'\t{v.char_code}: {v.value:.2f} {trend_sign}{abs(v.trend):.2f}\n'
            
        except Exception as e:
            self._logger.exception(e)
            response_text = "Error: " + str(e)


        # self._logger.info(response_text)
        self._bot.send_message(message.chat.id, response_text)





    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)
