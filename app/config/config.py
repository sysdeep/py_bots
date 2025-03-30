from dataclasses import dataclass


@dataclass
class VPS:
    name: str
    address: str


@dataclass
class Config:
    cc_access_token: str        # path to cc token
    vps: list[VPS]
