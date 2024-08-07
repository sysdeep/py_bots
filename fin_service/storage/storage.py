from dataclasses import asdict
from datetime import datetime

from tinydb import TinyDB

from .models import Valute


class Storage:
    def __init__(self, storage_path: str) -> None:
        self._db = TinyDB(storage_path)
        self._table_valutes = self._db.table("valutes")

    def insert_valute(self, valute: Valute):
        data = asdict(valute)
        # data["date"] = datetime.now().isoformat()
        self._table_valutes.insert(data)

    def get_valutes(self) -> list[Valute]:
        valutes = self._table_valutes.all()
        print(valutes)
        return []


if __name__ == "__main__":

    storage = Storage("/tmp/test_valutes_storage.json")

    storage.get_valutes()

    valute1 = Valute(
        name="name",
        value=11.22,
        num_code="034",
        char_code="RU",
        nominal=1,
        vunit_rate=11.22,
        date="date",
    )
    storage.insert_valute(valute1)

    storage.get_valutes()
