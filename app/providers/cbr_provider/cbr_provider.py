from datetime import datetime
import requests

from .models import ValuteReport
from .parsers.valute_parser import ValuteParser


class CbrProvider:
    def __init__(self):
        pass

    def get_valute(self, for_date: datetime | None = None) -> ValuteReport:


        # NOTE: for date - pass deq_date
        # url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2024'

        url = 'https://www.cbr.ru/scripts/XML_daily.asp'

        if for_date:
            req_date = for_date.strftime('%d/%m/%Y')
            url += f'?date_req={req_date}'


        r = requests.get(url)
        r.raise_for_status()
        
        report = ValuteParser.parse_valute_document(r.text)

        return report

    
    def get_metalls(self):
        url = 'https://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/07/2001&date_req2=13/07/2001'

        return url


if __name__ == '__main__':

    p = CbrProvider()

    print(p.get_valute())
