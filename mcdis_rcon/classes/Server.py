from ..modules import *
from ..utils import *

from .Process import Process
from .McDisClient import McDisClient

class Server(Process):
    def __init__(self, name: str, client: McDisClient, config: dict):
        super().__init__(name, client, config)

    def         send_response       (self, target : str, message : Union[str, list[str]], *, colour : str = 'gray'):
        if isinstance(message, str):
            message = message.replace("\n","").replace('"',"'")
            self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')
        
        elif isinstance(message, list) and all(isinstance(i, str) for i in message):
            for msg in message:
                msg = msg.replace("\n","").replace('"',"'")
                self.execute(f'tellraw {target} {{"text": "{msg}","color":"{colour}"}}')
    
    def         is_command          (self, message: str, command: str):
        dummy = message + ' '
        return dummy.startswith(f'{self.prefix}{command} ')

    def         show_command        (self, target : str, command : str, description : str):
        signs = [self.prefix, '<', '>', ':', '|']
        command = f'{self.prefix}{command}'
        
        for sign in signs: 
            command = command.replace(sign, f'§6{sign}§f')
        
        description = '  ↳ ' + description

        self.send_response(target, [command, description])

    def         _find_real_process  (self):
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