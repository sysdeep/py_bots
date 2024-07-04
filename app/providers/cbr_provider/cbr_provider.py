
class CbrProvider:
    def __init__(self):
        pass

    def get_money(self, for_date):
        url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2024'
        return url

    
    def get_metalls(self):
        url = 'https://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/07/2001&date_req2=13/07/2001'

        return url
