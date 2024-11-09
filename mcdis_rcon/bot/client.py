from .pm_functions import *
from .modules import *

from .loader import _, config, find_panel

first_start = True
client = commands.Bot(command_prefix='$', intents = discord.Intents().all())

def run_client():
    try:
        client.run(config['Bot Token'])
    except Exception as error:
        print(_('Error while running discord client: {}').format(error))
        os._exit(0)

@client.event
async def on_ready():
    global first_start
    
    if first_start:
        first_start = False
        find_panel(client)

        print(_('Logged in as {}!').format(client.user))

        try: 
            from .pm_loader import pm_load
            await pm_load(client)
        except Exception as error:
            print(_('There was an error while loading McDis-RCON.'))
            print(_('Error: {}').format(error))
            os._exit(0)

        if config['Booleans']['allow flask']:
            from .pm_loader import flask_manager
            await flask_manager.start()

        signal.signal(signal.SIGINT, signal_handler)

@client.event
async def on_message(message: discord.Message):
    from .loader import panel
    if not panel: return
    
    from .pm_behaviours import pm_on_message
    await pm_on_message(client, message)