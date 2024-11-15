from ..modules import *
from ..utils import *

from .Network import Network
from .Server import Server
from .Flask import FlaskManager

class McDisClient(commands.Bot):
    def __init__(self):
        super().__init__(blank_space, intents = discord.Intents().all())
        self.config     : dict                                  = {}
        self.panel      : discord.TextChannel                   = None
        self._          : gettext.GNUTranslations.gettext       = None
        self.path_backups                                       = '.mdbackups'
        self.path_addons                                        = '.mdaddons'
        self.addons                                             = []
        self.flask      : FlaskManager                          = None
        self.processes  : list[Union[Network,Server]]           = []
        self.networks   : list[Network]                         = []
        self.servers    : list[Server]                          = []
        
        os.makedirs(self.path_backups, exist_ok = True)
        os.makedirs(self.path_addons , exist_ok = True)
        
        self.load_config()

        try:
            self.run(self.config['Bot Token'])
        except Exception as error:
            print(self._('Error while running discord client: {}').format(error))
            os._exit(0)
        
    def load_config             (self):
        try:
            with open('md_config.yml', "r+") as file:
                yaml = ruamel.yaml.YAML()
                yaml.indent(mapping = 2, sequence = 4, offset = 2)
                yaml.preserve_quotes = True

                self.config = yaml.load(file)

        except Exception as error:
            print('The file \'md_config.yml\' could not be opened.')
            print(f'Error: {error}')
            os._exit(0)

        try:
            if      not isinstance(self.config['Bot Token'], str):
                print('The \'Bot Token\' variable must be a string.')
                os._exit(0)

            elif    not isinstance(self.config['Panel ID'], int):
                print('The \'Panel ID\' variable must be an integer.')
                os._exit(0)

            elif    not self.config['Language'] in allowed_languages:
                print(f'The \'Language\' variable must be one of the following: {", ".join(allowed_languages)}.')
                os._exit(0)

            elif    not isinstance(self.config['Backups'], int):
                print(f'The \'Backups\' variable must be an integer between 1 and 5.')
                os._exit(0)

            elif    not self.config['Backups'] in list(range(1,6)):
                print(f'The \'Backups\' variable must be between 1 and 5, not {self.config["Backups"]}.')
                os._exit(0)

            elif    not isinstance(self.config['Flask']['Allow'], bool):
                print('The \'Flask: Allow\' variable must be a boolean.')
                os._exit(0)

            elif    not self.config['Flask']['Allow']:
                pass

            elif    not isinstance(self.config['Flask']['IP'], str):
                print('The \'Flask: IP\' variable must be a string.')
                os._exit(0)

            elif    not isinstance(self.config['Flask']['Port'], int):
                print('The \'Flask: Port\' variable must be an integer.')
                os._exit(0)
            
            names = []
            
            for process_type in self.config['Processes']:
                if self.config['Processes'][process_type] == None: 
                    self.config['Processes'][process_type] = []
                    continue

                for process in self.config['Processes'][process_type]:
                    process_config = self.config['Processes'][process_type][process]

                    if not isinstance(process, str):
                        print(f'{process}: The process names must be string.')
                        os._exit(0)

                    elif len(process) > 40:
                        print(f'{process}: The process name must not exceed 40 characters.')
                        os._exit(0)

                    elif process in [self.path_backups, self.path_addons]:
                        print(f'{process}:  A process cannot be named \'{self.path_backups}\' or \'{self.path_addons}\'.')
                        os._exit(0)
                    
                    elif process.lower() in names:
                        print(f'You can\'t have two processes with the same name: {process}')
                        os._exit(0)

                    elif not is_valid_path_name(process):
                        print(f'{process}: Process names can only contain letters, numbers, periods (.), hyphens (-), underscores (_), and spaces.')
                        os._exit(0)

                    elif not isinstance(process_config['start_command'], str):
                        print(f'{process}: The \'start_command\' variable must be a string.')
                        os._exit(0)
                    
                    elif not isinstance(process_config['stop_command'], str):
                        print(f'{process}: The \'start_command\' variable must be a string.')
                        os._exit(0)

                    elif not all([isinstance(x,str) for x in process_config['relay_blacklist']]):
                        print(f'{process}: The \'relay_blacklist\' variable must be a list of strings.')
                        os._exit(0)
                    
                    names.append(process.lower())
                        
        except KeyError as error:
            print(f'Key not found: {error}.\n'
                  f'Your \'md_config.yml\' file is incomplete.\n'
                  f'Please try requesting another one using \'mcdis init\'.')
            os._exit(0)
        
        locales_dir = os.path.join(package_path, 'locales')

        if self.config['Language'] != 'en':
            lang = gettext.translation('app', localedir = locales_dir, languages = [self.config['Language']])
        else:
            lang = gettext.NullTranslations()

        lang.install()
        self._ = lang.gettext

        print(self._('Your configuration has been loaded successfully.'))

    def find_panel              (self):
        panel_id = self.config['Panel ID']
        self.panel = self.get_channel(panel_id)
            
        if self.panel == None: 
            print(self._('Error: Channel with id {} not found.').format(panel_id))
            os._exit(0)
        elif not isinstance(self.panel, discord.TextChannel): 
            print(self._('Error: The panel channel must be a text channel.'))
            os._exit(0)
    
    def on_stop                 (self):
        any_process_open = lambda: any([process.state() in ['Open', 'Initializing'] for process in self.processes])
        
        if any_process_open():
            print(self._('Closing processes...'))

            for process in  self.processes:
                process.stop(omit_tasks=True)
            
            i = 60
            while i > 0 and any_process_open():
                print(self._('Processes will be forcibly closed in {} seconds...').format(i))
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
                i -= 1
                time.sleep(1)
                
            if any_process_open():
                for process in self.processes:
                    process.kill()
                
                print(self._('Processes forcibly closed.'))
            else:
                print(self._('Processes closed.'))
        os._exit(0)
    
    async def load_processes    (self):
        print(self._('Loading Processes Manager:'))
        
        for name in self.config['Processes']['Servers']:
            server = Server(name, self, self.config['Processes']['Servers'][name])
            self.processes.append(server)
            self.servers.append(server)

        for name in self.config['Processes']['Networks']:
            network = Network(name, self, self.config['Processes']['Networks'][name])
            self.processes.append(network)
            self.networks.append(network)

        processes_objects = "\n".join([f'     -> {process.name}      \t{type(process)}' for process in self.processes])
        print(self._('   • Creating objects:\n{}').format(processes_objects))
            
        for process in self.processes:
            await thread(f'Console {process.name}', self.panel, public = True)
        await thread(f'Error Reports', self.panel, public = True)

    async def load_addons       (self):
        addons = [dir for dir in os.listdir(self.path_addons) if os.path.exists(os.path.join(self.path_addons, dir, '__init__.py'))]
        if not addons: return
        
        print(self._('   • Importing addons:'))
        sys.path.insert(0, self.path_addons)
        
        for addon in addons:
            try:
                package_spec = importlib.util.spec_from_file_location(addon, os.path.join(self.path_addons, addon, '__init__.py'))
                mod = importlib.util.module_from_spec(package_spec)
                package_spec.loader.exec_module(mod)
                self.addons.append(mod)
                print(self._('     -> Imported \t{}').format(os.path.basename(addon)))
            except:
                print(self._('     -> Unable to import {}\n{}').format(os.path.basename(addon), traceback.format_exc()))
                os._exit(0)
        
        sys.path.pop(0)

        await self.call_addons('load', args = tuple(), exit = True)

    async def load_behaviours   (self):
        behaviours_dir = os.path.join(package_path, 'behaviours')

        scripts = [filename for filename in os.listdir(behaviours_dir)]

        for script in scripts:
            await self.load_extension(f'mcdis_rcon.behaviours.{script[:-3]}')

    async def call_addons       (self, function: str, *, args: tuple, exit: bool = False):
        args = (self,) + args

        for addon in self.addons:
            try:
                try: func = getattr(addon, 'call_behaviours')
                except AttributeError: continue
            
                await func(function, args)
            except: 
                print('Error in {}() of {}:\n{}\n'.format(function, addon.__name__, traceback.format_exc()))
                if exit: os._exit(0)

    async def on_ready          (self):
        from ..banners import banner_creator

        self.find_panel(self)

        print(self._('Logged in as {}!').format(self.user))

        try: 
            await self.load_processes(self)
            await self.load_addons(self)
            await self.tree.sync()
            if self.config['Flask']['Allow']: 
                self.flask = FlaskManager()
        except Exception as error:
            print(self._('There was an error while loading McDis-RCON.'))
            print(self._('Error: {}').format(error))
            os._exit(0)

        asyncio.create_task(banner_creator(self))
        print(self._('   • Loaded Server Panel'))
        print(self._('Loading Complete\n'))

        signal_handler = lambda sig, frame: threading.Thread(target = self.on_stop, args = (self,)).start()
        
        signal.signal(signal.SIGINT, signal_handler)







""" 
async def pm_on_message(client: commands.Bot, message: discord.Message):
    from ..pm_banner import banner_creator

    if message.author.bot: return

    for process in processes: await process.discord_listener(message)

    if message.channel.id == panel.id:
        if message.content.lower() == f'{mcdis_prefix}start-all':
            await message.delete()
            for process in processes: process.start()

            await asyncio.sleep(1)
            asyncio.create_task(banner_creator(client, loop = False, views = False))
                
        elif message.content.lower() == f'{mcdis_prefix}stop-all':
            await message.delete()
            for process in processes: process.stop()
                            
        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}start':
            process_name = message.content.removeprefix(f'{mcdis_prefix}start').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()
            
            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}start <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            else:
                if process.state() != 'Closed':
                    await message.channel.send(f"✖ El servidor ya estaba abierto...")
                    return
                
                await message.channel.send(f"[{process.name}] Abriendo servidor...")
                process.start()

        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}stop':
            process_name = message.content.removeprefix(f'{mcdis_prefix}start').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()
            
            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}stop <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            else:
                if process.state() == 'Closed':
                    await message.channel.send(f"✖ El servidor no estaba abierto...")
                    return
                
                await message.channel.send(f"[{process.name}] Cerrando servidor...")
                process.stop()
        
        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}kill':
            process_name = message.content.removeprefix(f'{mcdis_prefix}kill').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()
            
            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}stop <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            else:
                if process.state() == 'Closed':
                    await message.channel.send(f"✖ El servidor no estaba abierto...")
                    return
                
                await message.channel.send(f"[{process.name}] Reiniciando servidor...")
                await process.kill()

        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}restart':
            process_name = message.content.removeprefix(f'{mcdis_prefix}restart').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()
            
            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}stop <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            else:
                if process.state() == 'Closed':
                    await message.channel.send(f"✖ El servidor no estaba abierto...")
                    return
                
                await message.channel.send(f"[{process.name}] Reiniciando servidor...")
                await process.restart()

        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}reload mdplugins':
            process_name = message.content.removeprefix(f'{mcdis_prefix}reload mdplugins').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()
            
            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}stop <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            else:
                if process.state() == 'Closed':
                    await message.channel.send(f"✖ El servidor no estaba abierto...")
                    return
                
                await message.channel.send(f"[{process.name}] mdplugins recargados.")
                process.load_plugins(reload = True)
        
        elif message.content.lower().split(' ')[0] == f'{mcdis_prefix}mk-bkp':
            process_name = message.content.removeprefix(f'{mcdis_prefix}mk-bkp').strip().lower()
            process = next(filter(lambda x: process_name == x.name.lower(), processes), None)

            await message.delete()

            if not process:
                response = await message.channel.send(content = _('✖ Specify the process. E.g.: `{}mk-bkp <name>`.').format(mcdis_prefix))
                await response.delete(delay = 5)
                return
            elif process.disk_usage(string = False) > psutil.disk_usage("/").free:
                response = await message.channel.send(content = _('✖ There\'s not enough space on the disk to create the backup.'))
                await response.delete(delay = 5)
                return

            elif process.state() != 'Closed':
                response = await message.channel.send(content = _('✖ The process must be closed to create the `.zip`.'))
                await response.delete(delay = 5)
                return
            
            response = await message.channel.send(_('`[{}]`: Compressing files...').format(process.name))
            
            counter = [0,0]
            task = threading.Thread(target = process.make_bkp, kwargs = {'counter' : counter})
            task.start()

            while task.is_alive():
                if counter[1] == 0: 
                    await asyncio.sleep(0.1)
                else:
                    show = _('`[{}]`: `[{}/{}]` files have been compressed...').format(process.name, counter[0], counter[1])
                    await response.edit(content = show)
                    await asyncio.sleep(0.5)

            await response.edit(content = _('✔ The files have been successfully compressed.'))
            await response.delete(delay = 5)

            await message.author.send(_('✔ The files have been successfully compressed.'))

"""
