from ..modules import *
from ..utils import *

from .Process import Process
from .McDisClient import McDisClient

class Server(Process):
    def __init__(self, name: str, client: McDisClient, config: dict):
        super().__init__(name, client, config)

    def         send_response       (self, target : str, message : Union[str, list[str]], *, colour : str = 'gray'):
        if isinstance(message, str):
            self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')
        
        elif isinstance(message, list) and all(isinstance(i, str) for i in message):
            for msg in message:
                self.execute(f'tellraw {target} {{"text": "{msg}","color":"{colour}"}}')
    
    def         is_command          (self, message: str, command: str):
        dummy = message + ' '
        return dummy.startswith(f'{self.prefix}{command} ')

    def         show_command        (self, target : str, command : str, description : str):
        signs = [self.prefix, '<', '>', ':', '|']
        mrkd_command = f'{self.prefix}{command}'
        
        for sign in signs: 
            mrkd_command = mrkd_command.replace(sign, f'§6{sign}§f')
        
        description = '  ↳ ' + description

        self.execute(f'tellraw {target} {hover_and_suggest(mrkd_command, suggest = f"{self.prefix}{command}", hover = mrkd_command)}')
        self.send_response(target, description)