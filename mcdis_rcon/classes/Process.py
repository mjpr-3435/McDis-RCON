from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class Process():
    def __init__(self, name: str, client: McDisClient, config: dict):
        self.name                   = name
        self.path_files             = name
        self.client                 = client
        self.path_bkps              = os.path.join(client.path_backups  , self.name)
        self.path_plugins           = os.path.join(self.path_files      ,'mdplugins' )
        self.path_plugins_config    = os.path.join(self.path_plugins    ,'configs'   )
        self.path_commands          = os.path.join(self.path_files      ,'mdcommands')
        self.relay_blacklist        = config['relay_blacklist']
        self.stop_command           = config['stop_command']
        self.start_command          = config['start_command']
        self.plugins                = []
        self.process                = None
        self.real_process           = None
        self.__relaying             = False
        self.__stop_relay           = False
        self.__stop_relay_reason    = None
        self.__console_log          = None
        self.__console_relay        = None
        
        dirs = [self.path_files, self.path_bkps, self.path_plugins, self.path_commands, self.path_plugins_config]
        for dir in dirs: os.makedirs(dir, exist_ok = True)
    
    @abstractmethod
    def _find_real_process(self):
        pass

    ###         Manager Logic       ###

    def         is_running               (self, poll_based: bool = False) -> str:
        if self.process != None:
            if self.process.poll() is None or not poll_based:
                return True
            return False
        return False
           
    def         start                   (self):
        if self.is_running() : return

        try:
            dirs = [self.path_files, self.path_plugins, self.path_plugins_config, self.path_commands]
            for dir in dirs: os.makedirs(dir, exist_ok = True)

            self.__console_log            = queue.Queue()
            self.__console_relay          = queue.Queue()

            self.process = subprocess.Popen(    self.start_command.split(' '), 
                                                cwd = self.path_files, 
                                                stdout = subprocess.PIPE, 
                                                stderr = subprocess.PIPE, 
                                                stdin = subprocess.PIPE,
                                                start_new_session = True)
            self.load_plugins()
            asyncio.create_task(self.__listener_console())
        except:
            asyncio.create_task(
                self.error_report(
                    title = 'start()',
                    error = traceback.format_exc()        
                )
            )
            self.stop()

    def         stop                    (self, *, omit_tasks = False):
        if not self.is_running(): return

        async def finalize():
            while self.is_running(poll_based = True) or self.__relaying: 
                await asyncio.sleep(0.1)

            self.process                = None
            self.real_process           = None
            self.__stop_relay           = False
            self.__stop_relay_reason    = None
            self.__console_log          = None
            self.__console_relay        = None
            self.unload_plugins()
        
        self.execute(self.stop_command)

        if not omit_tasks: asyncio.create_task(finalize())
        
    def         kill                    (self):
        if isinstance(self.process, subprocess.Popen): 
            try: self.process.kill()
            except: pass

        self._find_real_process()
        try: self.real_process.kill()
        except: pass
    
    def         load_plugins            (self, *, reload = False):
        if self.is_running() == 'Closed': return
        
        temp_path = os.path.join(self.path_plugins, 'tmp')
        os.makedirs(temp_path, exist_ok = True)

        if reload:
            self.unload_plugins()
            logs = ['Reloading McDis Plugin System...',
                    'McDis Plugin System is starting up',]
        else:
            logs = ['McDis Plugin System is starting up']

        valid_extensions = ['.py', '.mcdis']
        modules = [file for file in os.listdir(self.path_plugins) if os.path.splitext(file)[1] in valid_extensions]

        if modules:
            logs.append('Importing mdplugins...')
            sys.path.insert(0, temp_path)

            for module in modules:
                try:
                    if module.endswith('.py'):
                        module_path = os.path.join(self.path_plugins, module)
                        spec = importlib.util.spec_from_file_location(module[:-3], module_path)
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        
                    elif module.endswith('.mcdis'):
                        zip_path = os.path.join(self.path_plugins, module)
                        mod_temp_dir = os.path.join(temp_path, module[:-6])
                        os.makedirs(mod_temp_dir, exist_ok = True) 

                        with zipfile.ZipFile(zip_path, 'r') as zip_file:
                            zip_file.extractall(mod_temp_dir)
                        
                        init_path = os.path.join(mod_temp_dir, '__init__.py')
                        pkg_spec = importlib.util.spec_from_file_location(module[:-6], init_path)
                        mod = importlib.util.module_from_spec(pkg_spec)
                        pkg_spec.loader.exec_module(mod)

                    self.plugins.append(mod)
                    logs.append(f'Plugin imported:: {module}')
                except:
                    asyncio.create_task(
                        self.error_report(
                            title = f'unable to import plugin {module}',
                            error = traceback.format_exc()
                        )
                    )
            
            sys.path.pop(0)
        else:
            logs.append('No plugins to import')
        
        if not reload: logs.append('Initializing process...')
        asyncio.create_task(self.call_plugins('load', (self,)))

        for log in logs: self.add_log(log)

        if os.path.exists(temp_path): shutil.rmtree(temp_path)

    def         unload_plugins          (self):
        for module in self.plugins:
            if module in sys.modules.values():
                sys.modules.pop(module.__name__, None)
                
        self.plugins = []

    async def   restart                 (self):
        if not self.is_running(): return
        
        self.stop()
            
        while self.is_running():
            await asyncio.sleep(0.1)

        self.start()

    ###         Resources           ###

    def         ram_usage               (self) -> str:
        if not self.is_running(): 
            pass
        elif not isinstance(self.real_process, psutil.Process):
            self._find_real_process()
        elif not self.real_process.is_running():
            self._find_real_process()
            
        return ram_usage(self.real_process)

    def         disk_usage              (self, string = True) -> float:
        return get_path_size(self.path_files, string = string)

    ###         Backups Logic       ###

    def         make_bkp                (self, *, counter : list = None, force = False):
        try:
            if self.is_running() and not force: return

            os.makedirs(self.path_bkps, exist_ok = True)

            bkp_path = os.path.join(self.path_bkps, f'{self.name} 1.zip')
            pattern = os.path.join(self.path_bkps, f'{self.name} [1-{self.client.config["Backups"]}].zip')
            bkps = glob.glob(pattern)
            sorted_bkps = sorted(bkps, key = os.path.getmtime, reverse = True)

            for i in range(self.client.config['Backups'] - 1,len(sorted_bkps)): os.remove(sorted_bkps.pop(i))

            sorted_bkps.reverse()
        
            for bkp in sorted_bkps:
                new_index = (len(sorted_bkps) + 1) - sorted_bkps.index(bkp)
                os.rename(bkp, os.path.join(self.path_bkps, f"{self.name} {new_index}.zip"))

            if counter:
                make_zip(self.path_files, bkp_path, counter)
            else:
                make_zip(self.path_files, bkp_path)
        except:
            asyncio.create_task(
                self.error_report(
                    title = 'make_bkp()',
                    error = traceback.format_exc()
                )
            )
    
    def         unpack_bkp              (self, backup, *, counter : list = None): 
        try:
            shutil.rmtree(self.path_files)

            os.makedirs(self.path_files, exist_ok = True)
            source = os.path.join(self.path_bkps, backup)

            if counter:
                unpack_zip(source, self.path_files, counter = counter)
            else:
                unpack_zip(source, self.path_files)
        except:
            asyncio.create_task(
                self.error_report(
                    title = 'unpack_bkp()',
                    error = traceback.format_exc()
                )
            )
    ###         Behaviours          ###

    async def   discord_listener        (self, message: discord.Message):
        await self.call_plugins('on_discord_message', (self, message))
         
        if not isinstance(message.channel, discord.Thread): return
        elif not message.channel.parent_id == self.client.panel.id: return
        elif not message.channel.name == f'Console {self.name}': return
        
        if message.content.lower() == 'start':
            self.start()
        
        elif message.content.lower() == 'kill':
            self.kill()

        elif message.content.lower() == 'restart':
            await self.restart()

        elif message.content.lower() == 'stop':
            self.stop()

        elif message.content.lower() == 'reload mdplugins':
            self.load_plugins(reload = True)

        else:
            self.execute(message.content)
    
    ###         Relay Logic         ###

    def         stop_relaying           (self, reason: str):
        self.__stop_relay_reason = reason
        self.__stop_relay = True
    
    def         __read_console          (self):
        while self.process.poll() is None:
            try:
                log = self.process.stdout.readline().decode().strip()
                self.__console_log.put(log)
            except:
                pass
        
    async def   __relay_console         (self):
        max_logs_in_queue   = 1000
        self.__relaying     = True
        remote_console      = await thread(f'Console {self.name}', self.client.panel)
        await remote_console.send('```\n[Initializing Process...]\n```')

        while (self.process.poll() is None or not self.__console_relay.empty()) and not self.__stop_relay:
            try:
                logs = '\n'.join([self.__console_relay.get() for _ in range(10) if not self.__console_relay.empty()])

                if logs.replace('\n','').strip() != '':
                    logs = logs.replace('_','⎽').replace('*',' ').replace('`','’').strip()
                    await remote_console.send(f'```md\n{truncate(logs, 1990)}```')

                if self.__console_relay.qsize() < 10: 
                    await asyncio.sleep(0.5)

                elif max_logs_in_queue < self.__console_relay.qsize(): 
                    self.__console_relay = queue.Queue()
                    log = self.log_format(
                        f'McDis was {max_logs_in_queue} logs behind; omitting relaying these logs...'
                        )
                        
                    await remote_console.send(f'```md\n{log}\n```')

                else: 
                    await asyncio.sleep(0.1)

            except:
                await self.error_report(
                    title = 'relay_console()',
                    error = traceback.format_exc())
        
        if self.__stop_relay_reason: 
            await remote_console.send(
                f'```md\n{truncate(self.__stop_relay_reason, 1990)}\n```'
                )
            
        await remote_console.send('```\n[Process Stopped]\n```')

        self.__relaying = False

    async def   __listener_events       (self, log: str):
        await self.call_plugins('listener_events', (self, log))

    async def   __listener_console        (self):
        asyncio.create_task(self.__relay_console())
        threading.Thread(target = self.__read_console).start()
            
        try: 
            while self.process.poll() is None or not self.__console_log.empty():
                if self.__console_log.empty(): 
                    await asyncio.sleep(0.1)
                    continue

                log = self.__console_log.get()
                for i in range(100): log : str = log.replace(f'[{i}m','')
                if log.replace('\n','').strip() == '': continue
                if not any([x in log for x in self.relay_blacklist if x]): self.__console_relay.put(log)
                
                asyncio.create_task(self.__listener_events(log))
        except:
            await self.error_report(
                title = 'listener_console()',
                error = traceback.format_exc()
            )
            return
        
        self.stop()

###         Utils               ###
    
    def         execute                 (self, command: str):
        try:
            self.process.stdin.write((command + '\n').encode())
            self.process.stdin.flush()
        except:
            pass

    def         log_format              (self, log: str, type: str = 'INFO'):
        return f'[McDis] [{datetime.now().strftime("%H:%M:%S")}] [MainThread/{type}]: {log}'
    
    def         add_log                 (self, log: str):
        self.__console_relay.put(self.log_format(log))

    async def   call_plugins            (self, function: str, args: tuple):
       for plugin in self.plugins:
            try: 
                try: func = getattr(plugin, function)
                except AttributeError: continue

                await func(*args)
            except: 
                await self.error_report(
                    title = '{function}() of {plugin}',
                    error = traceback.format_exc()
                    )

    async def   error_report            (self, *, title: str, error: str):
        formatted_title = f'{self.name}: {title}'
        
        error_link = await  self.client.error_report(
            title = formatted_title,
            error = error
        )

        formatted_error = self.log_format(f'Error report created. {formatted_title}')
        mrkd = f'{error_link}\n```md\n{formatted_error}\n```'
        remote_console = await thread(f'Console {self.name}', self.client.panel)

        await remote_console.send(mrkd)
    
    async def   send_to_console         (self, message : str):
        mrkd = f'```md\n{truncate(message, 1990)}\n```'
        remote_console = await thread(f'Console {self.name}', self.client.panel)

        await remote_console.send(mrkd)