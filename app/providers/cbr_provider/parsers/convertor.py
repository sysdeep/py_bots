
from xml.etree.ElementTree import Element


class Convertor:

    @classmethod
    def extract_str(cls, value: str) -> str:
        return value

    @classmethod
    def extract_float(cls, value: str) -> float:
        re_value = value.replace(',', '.')
        return float(re_value)

    @classmethod
    def extract_int(cls, value: str) -> int:
        return int(value)
