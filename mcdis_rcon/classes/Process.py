from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class Process():
    def __init__(self, name: str, client: McDisClient, config: dict):
        self.name                   = name
        self.path_files             = name
        self.client                 = client
        self.prefix                 = self.client.prefix
        self.path_bkps              = os.path.join(client.path_backups, self.name)
        self.path_plugins           = os.path.join(self.path_files,'.mdplugins')
        self.path_plugins_configs   = os.path.join(self.path_plugins,'configs')
        self.path_commands          = os.path.join(self.path_files,'.mdcommands')
        self.start_cmd              = config['start_cmd']
        self.stop_cmd               = config['stop_cmd']
        self.blacklist              = config['blacklist']
        self.plugins                = {}
        self.process                = None
        self.real_process           = None
        self._relaying              = False
        self._stop_relay            = False
        self._stop_relay_reason     = None
        self._console_log           = None
        self._console_relay         = None
        self._max_logs_in_queue     = 1000
        
        dirs = [self.path_files, self.path_bkps, self.path_plugins, self.path_commands, self.path_plugins_configs]
        for dir in dirs: os.makedirs(dir, exist_ok = True)

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
            dirs = [self.path_files, self.path_plugins, self.path_plugins_configs, self.path_commands]
            for dir in dirs: os.makedirs(dir, exist_ok = True)

            self._console_log            = queue.Queue()
            self._console_relay          = queue.Queue()

            self.process = subprocess.Popen(    self.start_cmd.split(' '), 
                                                cwd = self.path_files, 
                                                stdout = subprocess.PIPE, 
                                                stderr = subprocess.PIPE, 
                                                stdin = subprocess.PIPE,
                                                start_new_session = True)
            self.load_plugins()
            asyncio.create_task(self._listener_console())
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
            while self.is_running(poll_based = True) or self._relaying: 
                await asyncio.sleep(0.1)

            self.process               = None
            self.real_process          = None
            self._stop_relay           = False
            self._stop_relay_reason    = None
            self._console_log          = None
            self._console_relay        = None
            self.unload_plugins()
        
        self.execute(self.stop_cmd)

        if not omit_tasks: asyncio.create_task(finalize())
        
    def         kill                    (self):
        if isinstance(self.process, subprocess.Popen): 
            try: self.process.kill()
            except: pass

        self._find_real_process()
        try: self.real_process.kill()
        except: pass

        self.process               = None
        self.real_process          = None
        self._stop_relay           = False
        self._stop_relay_reason    = None
        self._console_log          = None
        self._console_relay        = None
        self.unload_plugins()
    
    def         load_plugins            (self, *, reload = False):
        if not self.is_running(): return
        
        if reload:
            self.unload_plugins()
            logs = ['Reloading McDis Plugin System...',
                    'McDis Plugin System is starting up',]
        else:
            logs = ['McDis Plugin System is starting up']

        valid_extensions = ['.py', '.mcdis']
        files_in_plugins_dir = os.listdir(self.path_plugins)
        cond = lambda file: os.path.splitext(file)[1] in valid_extensions

        plugins = [file for file in files_in_plugins_dir if cond(file)]

        if not plugins:
            logs.append('No plugins to import')

        else:
            logs.append('Importing mdplugins...')

            for plugin in plugins:
                try:
                    if plugin.endswith('.py'):
                        module_path = os.path.join(self.path_plugins, plugin)
                        spec = importlib.util.spec_from_file_location(plugin.removesuffix('.py'), module_path)
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        
                    elif plugin.endswith('.mcdis') and False:
                        plugin_path = os.path.join(self.path_plugins, plugin)
                        sys.path.insert(0, plugin_path)
                        
                        mod = importlib.import_module(f'mdplugin.__init__')
                        sys.path.pop(0)
                    
                    plugin_instance = mod.mdplugin(self)
                    self.plugins[os.path.splitext(plugin)[0]] = plugin_instance
                    logs.append(f'Plugin imported:: {plugin}')
                    
                except:
                    asyncio.create_task(
                        self.error_report(
                            title = f'Unable to import plugin {plugin}',
                            error = traceback.format_exc()
                        )
                    )
        
        if not reload: logs.append('Initializing process...')

        for log in logs: self.add_log(log)

    def         unload_plugins          (self):
        for name, plugin in self.plugins.items():
            if hasattr(plugin, 'unload') and callable(plugin.unload):
                plugin.unload()

        self.plugins = {}

    async def   restart                 (self):
        if not self.is_running(): return
        
        self.stop()
            
        while self.is_running():
            await asyncio.sleep(0.1)

        self.start()

    ###         Resources           ###
    
    def         _find_real_process(self):
        abs_file_path = os.path.abspath(self.path_files)
        
        for process in psutil.process_iter():
            try:
                javas = ['java', 'java.exe']
                cond_1 = process.name() in javas
                cond_2 = os.path.commonpath([abs_file_path, process.cwd()]) == abs_file_path
                cond_3 = any([java in process.cmdline()[0] for java in javas])
                cond_4 = process.memory_info().rss // (1024**2) > 50
                
                if cond_1 and cond_2 and cond_3 and cond_4:
                    self.real_process = process
                    break
            except: pass

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

    def         make_bkp                (self,          *, counter : list = None):
        if self.is_running(): return

        os.makedirs(self.path_bkps, exist_ok = True)

        bkp_path = os.path.join(self.path_bkps, f'{self.name} 1.zip')
        pattern = os.path.join(self.path_bkps, f'{self.name} [1-{self.client.config["Backups"]}].zip')
        bkps = glob.glob(pattern)
        sorted_bkps = sorted(bkps, key = os.path.getmtime, reverse = True)

        for i in range(self.client.config['Backups'] - 1,len(sorted_bkps)): os.remove(sorted_bkps.pop(i))

        sorted_bkps.reverse()
    
        for bkp in sorted_bkps:
            new_index = (len(sorted_bkps) + 1) - sorted_bkps.index(bkp)
            new_name = os.path.join(self.path_bkps, f"{self.name} {new_index}.zip")
            
            try:
                os.rename(bkp, new_name)
            except:
                self.error_report(
                    title = 'Renaming in make_bkp()',
                    error = traceback.format_exc())
                return
            
        make_zip(self.path_files, bkp_path, counter)

        log_filename = 'backup_log.txt'
        log_content = f'Backup created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'

        with zipfile.ZipFile(bkp_path, 'a') as zipf:
            zipf.writestr(log_filename, log_content)

        with zipfile.ZipFile(bkp_path, 'a') as zipf:
            if log_filename in zipf.namelist():
                temp_zip = zipfile.ZipFile(bkp_path, 'w')
                for item in zipf.infolist():
                    if item.filename != log_filename:
                        temp_zip.writestr(item.filename, zipf.read(item.filename))
                temp_zip.close()
            
            zipf.writestr(log_filename, log_content)
    
    def         unpack_bkp              (self, backup,  *, counter : list = None):
        shutil.rmtree(self.path_files)

        os.makedirs(self.path_files, exist_ok = True)
        source = os.path.join(self.path_bkps, backup)

        unpack_zip(source, self.path_files, counter)
   
    ###         Behaviours          ###

    async def   discord_listener        (self, message: discord.Message):
        await self.call_plugins('on_discord_message', (message,))
         
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

        elif message.content.lower() == 'mdreload':
            self.load_plugins(reload = True)

        else:
            self.execute(message.content)
    
    ###         Relay Logic         ###

    def         stop_relaying           (self, reason: str):
        self._stop_relay_reason = reason
        self._stop_relay = True
    
    def         _read_console          (self):
        while self.process.poll() is None:
            try:
                log = self.process.stdout.readline().decode().strip()
                self._console_log.put(log)
            except:
                pass
        
    async def   _relay_console         (self):
        self._relaying     = True
        remote_console      = await thread(f'Console {self.name}', self.client.panel)
        await remote_console.send('```\n[Initializing Process...]\n```')

        while (self.process.poll() is None or not self._console_relay.empty()) and not self._stop_relay:
            try:
                logs = '\n'.join([self._console_relay.get() for _ in range(10) if not self._console_relay.empty()])

                if logs.replace('\n','').strip() != '':
                    logs = logs.replace('_','⎽').replace('*',' ').replace('`','’').strip()
                    await remote_console.send(f'```md\n{truncate(logs, 1990)}```')

                if self._console_relay.qsize() < 10: 
                    await asyncio.sleep(0.5)

                elif self._max_logs_in_queue < self._console_relay.qsize(): 
                    self._console_relay = queue.Queue()
                    log = self.log_format(
                        f'McDis was {self._max_logs_in_queue} logs behind; omitting relaying these logs...'
                        )
                        
                    await remote_console.send(f'```md\n{log}\n```')

                else: 
                    await asyncio.sleep(0.1)

            except:
                await self.error_report(
                    title = 'relay_console()',
                    error = traceback.format_exc())
        
        if self._stop_relay_reason: 
            await remote_console.send(
                f'```md\n{truncate(self._stop_relay_reason, 1990)}\n```'
                )
            
        await remote_console.send('```\n[Process Stopped]\n```')

        self._relaying = False

    async def   _listener_events       (self, log: str):
        await self.call_plugins('listener_events', (log, ))

    async def   _listener_console        (self):
        asyncio.create_task(self._relay_console())
        threading.Thread(target = self._read_console).start()
            
        try: 
            while self.process.poll() is None or not self._console_log.empty():
                if self._console_log.empty(): 
                    await asyncio.sleep(0.1)
                    continue

                log = self._console_log.get()
                for i in range(100): log : str = log.replace(f'[{i}m','')
                if log.replace('\n','').strip() == '': continue
                if not any([x in log for x in self.blacklist if x]): self._console_relay.put(log)
                
                asyncio.create_task(self._listener_events(log))
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
        self._console_relay.put(self.log_format(log))

    async def   call_plugins            (self, function: str, args: tuple = tuple()):
       for name, plugin in self.plugins.items():
            try: 
                func = getattr(plugin, function, None)
                if func:
                    await func(*args)
            except: 
                await self.error_report(
                    title = f'{function}() of {plugin}',
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
    
    async def   send_to_console         (self, message : str) -> discord.Message:
        mrkd = f'```md\n{truncate(message, 1990)}\n```'
        remote_console = await thread(f'Console {self.name}', self.client.panel)

        discord_message = await remote_console.send(mrkd)

        return discord_message