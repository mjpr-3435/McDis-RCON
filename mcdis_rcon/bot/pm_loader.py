from .pm_functions import *
from .pm_classes import *
from .pm_banner import *
from .modules import *

from .loader import _, config, panel

addons                                      = []
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

    await load_addons(client)

    if config['Booleans']['allow flask']: 
        flask_manager = FlaskServerManager()

    asyncio.create_task(banner_creator(client))
    print(_('   • Loaded Server Panel'))
    print(_('Loading Complete\n'))

async def load_addons(client: commands.Bot):
    global addons
    
    md_plugins_dir = '.mdaddons'
    os.makedirs(md_plugins_dir, exist_ok = True)
    addons_dirs = [dir for dir in os.listdir(md_plugins_dir) if os.path.exists(os.path.join(md_plugins_dir, dir, '__init__.py'))]
    if not addons_dirs: return
    
    print(_('   • Importing addons:'))
    sys.path.insert(0, md_plugins_dir)
    for addon_dir in addons_dirs:
        try:
            package_spec = importlib.util.spec_from_file_location(addon_dir, os.path.join(md_plugins_dir, addon_dir, '__init__.py'))
            mod = importlib.util.module_from_spec(package_spec)
            package_spec.loader.exec_module(mod)
            addons.append(mod)
            print(_('     -> Imported \t{}').format(os.path.basename(addon_dir)))
        except:
            print(_('     -> Unable to import {}\n{}').format(os.path.basename(addon_dir), traceback.format_exc()))
            os._exit(0)
    
    sys.path.pop(0)

    for addon_dir in addons:
        try:
            try: func = getattr(addon_dir, 'load')
            except AttributeError: continue
        
            await func(client)
        except: 
            print(_('Error in load() of {}:\n{}\n').format(addon_dir.__name__, traceback.format_exc()))
            os._exit(0)