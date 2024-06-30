from dataclasses import dataclass

import psutil


@dataclass
class Health:
    cpu_count: int
    mem_prc: float


class HealthService:
    def __init__(self) -> None:
        pass

    def get_health(self) -> Health:

        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        memory.percent

        return Health(cpu_count=cpu_count, mem_prc=memory.percent)
