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

async def call_addons(function: str, args: tuple):
    from ..pm_loader import addons, flask_manager, processes, servers, networks, panel
    extras = {"flask_manager" : flask_manager,
              "processes"     : processes,
              "networks"      : networks,
              "servers"       : servers,
              "panel"         : panel}
    
    for addon in addons:
        try:
            try: func = getattr(addon, 'call_behaviours')
            except AttributeError: continue
        
            await func(function, args, extras)
        except: 
            print(f'Error in {function}() of {addon.__name__}:\n{traceback.format_exc()}\n')