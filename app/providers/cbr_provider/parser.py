import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from .models import Valute

class Parser:

    @classmethod
    def parse_valute_document(cls, document: str) -> list[Valute]:
        
        result: list[Valute] = []
        tree = ET.fromstring(document)
        print(tree)

        for valute in tree:
            print(valute)
            
            r = cls._parse_valute(valute)
            result.append(r)
            print(r)
                    # root = tree.getroot()
        # print(root)

        return result

    @classmethod
    def _parse_valute(cls, valute: Element) -> Valute:
        char_code = ''
        name = ''
        value = 0.0
        for data in valute:
        
            if data.tag == 'CharCode':
                char_code = str(data.text)

            if data.tag == 'Value':
                value = str(data.text)

            if data.tag == 'Name':
                name = str(data.text)

        return Valute(name=name, code=char_code, value=value)

