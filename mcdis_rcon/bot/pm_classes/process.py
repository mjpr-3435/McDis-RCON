from ..pm_functions import *
from ..modules import *

from ..loader import _, config, panel

class Process():
    def __init__(self, name: str, client: commands.Bot, process_config: dict):
        from ..pm_loader import processes, servers, networks
        self.name                   = name
        self.client                 = client
        self.prefix                 = mcdis_prefix
        self.path_files             = name
        self.path_bkps              = os.path.join('Backups',self.name)
        self.path_plugins           = os.path.join(self.path_files,'md_plugins')
        self.path_plugins_config    = os.path.join(self.path_plugins,'configs')
        self.path_commands          = os.path.join(self.path_files,'md_commands')
        self.plugins                = []
        self.process                = None
        self.real_process           = None
        self.relaying               = False
        self.already_started        = False
        self.console_log            = None
        self.console_relay          = None
        self.process_config         = process_config
        self.mcdis_config           = config
        self.stop_relay             = False
        self.stop_relay_reason      = ''
        self.processes              = processes
        self.servers                = servers
        self.networks               = networks
        self.relay_blacklist        = process_config['relay_blacklist']
        self.stop_command           = process_config['stop_command']
        self.start_command          = process_config['start_command']
        
        dirs = [self.path_files, self.path_bkps, self.path_plugins, self.path_commands, self.path_plugins_config]
        for dir in dirs: os.makedirs(dir, exist_ok=True)
    
    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def find_real_process(self):
        pass

    @abstractmethod
    async def listener_events(self, log):
        await self.call_plugins('listener_events', (self, log))

    def         state               (self, poll_based: bool = False) -> str:
        if self.process != None:
            if self.process.poll() is None or not poll_based:
                if self.already_started:
                    return 'Open'
                else:
                    return 'Initializing'
            return 'Closed'
        return 'Closed'
           
    def         start               (self):
        if self.state() in ['Open','Initializing']: return

        try:
            dirs = [self.path_files, self.path_plugins, self.path_plugins_config, self.path_commands]
            for dir in dirs: os.makedirs(dir, exist_ok = True)

            self.console_log            = queue.Queue()
            self.console_relay          = queue.Queue()

            self.process = subprocess.Popen(    self.start_command.split(' '), 
                                                cwd = self.path_files, 
                                                stdout = subprocess.PIPE, 
                                                stderr = subprocess.PIPE, 
                                                stdin = subprocess.PIPE,
                                                start_new_session = True)
            self.load_plugins()
            self.on_start()
            asyncio.create_task(self.listener_console())
        except:
            asyncio.create_task(self.error_report(_('Error in the function start().\n\n{}').format(traceback.format_exc())))
            self.stop()

    def         stop                (self, *, omit_tasks = False):
        if self.state() == 'Closed': return

        async def finalize():
            while self.state(poll_based = True) in ['Open','Initializing'] or self.relaying: 
                await asyncio.sleep(0.1)

            self.already_started = False
            self.stop_relay = False
            self.stop_relay_reason = ''
            self.process = None
            self.real_process = None
            self.console_log = None
            self.console_relay = None
            self.unload_plugins()
            
            self.on_stop()
        
        self.execute(self.stop_command)

        if not omit_tasks: asyncio.create_task(finalize())
        
    def         kill                (self):
        if isinstance(self.process, subprocess.Popen): 
            try: self.process.kill()
            except: pass

        self.find_real_process()
        try: self.real_process.kill()
        except: pass
    
    def         log_format          (self, log: str, type: str = 'INFO'):
        return f'[McDis] [{datetime.now().strftime("%H:%M:%S")}] [MainThread/{type}]: {log}'
    
    def         add_log             (self, log: str):
        self.console_relay.put(self.log_format(log))

    def         ram_usage           (self) -> str:
        if self.state() == 'Closed': 
            pass
        elif not isinstance(self.real_process, psutil.Process):
            self.find_real_process()
        elif not self.real_process.is_running():
            self.find_real_process()
            
        return ram_usage(self.real_process)

    def         disk_usage          (self, string = True) -> float:
        return get_path_size(self.path_files, string = string)

    def         make_bkp            (self, *, counter : list = None, force = False):
        if self.state() != 'Closed' and not force: return

        os.makedirs(self.path_bkps, exist_ok=True)

        bkp_path = os.path.join(self.path_bkps, f'{self.name} 1.zip')
        pattern = os.path.join(self.path_bkps, f'{self.name} [1-{config["Backups"]}].zip')
        bkps = glob.glob(pattern)
        sorted_bkps = sorted(bkps, key=os.path.getmtime, reverse = True)

        for i in range(config['Backups'] - 1,len(sorted_bkps)): os.remove(sorted_bkps.pop(i))

        sorted_bkps.reverse()
    
        for bkp in sorted_bkps:
            new_index = (len(sorted_bkps) + 1) - sorted_bkps.index(bkp)
            os.rename(bkp,os.path.join(self.path_bkps,f"{self.name} {new_index}.zip"))

        if counter:
            make_zip(self.path_files, bkp_path, counter)
        else:
            make_zip(self.path_files, bkp_path)

    def         unpack_bkp          (self, backup, *, counter : list = None): 
        try:
            shutil.rmtree(self.path_files)
        except Exception as error:
            if counter: counter[1] = error
        else:
            os.makedirs(self.path_files, exist_ok = True)
            source = os.path.join(self.path_bkps, backup)

            if counter:
                unpack_zip(source, self.path_files, counter = counter)
            else:
                unpack_zip(source, self.path_files)

    def         execute             (self, command: str):
        try:
            self.process.stdin.write((command + '\n').encode())
            self.process.stdin.flush()
        except:
            pass
    
    def         stop_relaying       (self, reason: str):
        self.stop_relay_reason = reason
        self.stop_relay = True
    
    def         load_plugins        (self,*, reload = False):
        if self.state() == 'Cerrado': return
        
        path_temp = os.path.join(self.path_plugins, 'tmp')

        if reload:
            self.unload_plugins()
            logs = ['Reloading McDis Plugin System...',
                    'McDis Plugin System is starting up',]
        else:
            logs = ['McDis Plugin System is starting up']

        valid_extensions = ['.py', '.mcdis']
        modules = [filename for filename in os.listdir(self.path_plugins) if os.path.splitext(filename)[1] in valid_extensions]

        if modules:
            logs.append('Importing mdplugins...')
            for module in modules:
                try:
                    if module.endswith('.py'):
                        spec = importlib.util.spec_from_file_location(module[:-3], os.path.join(self.path_plugins, module))
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        
                    elif module.endswith('.mcdis'):
                        zip_path = os.path.join(self.path_plugins, module)
                        temp_dir = os.path.join(path_temp, module[:-6])
                        os.makedirs(temp_dir, exist_ok = True) 
                        sys.path.insert(0, path_temp)

                        with zipfile.ZipFile(zip_path, 'r') as zip_file:
                            zip_file.extractall(temp_dir)

                        package_spec = importlib.util.spec_from_file_location(module[:-6], os.path.join(temp_dir, '__init__.py'))
                        mod = importlib.util.module_from_spec(package_spec)
                        package_spec.loader.exec_module(mod)
                        sys.path.pop(0)
                        

                    self.plugins.append(mod)
                    logs.append(f'Plugin imported:: {module}')
                except:
                    asyncio.create_task(self.error_report(_('Error while trying to load the plugin {}.\n\n{}').format(module,traceback.format_exc())))
                    logs.append(f'Unable to import plugin {module}')
        else:
            logs.append('No plugins to import')

        if not reload: logs.append('Initializing process...')
        asyncio.create_task(self.call_plugins('load', (self,)))

        for log in logs: self.add_log(log)

        if os.path.exists(path_temp): shutil.rmtree(path_temp)

    def         unload_plugins      (self):
        for module in self.plugins:
            if module in sys.modules.values():
                sys.modules.pop(module.__name__, None)
                
        self.plugins = []

    async def   call_plugins        (self, function: str, args: tuple):
       for plugin in self.plugins:
            try: 
                try: func = getattr(plugin, function)
                except AttributeError: continue

                await func(*args)
            except: await self.error_report(_('Error in {}() of {}.\n\n{}').format(function, plugin, traceback.format_exc()))

    async def   restart             (self):
        if self.state() == 'Closed': return
        
        self.stop()
            
        while self.state() != 'Closed':
            await asyncio.sleep(0.1)

        self.start()

    async def   error_report        (self, error : str):
        mrkd_error = f'```diff\n- Error Report:\n{error[:1950]}\n```'
        error_reports = await thread('Error Reports', panel)
        remote_console = await thread(f'Console {self.name}', panel)

        error_report = await remote_console.send(mrkd_error)
        await  error_reports.send(f'**Error report: ** {error_report.jump_url}')

        print(mrkd_error[7:-3])
       
    async def   discord_listener     (self, message: discord.Message):
        await self.call_plugins('on_discord_message', (self, message))
         
        if not isinstance(message.channel, discord.Thread): return
        elif not message.channel.parent_id == panel.id: return
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

    async def   listener_console    (self):
        def read_console(self: Process):
            while self.process.poll() is None:
                try:
                    log = self.process.stdout.readline().decode().strip()
                    self.console_log.put(log)
                except:
                    pass
        
        async def relay_console(self: Process):
            self.relaying = True
            remote_console = await thread(f'Console {self.name}', panel)
            await remote_console.send('```\n[Initializing Process...]\n```')

            while self.process.poll() is None or (not self.console_relay.empty()) and not self.stop_relay:
                try:
                    logs = '\n'.join([self.console_relay.get() for _ in range(10) if not self.console_relay.empty()])

                    if logs.replace('\n','').strip() != '':
                        logs = logs.replace('_','⎽').replace('*',' ').replace('`','\'')
                        await remote_console.send(f'```md\n{logs[:1990]}```')

                    if self.console_relay.qsize() < 10: await asyncio.sleep(0.5)
                    elif self.console_relay.qsize() > max_queue: 
                        self.console_relay = queue.Queue()
                        log = self.log_format(f'McDis was {max_queue} logs behind; omitting relaying these logs...')
                        await remote_console.send(f'```md\n{log}\n```')
                    else: await asyncio.sleep(0.1)
                except:
                    await self.error_report(_('Error in the function relay_console().\n\n{}').format(traceback.format_exc()))
            
            if self.stop_relay_reason: 
                await remote_console.send(f'```md\n{self.stop_relay_reason[:1990]}\n```')
            await remote_console.send('```\n[Process Stopped]\n```')
            self.relaying = False

        asyncio.create_task(relay_console(self))
        threading.Thread(target = read_console, args = (self,)).start()
            
        try: 
            while self.process.poll() is None or not self.console_log.empty():
                if self.console_log.empty(): 
                    await asyncio.sleep(0.1)
                    continue

                log = self.console_log.get()
                for i in range(100):
                    log : str = log.replace(f'[{i}m','')

                if log.replace('\n','').strip() == '': continue
                if not any([x in log for x in self.relay_blacklist if x]): self.console_relay.put(log)
                
                asyncio.create_task(self.listener_events(log))
        except:
            await self.error_report(_('Closing Process.\nError in the function listener_console().\n\n{}').format(traceback.format_exc()))
        
        self.stop()