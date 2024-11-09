from ..modules import *

def truncate (string: str, max_lenght:int) -> str:
    string = string if len(string) < max_lenght else f'{string[:max_lenght-3]}...'
    return string

async def excute_and_wait(function: Callable, *, args: tuple = tuple(), kwargs: dict = dict()):
    task = threading.Thread(target = function, args = args, kwargs = kwargs)
    task.start()

    while task.is_alive():
        await asyncio.sleep(1)

async def excute(function: Callable, *, args: tuple = tuple(), kwargs: dict = dict()):
    threading.Thread(target = function, args = args, kwargs = kwargs).start()