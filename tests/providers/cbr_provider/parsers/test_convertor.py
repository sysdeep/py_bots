from app.providers.cbr_provider.parsers.convertor import Convertor

import pytest


@pytest.mark.parametrize('payload, expected', [
    ['foo', 'foo'],
])
def test_extract_text(payload, expected):

    assert Convertor.extract_str(payload) == expected


@pytest.mark.parametrize('payload, expected', [
    ('1,23', 1.23),
    ('1.23', 1.23),
    ('0.23', 0.23),
])
def test_extract_float(payload, expected):

    assert Convertor.extract_float(payload) == expected


@pytest.mark.parametrize('payload, expected', [
    ('1', 1),
    ('0', 0),
])
def test_extract_int(payload, expected):

    assert Convertor.extract_float(payload) == expected


