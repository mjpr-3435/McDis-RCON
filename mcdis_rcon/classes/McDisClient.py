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
        self.addons                                             = []
        self.flask      : FlaskManager                          = None
        self.processes  : list[Union[Network,Server]]           = []
        self.networks   : list[Network]                         = []
        self.servers    : list[Server]                          = []
        self.uploader                                           = Uploader()
        self.is_running                                         = False
        
        self.max_processes                                           = 5

        os.makedirs(self.path_backups, exist_ok = True)
        os.makedirs(self.path_addons , exist_ok = True)
        
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

                    elif process in [self.path_backups, self.path_addons]:
                        print(f'{process}:  A process cannot be named \'{self.path_backups}\' or \'{self.path_addons}\'.')
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

                    elif not all([isinstance(x,str) for x in process_config['blacklist']]):
                        print(f'{process}: The \'blacklist\' variable must be a list of strings.')
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
        print(self._('   • Creating processes objects\n{}').format(processes_objects))
            
        for process in self.processes:
            await thread(f'Console {process.name}', self.panel, public = True)
        await thread(f'Error Reports', self.panel, public = True)

    async def   _load_addons           (self):
        files_in_addons_dir = os.listdir(self.path_addons)
        
        def condition(file):
            path = os.path.join(self.path_addons, file)
            path_init = os.path.join(path, '__init__.py')

            return os.path.isdir(path) and os.path.exists(path_init)
        
        addons = [file for file in files_in_addons_dir if condition(file)]
        if not addons: return
        
        print(self._('   • Importing addons:'))
        sys.path.insert(0, self.path_addons)
        
        for addon in addons:
            try:
                path_init = os.path.join(self.path_addons, addon, '__init__.py')
                pkg = importlib.util.spec_from_file_location(addon, path_init)
                mod = importlib.util.module_from_spec(pkg)
                pkg.loader.exec_module(mod)
                self.addons.append(mod)
                print(self._('     -> Imported \t{}').format(os.path.basename(addon)))
            except:
                print(self._('     -> Unable to import {}\n{}').format(os.path.basename(addon), traceback.format_exc()))
                os._exit(0)
        
        sys.path.pop(0)

        await self.call_addons('load', (self,), exit_on_error = True)

    async def   _load_behaviours       (self):
        behaviours_dir = os.path.join(package_path, 'behaviours')

        scripts = [filename for filename in os.listdir(behaviours_dir)]

        for script in scripts:
            await self.load_extension(f'mcdis_rcon.behaviours.{script.removesuffix(".py")}')
    
    async def   _load_banner           (self, *, loop: bool = True, view: bool = True):
        from ..gui.Panel import PanelView, PanelEmbed
        first_iteration = True
        file = None

        if os.path.exists('banner.png'): 
            file = discord.File('banner.png')

        while loop or first_iteration:
            first_iteration = False
            
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
        self._load_panel()

        print(self._('Logged in as {}!').format(self.user))

        try:
            await self._load_processes()
            await self._load_addons()
            await self._load_behaviours()
            print(self._('   • Loaded behaviours'))
            await self.tree.sync()
            print(self._('   • Client commands synchronized to Discord'))

            if self.config['Flask']['Allow']: 
                self.flask = FlaskManager(self)
                print(self._('   • Flask object created'))
                
        except Exception as error:
            print(self._('There was an error while loading McDis-RCON.'))
            print(self._('Error: {}').format(error))
            os._exit(0)

        asyncio.create_task(self._load_banner())
        print(self._('   • Loaded server panel'))
        print(self._('Loading Complete'))

        signal_handler = lambda sig, frame: threading.Thread(target = self.on_stop).start()
        
        signal.signal(signal.SIGINT, signal_handler)
        self.is_running = True

    async def   panel_interface         (self, message: discord.Message):
        if message.author.bot: 
            return

        for process in self.processes: 
            await process.discord_listener(message)

        if message.channel.id == self.panel.id:
            if   self.is_panel_command(message.content.lower(), f'{ self.prefix}start-all'):
                await message.delete()

                for process in self.processes: 
                    process.start()
                    
            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}stop-all'):
                await message.delete()

                for process in self.processes: 
                    process.stop()
                                
            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}start'):
                process_name = message.content.removeprefix(f'{ self.prefix}start')
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}start <name>`.').format( self.prefix))
                    await response.delete(delay = 5)

                elif process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was already open.').format(process.name))
                    await response.delete(delay = 5)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Initializing process.').format(process.name))
                    await response.delete(delay = 5)
                    process.start()

            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}stop'):
                process_name = message.content.removeprefix(f'{ self.prefix}stop')
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()

                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}stop <name>`.').format( self.prefix))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 5)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Stopping process.').format(process.name))
                    await response.delete(delay = 5)
                    process.stop()
            
            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}kill'):
                process_name = message.content.removeprefix(f'{ self.prefix}kill')
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}kill <name>`.').format( self.prefix))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 5)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Forcibly stopped process.').format(process.name))
                    await response.delete(delay = 5)
                    process.kill()

            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}restart'):
                process_name = message.content.removeprefix(f'{ self.prefix}restart')
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}restart <name>`.').format( self.prefix))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 5)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Restarting process...').format(process.name))
                    await response.delete(delay = 5)
                    await process.restart()

            elif self.is_panel_command(message.content.lower(), f'{ self.prefix}reload mdplugins'):
                process_name = message.content.removeprefix(f'{ self.prefix}reload mdplugins')
                process = next(filter(lambda x: process_name == x.name.lower(), self.processes), None)

                await message.delete()
                
                if not process:
                    response = await message.channel.send(
                        self._('✖ Specify the process. E.g.: `{}reload_mdplugins <name>`.').format( self.prefix))
                    await response.delete(delay = 5)

                elif not process.is_running():
                    response = await message.channel.send(
                        self._('✖ `[{}]`: The process was not open.').format(process.name))
                    await response.delete(delay = 5)
                
                else:
                    response = await message.channel.send(
                        self._('✔ `[{}]`: Reloading mdplugins...').format(process.name))
                    await response.delete(delay = 5)
                    process.load_plugins(reload = True)
        
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
    
    def         is_panel_command        (self, message: str, command: str):
            dummy = message + ' '
            return dummy.startswith(f'{self.prefix}{command} ')
        
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

    async def   call_addons             (self, function: str, args: tuple, *, exit_on_error: bool = False):
        for addon in self.addons:
            try:
                try: func = getattr(addon, 'call_behaviours')
                except AttributeError: continue
            
                await func(function, args)
            except: 
                await self.error_report(
                    title = f'{function}() of {addon.__name__}',
                    error = traceback.format_exc()
                )

                if exit_on_error: os._exit(0)

    async def   error_report            (self, *, title: str, error: str, ):
        error_log = f'- Error Report [{title}]:\n\n{error}'.replace('`','’')
        mrkd_error = f'```diff\n{truncate(error_log, 1980)}\n```'
        error_reports = await thread('Error Reports', self.panel)
        error_report = await error_reports.send(mrkd_error)
        print(f'\n{error_log}')
        
        return error_report.jump_url