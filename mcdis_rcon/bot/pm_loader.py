from .pm_functions import *
from .pm_classes import *
from .pm_banner import *
from .modules import *

from .loader import _, config, panel

flask_manager                               = None
processes   : list[Union[Network,Server]]   = []
networks    : list[Network]                 = []
servers     : list[Server]                  = []

async def pm_load(client: commands.Bot):
    global flask_manager

    print(_('Loading Processes Manager:'))
    
    for name in config['Processes']['Servers']:
        server = Server(name, client, config['Processes']['Servers'][name])
        processes.append(server)
        servers.append(server)

    for name in config['Processes']['Networks']:
        network = Network(name, client, config['Processes']['Networks'][name])
        processes.append(network)
        networks.append(network)

    processes_objects = "\n".join([f'     -> {process.name}      \t{type(process)}' for process in processes])
    print(_('   • Creating objects:\n{}').format(processes_objects))
        
    for process in processes:
        await thread(f'Console {process.name}', panel, public = True)
    await thread(f'Error Reports', panel, public = True)
    
    print(_('   • Loaded Server Panel'))

    if config['Booleans']['allow flask']: 
        flask_manager = FlaskServerManager()

    asyncio.create_task(banner_creator(client))
    print(_('Loading Complete\n'))