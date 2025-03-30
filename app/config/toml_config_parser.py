import toml

from .config_parser import ConfigParser
from .config import Config, VPS


class TomlConfigParser(ConfigParser):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def parse(self) -> Config:
        with open(self._file_path, "r", encoding="utf8") as fd:
            data = toml.load(fd)

        cc_access_token = data["main"]["cc_access_token"]

        vps_list = []
        for vps_dict in data.get('vps', []):
            vps = VPS(address=vps_dict["address"], name=vps_dict["name"])
            vps_list.append(vps)

        return Config(cc_access_token=cc_access_token, vps=vps_list)
