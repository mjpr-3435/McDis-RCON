import os


def clear_cmd() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
