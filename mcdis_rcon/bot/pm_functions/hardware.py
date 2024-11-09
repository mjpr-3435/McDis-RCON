from ..modules import *

def get_cpu_temp() -> str:
    try:
        temps = psutil.sensors_temperatures()

        if 'coretemp' in temps:
            for temp in temps['coretemp']:
                if 'package id' in temp.label.lower():
                    return f'{int(temp.current)} °C'
    except:
        return f'—— °C'
    
def ram_usage(process: psutil.Process) -> str:
    try:
        total = process.memory_info().rss
        magnitude = ['B', 'KB', 'MB', 'GB', 'TB']
        i = int(math.log(total, 1024)) if total != 0 else 0

        return f'{total / (1024 ** (i)) :.1f} {magnitude[i]}'
    except:
        return '———'