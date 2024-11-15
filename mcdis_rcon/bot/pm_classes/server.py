from ..pm_functions import *
from ..modules import *

from ..loader import _, config, panel
from .process import Process

class Server(Process):
    def __init__(self, name: str, client: commands.Bot, process_config: dict):
        super().__init__(name, client, process_config)

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