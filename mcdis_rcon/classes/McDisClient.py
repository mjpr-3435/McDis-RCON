from ..modules import *
from ..utils import *

class McDisClient(commands.Bot):
    def __init__(self):
        super().__init__(blank_space, intents = discord.Intents().all())
        from .Uploader import Uploader
        from .Network import Network
        from .Server import Server
        from .Flask import FlaskManager
        
        self.prefix                                             = '!!'
        self.cwd                                                = os.getcwd()
        self.config     : dict                                  = {}
        self.panel      : discord.TextChannel                   = None
        self._          : Callable[[str], str]                  = None
        self.path_backups                                       = '.mdbackups'
        self.path_addons                                        = '.mdaddons'
        self.path_addons_configs                                = os.path.join('.mdaddons', 'configs')
        self.addons                                             = {}
        self.flask      : FlaskManager                          = None
        self.processes  : list[Union[Network,Server]]           = []
        self.networks   : list[Network]                         = []
        self.servers    : list[Server]                          = []
        self.uploader                                           = Uploader()
        self.is_running                                         = False
        self.display_panel                                      = False

        os.makedirs(self.path_backups        , exist_ok = True)
        os.makedirs(self.path_addons         , exist_ok = True)
        os.makedirs(self.path_addons_configs , exist_ok = True)
        
        self._load_config()

        try:
            self.run(self.config['Bot Token'])
        except Exception as error:
            print(self._('Error while running discord client: {}').format(error))
            os._exit(0)

    ###         Loaders             ###

    def         _load_config           (self):
        try:
            self.config = read_yml('md_config.yml')

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

                    elif process in [self.path_backups, self.path_addons, 'Flask']:
                        print(f'{process}:  A process cannot be named \'{self.path_backups}\', \'{self.path_addons}\' or Flask.')
                        os._exit(0)
                    
                    elif process.lower() in names:
                        print(f'You can\'t have two processes with the same name: {process}')
                        os._exit(0)

                    elif not is_valid_path_name(process):
                        print(f'{process}: Process names can only contain letters, numbers, periods (.), hyphens (-), underscores (_), and spaces.')
                        os._exit(0)

                    elif not isinstance(process_config['start_cmd'], str):
                        print(f'{process}: The \'start_cmd\' variable must be a string.')
                        os._exit(0)
                    
                    elif not isinstance(process_config['stop_cmd'], str):
                        print(f'{process}: The \'start_cmd\' variable must be a string.')
                        os._exit(0)

                    elif process_config['blacklist'] == None:
                        process_config['blacklist'] = []

                    elif not all([isinstance(x,str) for x in process_config['blacklist']]):
                        print(f'{process}: The \'blacklist\' variable must be a list of strings.')
                        os._exit(0)
                    
                    names.append(process.lower())
                        
        except KeyError as error:
            print(f'\n\nKey not found: {error}.\n\n'
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

    def         _load_panel            (self):
        panel_id = self.config['Panel ID']
        self.panel = self.get_channel(panel_id)
            
        if self.panel == None: 
            print(self._('Error: Channel with id {} not found.').format(panel_id))
            os._exit(0)
        elif not isinstance(self.panel, discord.TextChannel): 
            print(self._('Error: The panel channel must be a text channel.'))
            os._exit(0)
        
    async def   _load_processes        (self):
        from .Network import Network
        from .Server import Server

        for name in self.config['Processes']['Servers']:
            server = Server(name, self, self.config['Processes']['Servers'][name])
            self.processes.append(server)
            self.servers.append(server)

        for name in self.config['Processes']['Networks']:
            network = Network(name, self, self.config['Processes']['Networks'][name])
            self.processes.append(network)
            self.networks.append(network)

        processes_objects = "\n".join([f'     -> {process.name}' for process in self.processes])
        if self.processes: print(self._('   • Creating objects\n{}').format(processes_objects))
            
        for process in self.processes:
            await thread(f'Console {process.name}', self.panel, public = True)
        await thread('Error Reports', self.panel, public = True)
        await thread('Console Flask', self.panel, public = True)

    async def   _load_addons           (self, *, reload: bool = False):
        if reload: self.unload_addons()
        
        files_in_addons_dir = os.listdir(self.path_addons)
                
        valid_extensions = ['.py', '.mcdis']
        cond = lambda file: os.path.splitext(file)[1] in valid_extensions
        
        addons = [file for file in files_in_addons_dir
                  if cond(file) or os.path.exists(os.path.join(self.path_addons, file, '__init__.py'))]

        if not addons: return

        if not reload: print(self._('   • Importing addons:'))

        for addon in addons:
            try:
                if addon.endswith('.py'):
                    addon_name = addon.removesuffix('.py')

                    module_path = os.path.join(self.path_plugins, addon)
                    spec = importlib.util.spec_from_file_location(addon.removesuffix('.py'), module_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                        
                elif os.path.isdir(os.path.join(self.path_addons, addon)):
                    addon_name = addon

                    module_path = os.path.join(self.path_addons, addon, '__init__.py')
                    spec = importlib.util.spec_from_file_location(addon, module_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                elif addon.endswith('.mcdis') and False:
                    addon_name = addon.removesuffix('.mcdis')

                    addon_path = os.path.join(self.path_addons, addon)
                    sys.path.insert(0, addon_path)

                    mod = importlib.import_module(f'mdaddon.__init__')

                    sys.path.pop(0)

                addon_instance = mod.mdaddon(self)
                self.addons[addon_name] = addon_instance

                if not reload: print(self._('     -> Imported {}').format(addon))
            except:
                if not reload: print(self._('     -> Unable to import {}').format(addon))

                await self.error_report(
                            title = f'Unable to import plugin {addon}',
                            error = traceback.format_exc(),
                            should_print = False
                        )

    async def   _load_behaviours       (self):
        behaviours_dir = os.path.join(package_path, 'behaviours')

        scripts = [filename for filename in os.listdir(behaviours_dir) if filename.endswith('.py')]

        for script in scripts:
            await self.load_extension(f'mcdis_rcon.behaviours.{script.removesuffix(".py")}')
    
    async def   _load_banner           (self, *, loop: bool = True, view: bool = True):
        from ..gui.Panel import PanelView, PanelEmbed
        first_iteration = True

        while loop or first_iteration:
            first_iteration = False
            file = None

            if os.path.exists('banner.png'): 
                file = discord.File('banner.png')
            
            try:
                messages =  [msg async for msg in self.panel.history(limit = None, oldest_first = True)]
                
                if not messages:
                    await self.panel.send(
                        embed = PanelEmbed(self), 
                        view = PanelView(self), 
                        file = file)

                elif not messages[0].author.id == self.user.id:
                    while messages:
                        await self.panel.purge()
                        messages =  [msg async for msg in self.panel.history(limit = None, oldest_first = True)]
                        
                    await self.panel.send(
                        embed = PanelEmbed(self), 
                        view = PanelView(self), 
                        file = file)

                elif not view:
                    await messages[0].edit(
                        embed = PanelEmbed(self), 
                        attachments = [file] if file else [])

                else:
                    await messages[0].edit(
                        embed = PanelEmbed(self), 
                        view = PanelView(self), 
                        attachments = [file] if file else [])

            except:
                await self.error_report(
                    title = 'Server Panel',
                    error = traceback.format_exc()
                )

            view = False
            await asyncio.sleep(15)
    
    ###         Behaviours          ###
    
    async def   on_ready                (self):
        from .Flask import FlaskManager
        if self.is_running: return
        
        self._load_panel()
        
        print(self._('Logged in as {}!').format(self.user))

        try:
            await self._load_processes()
            await self._load_addons()
            await self._load_behaviours()
            print(self._('   • Loaded Discord events'))
            self.flask = FlaskManager(self)

            asyncio.create_task(self._load_banner())
            print(self._('   • Loaded server panel'))
            print(self._('Loading Complete'))
  
        except Exception as error:
            print(self._('There was an error while loading McDis RCON.'))
            print(self._('Error: {}').format(error))
            os._exit(0)

        signal_handler = lambda sig, frame: threading.Thread(target = self.on_stop).start()
        
        signal.signal(signal.SIGINT, signal_handler)
        self.is_running = True

        await execute_and_wait(self.console_listener)

    def         console_listener        (self):
        
        while True:
            command = input('\n>>')
            asyncio.run_coroutine_threadsafe(self.console_interface(command), self.loop)
            time.sleep(3)

    async def   console_interface       (self, command: str):

        if   self.is_command(command.lower(), 'start-all'      , console = True):
            print(self._('✔ Initializing processes.'))

            for process in self.processes: 
                process.start()
                
        elif self.is_command(command.lower(), 'stop-all'       , console = True):
            print(self._('✔ Stopping processes.'))

            for process in self.processes: 
                process.stop()
                            
        elif self.is_command(command.lower(), 'kill-all'       , console = True):
            print(self._('✔ Forcibly stopped processes.'))

            for process in self.processes: 
                process.kill()
                            
        elif self.is_command(command.lower(), 'restart-all'    , console = True):
            print(self._('✔ Restarting processes...'))

            for process in self.processes: 
                await process.restart()
                            
        elif self.is_command(command.lower(), 'mdreload-all'   , console = True):
            print(self._('✔ Reloading mdplugins...'))

            for process in self.processes: 
                process.load_plugins(reload = True)
                            
        elif self.is_command(command.lower(), 'start'          , console = True):
            process_name = command.removeprefix('start').lower().strip()
            process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

            if not process:
                print(self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                        .format(self.prefix, 'start', self.prefix, 'start'))

            elif process.is_running():
                print(self._('✖ `[{}]`: The process was already open.').format(process.name).replace('`',''))
            
            else:
                print(self._('✔ `[{}]`: Initializing process.').format(process.name).replace('`',''))
                process.start()

        elif self.is_command(command.lower(), 'stop'           , console = True):
            process_name = command.removeprefix('stop').lower().strip()
            process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

            if not process:
                print(self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                        .format(self.prefix, 'stop', self.prefix, 'stop'))

            elif not process.is_running():
                print(self._('✖ `[{}]`: The process was not open.').format(process.name).replace('`',''))
            
            else:
                print(self._('✔ `[{}]`: Stopping process.').format(process.name).replace('`',''))
                process.stop()
        
        elif self.is_command(command.lower(), 'kill'           , console = True):
            process_name = command.removeprefix('kill').lower().strip()
            process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

            await command.delete()
            
            if not process:
                print(self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                        .format(self.prefix, 'kill', self.prefix, 'kill'))

            elif not process.is_running():
                print(self._('✖ `[{}]`: The process was not open.').format(process.name).replace('`',''))
            
            else:
                print(self._('✔ `[{}]`: Forcibly stopped process.').format(process.name).replace('`',''))
                process.kill()

        elif self.is_command(command.lower(), 'restart'        , console = True):
            process_name = command.removeprefix('restart').lower().strip()
            process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)
            
            if not process:
                print(self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                        .format(self.prefix, 'restart', self.prefix, 'restart'))

            elif not process.is_running():
                print(self._('✖ `[{}]`: The process was not open.').format(process.name).replace('`',''))
            
            else:
                print(self._('✔ `[{}]`: Restarting process...').format(process.name).replace('`',''))
                await process.restart()

        elif self.is_command(command.lower(), 'mdreload'       , console = True):
            process_name = command.removeprefix('mdreload').lower().strip()
            process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)
            
            if not process:
                print(self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                        .format(self.prefix, 'mdreload', self.prefix, 'mdreload'))

            elif not process.is_running():
                print(self._('✖ `[{}]`: The process was not open.').format(process.name).replace('`',''))
            
            else:
                print(self._('✔ `[{}]`: Reloading mdplugins...').format(process.name).replace('`',''))
                process.load_plugins(reload = True)

        elif self.is_command(command.lower(), 'status'       , console = True) and not self.display_panel:
            self.display_panel = True

            await self._load_banner(loop = False, view = False)

        elif self.is_command(command.lower(), 'exit'         , console = True):
            threading.Thread(target = self.on_stop).start()

        else:
            print(self._('✖ Invalid command `{}`.').format(command))
        
    async def   panel_interface         (self, message: discord.Message):
        if message.author.bot: 
            return

        if message.channel.id == self.panel.id:
            if   self.is_command(message.content.lower(), 'start-all'):
                await message.delete()

                response = await message.channel.send(
                    self._('✔ Initializing processes.'))
                await response.delete(delay = 2)

                for process in self.processes: 
                    process.start()
                    
            elif self.is_command(message.content.lower(), 'stop-all'):
                await message.delete()

                response = await message.channel.send(
                    self._('✔ Stopping processes.'))
                await response.delete(delay = 2)

                for process in self.processes: 
                    process.stop()
                                
            elif self.is_command(message.content.lower(), 'kill-all'):
                await message.delete()

                response = await message.channel.send(
                    self._('✔ Forcibly stopped processes.'))
                await response.delete(delay = 2)

                for process in self.processes: 
                    process.kill()
                                
            elif self.is_command(message.content.lower(), 'restart-all'):
                await message.delete()

                response = await message.channel.send(
                    self._('✔ Restarting processes...'))
                await response.delete(delay = 2)

                for process in self.processes: 
                    await process.restart()
                                
            elif self.is_command(message.content.lower(), 'mdreload-all'):
                await message.delete()

                response = await message.channel.send(
                    self._('✔ Reloading mdplugins...'))
                await response.delete(delay = 2)

                for process in self.processes: 
                    process.load_plugins(reload = True)
                                
            elif self.is_command(message.content.lower(), 'start'):
                process_name = message.content.removeprefix(f'{ self.prefix}start').lower().strip()
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                            .format(self.prefix, 'start', self.prefix, 'start'))
                    await response.delete(delay = 5)

                elif process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was already open.').format(process.name))
                    await response.delete(delay = 2)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Initializing process.').format(process.name))
                    await response.delete(delay = 2)
                    process.start()

            elif self.is_command(message.content.lower(), 'stop'):
                process_name = message.content.removeprefix(f'{ self.prefix}stop').lower().strip()
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()

                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                            .format(self.prefix, 'stop', self.prefix, 'stop'))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 2)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Stopping process.').format(process.name))
                    await response.delete(delay = 2)
                    process.stop()
            
            elif self.is_command(message.content.lower(), 'kill'):
                process_name = message.content.removeprefix(f'{ self.prefix}kill').lower().strip()
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                            .format(self.prefix, 'kill', self.prefix, 'kill'))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 2)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Forcibly stopped process.').format(process.name))
                    await response.delete(delay = 2)
                    process.kill()

            elif self.is_command(message.content.lower(), 'restart'):
                process_name = message.content.removeprefix(f'{ self.prefix}restart').lower().strip()
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                            .format(self.prefix, 'restart', self.prefix, 'restart'))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 2)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Restarting process...').format(process.name))
                    await response.delete(delay = 2)
                    await process.restart()

            elif self.is_command(message.content.lower(), 'mdreload'):
                process_name = message.content.removeprefix(f'{ self.prefix}mdreload').lower().strip()
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}{} <name>` or `{}{}-all`.')\
                            .format(self.prefix, 'mdreload', self.prefix, 'mdreload'))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 2)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Reloading mdplugins...').format(process.name))
                    await response.delete(delay = 2)
                    process.load_plugins(reload = True)
            
        for process in self.processes: 
            await process.discord_listener(message)
    
    async def   upload_logic            (self, message: discord.Message):
        if message.author.bot: 
            return
        
        elif not message.attachments: 
            return
        
        elif not self.uploader.is_running: 
            return
        
        elif self.uploader.overwrite:
            response = await message.channel.send(self._('Saving files...'))
            await asyncio.sleep(2)

            i = 1
            for attachment in message.attachments:
                path_to_save = os.path.join(self.uploader.path_to_upload, attachment.filename)
                await attachment.save(path_to_save)

                response = await response.edit(
                    content = self._('`[{}/{}]` Uploaded files.').format(i, len(message.attachments)))
                i += 1
            
            response = await response.edit(content = self._('✔ Files have been uploaded.'))
            await response.delete(delay = 2)
        else:
            response = await message.channel.send(self._('Processing files...'))
            await asyncio.sleep(2)

            for attachment in message.attachments:
                path_to_save = os.path.join(self.uploader.path_to_upload, attachment.filename)
                path_to_show = mcdis_path(path_to_save)
            
                if not os.path.exists(path_to_save):
                    await attachment.save(path_to_save)
                    response = await response.edit(content = response.content + self._('\n • `{}` uploaded.').format(attachment.filename))
            
                else:
                    response = await response.edit(content = response.content + self._('\n • McDis will not overwrite the file `{}`.').format(path_to_show))
                await asyncio.sleep(2)

            response = await response.edit(content = response.content + self._('\n ✔ Files have been processed.'))
            await response.delete(delay = 2)
        await message.delete()

    async def   restart                 (self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content = self._('Checking if there are open processes...'),
            embed = None,
            view = None)
        
        await asyncio.sleep(1)
        
        await self.call_addons('on_restart', (self, interaction))

        any_process_open = lambda: any([process.is_running()  for process in self.processes])

        if any_process_open():
            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                content = self._('Closing processes...'))
            print(self._('Closing processes...'))
            await asyncio.sleep(2)

        for process in self.processes: process.stop()
        
        i = 60
        while i > 0 and any_process_open():
            await interaction.followup.edit_message(
                message_id = interaction.message.id,
                content = self._('Processes will be forcibly closed in {} seconds...').format(i))
            print(self._('Processes will be forcibly closed in {} seconds...').format(i))
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
            i -= 1
            await asyncio.sleep(1)
        
        if any_process_open():
            for process in self.processes:
                process.kill()
            
            print(self._('Processes forcibly closed.'))
        else:
            print(self._('Processes closed.'))

        print(self._('Restarting...'))

        await interaction.followup.edit_message(
            message_id = interaction.message.id,
            content = self._('Restarting...'))

        await asyncio.sleep(3)
        await interaction.followup.delete_message(interaction.message.id)

        command = sys.argv[0]
        os.execv(command, sys.argv)
    
    def         on_stop                 (self):
        for addon in self.addons:
            try: 
                try: func = getattr(addon, 'on_stop')
                except AttributeError: continue
                func(self)
            except: 
                print(self._('Error in {} of {}: {}').format('on_stop()', addon.__name__, traceback.format_exc()))

        any_process_open = lambda: any([process.is_running() for process in self.processes])
        
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
    
    ###         Utils               ###
    
    def         is_command              (self, message: str, command: str, console: bool = False):
        dummy = message + ' '
        return dummy.startswith(f'{self.prefix}{command} ') if not console else dummy.startswith(command) 
        
    def         is_valid_mcdis_path     (self, path: str, *, check_if_file: bool = False, check_if_dir: bool = False):
        real_path = un_mcdis_path(path)
        new_path = os.path.join(self.cwd, real_path)
        # Note: If `real_path` is an absolute path, `os.path.join(self.cwd, real_path)` will ignore `self.cwd` 
        # and use only `real_path`. This behavior ensures that absolute paths override the base path provided.
        # To prevent escaping from `self.cwd`, a check is performed to ensure `new_path` starts with `self.cwd`.

        
        if not path.split(os.sep)[0] == 'McDis':
            return self._('✖ The path must be a McDis path. E.g.: `McDis/Backups`.')
        if not new_path.startswith(self.cwd):
            return self._('✖ You must work within the directory where McDis is running.')
        elif not os.path.exists(real_path):
            return self._('✖ The path must exist.')
        elif check_if_dir and not os.path.isdir(real_path):
            return self._('✖ The path must be a directory.')
        elif check_if_file and not os.path.isfile(real_path):
            return self._('✖ The path must be a file.')
        
        return True

    async def   call_addons             (self, function: str, args: tuple = tuple()):
        for name, addon in self.addons.items():
            try:
                func = getattr(addon, function, None)
                if func:
                    await func(*args)
                        
            except Exception:
                await self.error_report(
                    title=f'{function}() of {addon}',
                    error=traceback.format_exc()
                )

    async def   error_report            (self, *, title: str, error: str, should_print: bool = True):
        error_log = f'- Error Report [{title}]:\n\n{error}'.replace('`','’')
        mrkd_error = f'```diff\n{truncate(error_log, 1980)}\n```'
        error_reports = await thread('Error Reports', self.panel)
        error_report = await error_reports.send(mrkd_error)
        if should_print: print(f'\n{error_log}')
        
        return error_report.jump_url

    def         error_wrapper           (self, *, error_title: str = '', reports: dict = None):
        def decorator(function: Callable):
            def wrapped(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except:
                    asyncio.run_coroutine_threadsafe(
                        self.error_report(
                            title = error_title,
                            error = traceback.format_exc()
                        ),
                        self.loop
                    )

                    if reports:
                        reports['error'] = True
            return wrapped
        return decorator

    def         unload_addons           (self):
        for name, addon in self.addons.items():
            if hasattr(addon, 'unload') and callable(addon.unload):
                addon.unload()

        self.addons = {}