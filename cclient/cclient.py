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

    def service(self, service_name: Service, action: Action) -> str:

        url = f'http://{self._settings.server}/api/system/service/{service_name.value}/{action.value}'

        res = requests.get(url, timeout=100)
        res.raise_for_status()

        return res.text


if __name__ == "__main__":
    c = CClient(CClientSettings(server="localhost:7788"))
    r = c.service(Service.nginx, Action.status)
    print(r)
