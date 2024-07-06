
from app.providers.cbr_provider.parser import Parser



def test_parse_valute(load_cbr_file):
    
    data = load_cbr_file('valute.xml')
    
    result = Parser.parse_valute_document(data)

    print(result)
    assert True


