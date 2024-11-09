from ..pm_functions import *
from ..modules import *

from ..loader import _, config, panel
from .process import Process

class Server(Process):
    def __init__(self, name: str, client: commands.Bot, process_config: dict):
        super().__init__(name, client, process_config)
        self.bots                   = []
        self.online_players         = []
        self.default_events         = True
        self.path_server            = self.path_files
        self.mcdreforged            = self.process_config['mcdreforged']
        
        if self.mcdreforged:
            try:
                with open(os.path.join(self.path_files,'config.yml'), "r+") as file:
                    yaml = ruamel.yaml.YAML()
                    yaml.indent(mapping = 2, sequence = 4, offset = 2)
                    yaml.preserve_quotes = True

                    mcdr_config = yaml.load(file)
                
                    mcdr_config['start_command'] = self.start_command
                    mcdr_config['advanced_console'] = False

                    file.seek(0)
                    yaml.dump(mcdr_config, file)
                    file.truncate()

                self.path_server            = os.path.join(self.path_files, mcdr_config['working_directory'])
                self.start_command          = 'mcdreforged'
            except:
                print(_('It was not possible to open the file \'{}\'.').format(os.path.join(self.path_files,'config.yml')))
                os._exit(0)

    def         on_stop(self):
        self.default_events = True
        self.online_players = []
        self.bots = []

    def         send_response       (self, target : str, message : Union[str, list[str]], *, colour : str = 'gray'):
        if isinstance(message, str):
            message = message.replace("\n","")
            self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')
        elif isinstance(message, list) and all(isinstance(i, str) for i in message):
            for msg in message:
                msg = msg.replace("\n","")
                self.execute(f'tellraw {target} {{"text": "{msg}","color":"{colour}"}}')
        else:
            try: message = str(message)
            except: return
            else:
                message = message.replace("\n","")
                self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')
    
    def         is_command          (self, message: str, command: str):
        dummy = message + ' '
        return dummy.startswith(f'{self.prefix}{command} ')


    def         show_command        (self, target : str, command : str, description : str):
        signs = [self.prefix, '<', '>', ':', '|']
        command = f'!!{command}'
        
        for sign in signs:
            command = command.replace(sign, f'§6{sign}§f')
        
        description = '  ↳ ' + description

        self.send_response(target, [command, description])

    def         find_real_process   (self):
        for process in psutil.process_iter():
            try:
                javas = ['java', 'java.exe']
                cond_1 = process.name() in javas
                cond_2 = os.path.abspath(self.path_files) in process.cwd()
                cond_3 = any([java in process.cmdline()[0] for java in javas])
                
                if cond_1 and cond_2 and cond_3:
                    self.real_process = process
                    break
            except: pass
    
    async def   listener_events     (self, log: str):
        try:
            if not self.default_events: 
                pass

            elif '[Server thread/INFO]' in log:
                if any([f'<{player}>' in log for player in self.online_players]):
                    player = log[log.index('<') + 1:log.index('>')]
                    message = log[log.index('>') + 1:].strip()

                    await self.call_plugins('on_player_message', (self, player, message))
                    
                    if not message.startswith(f'{self.prefix}'): return
                    
                    await self.call_plugins('on_player_command', (self, player, message))

                elif 'logged in with entity id' in log:
                    player_and_ip = log.split(' ')[log.split(' ').index('logged') - 1].strip()
                    player = player_and_ip.split('[')[0]
                    
                    self.online_players.append(player)

                    await self.call_plugins('on_player_join', (self, player))

                elif log.endswith('left the game'):
                    player = log.split(' ')[log.split(' ').index('left') - 1 ] 
                    if player in self.bots: self.bots.remove(player)
                    elif player in self.online_players: self.online_players.remove(player)

                    await self.call_plugins('on_player_left', (self, player))

                elif 'Starting minecraft server' in log:
                    await self.call_plugins('on_started', (self,))

                elif log.endswith('For help, type "help"'):
                    self.already_started = True
                    await self.call_plugins('on_already_started', (self,))
                    
                elif log.endswith('Stopping the server'):
                    await self.call_plugins('on_stopped', (self,))
                
                elif log.endswith('ThreadedAnvilChunkStorage: All dimensions are saved'):
                    await self.call_plugins('on_already_stopped', (self,))
 
            elif '[Server Watchdog/ERROR]: ' in log:
                if  log.endswith('Considering it to be crashed, server will forcibly shutdown.'): 
                    if config['Booleans']['omit crash report relay']:
                        self.stop_relaying(self.log_format('Crash detected. Finalizing relay...'))
                    
                    await self.call_plugins('on_crash', (self,))

            await self.call_plugins('listener_events', (self, log))

        except: await self.error_report(_('Error in the function listener_events().\n\n{}').format(traceback.format_exc()))