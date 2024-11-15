from ..modules import *

async def execute_and_wait(function: Callable, *, args: tuple = tuple(), kwargs: dict = dict()):
    task = threading.Thread(target = function, args = args, kwargs = kwargs)
    task.start()

    while task.is_alive():
        await asyncio.sleep(1)

async def execute(function: Callable, *, args: tuple = tuple(), kwargs: dict = dict()):
    threading.Thread(target = function, args = args, kwargs = kwargs).start()