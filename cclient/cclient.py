from enum import Enum

import requests

from .cclient_settings import CClientSettings


class Service(Enum):
    wireguard = "eev3gu7A"
    nginx = "usahgaL0"


class Action(Enum):
    status = "shiKaip2"
    start = "xaequ9Ai"
    stop = "ahtaet1X"
    restart = "ooZ1aega"


class CClient:
    def __init__(self, settings: CClientSettings):
        self._settings = settings

    @property
    def settings(self) -> CClientSettings:
        return self._settings

    def service(self, service_name: Service, action: Action) -> str:

        url = f"http://{self._settings.server}/api/system/service/{service_name.value}/{action.value}"

        headers = {"Authorization": f"Bearer {self._settings.token}"}

        res = requests.get(url, timeout=100, headers=headers)
        res.raise_for_status()

        return res.text


if __name__ == "__main__":
    with open("../secrets/token_rsa") as fd:
        token = fd.read()

    c = CClient(CClientSettings(server="localhost:7788", token=token.rstrip(), name="test"))
    r = c.service(Service.nginx, Action.status)
    print(r)
