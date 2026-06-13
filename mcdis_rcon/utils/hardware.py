import math
from collections.abc import Mapping, Sequence
from typing import Protocol, cast

import psutil


class TemperatureSensor(Protocol):
    label: str
    current: float


def get_cpu_temp() -> str:
    try:
        temps = cast(
            Mapping[str, Sequence[TemperatureSensor]],
            psutil.sensors_temperatures(),  # type: ignore[attr-defined]
        )
        for sensor in ['coretemp', 'k10temp']:
            if sensor in temps:
                for temp in temps[sensor]:
                    if (
                        'package id' in temp.label.lower()
                        or 'tdie' in temp.label.lower()
                        or 'tctl' in temp.label.lower()
                    ):
                        return f'{int(temp.current)} °C'
        return '—— °C'
    except Exception:
        return '—— °C'


def ram_usage(process: psutil.Process, string: bool = True) -> str | float:
    try:
        total = process.memory_info().rss
        magnitude = ['B', 'KB', 'MB', 'GB', 'TB']
        i = int(math.log(total, 1024)) if total != 0 else 0

        if not string:
            return float(total / (1024**i))
        else:
            return f'{total / (1024**i):.1f} {magnitude[i]}'
    except Exception:
        if not string:
            return 0
        else:
            return '———'
