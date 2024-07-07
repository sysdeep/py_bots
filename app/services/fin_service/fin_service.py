from dataclasses import dataclass
from datetime import datetime, timedelta

from app.providers.cbr_provider.cbr_provider import CbrProvider

@dataclass
class Valute:
    char_code: str
    value: float
    trend: float


@dataclass
class ValuteReport:
    date: str
    valutes: list[Valute]



class FinService:
    NEED_VALUTES = ['USD', 'EUR']
    def __init__(self) -> None:
        self._provider = CbrProvider()

    def get_valute(self) -> ValuteReport:
        
        # now
        valutes_now = self._provider.get_valute()
        now_date = datetime.strptime(valutes_now.date, '%Y.%m.%d')

        yesterday_date = now_date - timedelta(days=1)
        valutes_yesterday = self._provider.get_valute(yesterday_date)


        filtered_now = [v for v in valutes_now.valutes if v.char_code in self.NEED_VALUTES]
        filtered_yesterday = [v for v in valutes_yesterday.valutes if v.char_code in self.NEED_VALUTES]

        valutes = []
        for v in filtered_now:

            trend = 0.0

            for yv in filtered_yesterday:
                if yv.char_code == v.char_code:
                    trend = v.value - yv.value
                    break

            valutes.append(Valute(char_code=v.char_code, value=v.value, trend=trend))


        return ValuteReport(date=valutes_now.date, valutes=valutes)
