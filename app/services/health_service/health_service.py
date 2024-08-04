from dataclasses import dataclass

import psutil


@dataclass
class DiskUsage:
    total: int
    userd: int
    free: int
    percent: float  # used prc


@dataclass
class DiskPartition:
    device: str
    mount_point: str
    fstype: str
    usage: DiskUsage


@dataclass
class Health:
    cpu_count: int
    mem_prc: float
    disk_info: list[DiskPartition]
    boot_time: float


class HealthService:
    def __init__(self) -> None:
        pass

    def get_health(self) -> Health:

        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        memory.percent

        boot_time = psutil.boot_time()

        parts_info = self._get_hdd_info()

        return Health(
            cpu_count=cpu_count,
            mem_prc=memory.percent,
            disk_info=parts_info,
            boot_time=boot_time,
        )

    @classmethod
    def _get_hdd_info(cls) -> list[DiskPartition]:
        partitions = psutil.disk_partitions(all=False)

        result: list[DiskPartition] = []
        for part in partitions:

            du = psutil.disk_usage(part.mountpoint)

            usage = DiskUsage(
                total=du.total, userd=du.used, free=du.free, percent=du.percent
            )
            disk_part = DiskPartition(
                device=part.device,
                mount_point=part.mountpoint,
                fstype=part.fstype,
                usage=usage,
            )
            result.append(disk_part)

        return result


if __name__ == "__main__":

    service = HealthService()
    health = service.get_health()
    print(health)
