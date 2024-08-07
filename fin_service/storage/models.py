from dataclasses import dataclass


@dataclass
class Valute:
    name: str  # Австралийский доллар
    value: float  # 59,3500
    num_code: str  # 036, ISO Цифр. код валюты
    char_code: str  # AUD, ISO Букв. код валюты
    nominal: int  # 1, номинал. ед
    vunit_rate: float  # 59,35, Курс за 1 единицу валюты
    date: str
