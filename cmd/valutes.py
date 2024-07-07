
from app.services.fin_service.fin_service import FinService


NEED_VALUTES = ['USD', 'EUR']

def main():
    service = FinService()
    valutes_result = service.get_valute()

    print(f'Valutes on {valutes_result.date}:')
    for v in valutes_result.valutes:
        trend_sign = '+' if v.trend > 0 else '-'
        print(f'\t{v.char_code}: {v.value:.2f} {trend_sign}{abs(v.trend):.2f}')



if __name__ == '__main__':

    main()
