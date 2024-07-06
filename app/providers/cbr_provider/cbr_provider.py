
import requests


class CbrProvider:
    def __init__(self):
        pass

    def get_valute(self):
        """
        <Valute ID="R01010">
        <NumCode>036</NumCode>
        <CharCode>AUD</CharCode>
        <Nominal>1</Nominal>
        <Name>Австралийский доллар</Name>
        <Value>59,4582</Value>
        <VunitRate>59,4582</VunitRate>
    </Valute>

        """
        url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2024'

        r = requests.get(url)
        r.raise_for_status()


        return url

    
    def get_metalls(self):
        url = 'https://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/07/2001&date_req2=13/07/2001'

        return url


if __name__ == '__main__':

    p = CbrProvider()

    print(p.get_valute())
