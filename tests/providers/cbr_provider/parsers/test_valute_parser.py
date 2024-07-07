from dataclasses import asdict

import pytest

from app.providers.cbr_provider.parsers.valute_parser import ValuteParser



def test_valute_parser_document(load_cbr_file):
    
    data = load_cbr_file('valute.xml')
    result = ValuteParser.parse_valute_document(data)

    assert len(result.valutes)

    # NOTE: кривовато..
    expected_date = '2024.07.06'
    assert result.date == expected_date


# one sample test -------------------------------------------------------------
ONE_SAMPLE_XML = """
<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="06.07.2024" name="Foreign Currency Market">
  <Valute ID="R01010">
    <NumCode>036</NumCode>
    <CharCode>AUD</CharCode>
    <Nominal>1</Nominal>
    <Name>Австралийский доллар</Name>
    <Value>59,3500</Value>
    <VunitRate>59,35</VunitRate>
  </Valute>
</ValCurs>
"""

ONE_SAMPLE_EXPECTED = {

    "name": "Австралийский доллар",
    "value": 59.35, 
    "num_code": "036",
    "char_code": "AUD",
    "nominal": 1,
    "vunit_rate": 59.35, 
}


@pytest.mark.parametrize('source, expected', [
    (ONE_SAMPLE_XML, ONE_SAMPLE_EXPECTED),
])
def test_valute_parse_sample(source, expected):
    
    
    result = ValuteParser.parse_valute_document(source.strip())

    assert len(result.valutes) == 1
    assert asdict(result.valutes[0]) == expected




