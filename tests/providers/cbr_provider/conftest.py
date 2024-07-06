import os
from pathlib import Path

import pytest

@pytest.fixture
def cbr_data_dir() -> Path:
    return Path(os.path.realpath(__file__)).parent / 'data'


@pytest.fixture
def load_cbr_file(cbr_data_dir):

    def _inner(file_name: str):
        file_path = cbr_data_dir / file_name
        return file_path.read_text()

    return _inner
