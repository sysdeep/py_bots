import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from enum import Enum



from ..models import Valute, ValuteReport
from .convertor import Convertor


class ValuteFields(Enum):
    """доступные поля в xml для 1 элемента"""
    num_code = 'NumCode'
    char_code= 'CharCode'
    nominal = 'Nominal'
    v_name = 'Name'
    v_value = 'Value'
    vunit_rate = 'VunitRate'


class DocumentHeaderFields(Enum):
    date = 'Date'

    # NOTE: not used
    # name = 'name'


class ValuteParser:

    _valute_parsers_map = {
        ValuteFields.num_code.value:  (Convertor.extract_str, 'num_code'),
        ValuteFields.char_code.value: (Convertor.extract_str, 'char_code'),
        ValuteFields.nominal.value: (Convertor.extract_int, 'nominal'),
        ValuteFields.v_name.value: (Convertor.extract_str, 'name'),
        ValuteFields.v_value.value: (Convertor.extract_float, 'value'),
        ValuteFields.vunit_rate.value: (Convertor.extract_float, 'vunit_rate'),
    }

    @classmethod
    def parse_valute_document(cls, document: str) -> ValuteReport:
        
        result: list[Valute] = []
        tree = ET.fromstring(document)

        date_value = cls._parse_document_date(tree)

        for valute in tree:
            r = cls._parse_valute(valute)
            result.append(r)

        return ValuteReport(date=date_value, valutes=result)

    @classmethod
    def _parse_valute(cls, valute: Element) -> Valute:

        result = {}
        for data in valute:
            if data.tag in cls._valute_parsers_map:
                convertor, model_name = cls._valute_parsers_map[data.tag]
                result[model_name] = convertor(data.text)


        return Valute(**result)

    
    @classmethod
    def _parse_document_date(cls, el: Element):
        data = el.attrib

        date_str = data[DocumentHeaderFields.date.value]

        dd, mm, yy = date_str.split('.')

        return f'{yy}.{mm}.{dd}'

