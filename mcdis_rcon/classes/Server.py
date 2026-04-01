from ..modules import *
from ..utils import *

from .Process import Process
from .McDisClient import McDisClient

class Server(Process):
    def __init__(self, name: str, client: McDisClient, config: dict):
        super().__init__(name, client, config)
        
    def send_response(self, target: str, message: str | list[str], *, colour: str = "gray"):
        if isinstance(message, str):
            self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')

        elif isinstance(message, list) and all(isinstance(i, str) for i in message):
            for msg in message:
                self.execute(f'tellraw {target} {{"text": "{msg}","color":"{colour}"}}')