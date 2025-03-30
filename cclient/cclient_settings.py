from dataclasses import dataclass


@dataclass
class CClientSettings:
    name: str
    server: str  # server address: server:123
    token: str  # jwt access token
