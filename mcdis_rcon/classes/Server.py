from .McDisClient import McDisClient
from .Process import Process, ProcessConfig


class Server(Process):
    def __init__(self, name: str, client: McDisClient, config: ProcessConfig) -> None:
        super().__init__(name, client, config)

    def send_response(self, target: str, message: str | list[str], *, colour: str = 'gray') -> None:
        if isinstance(message, str):
            self.execute(f'tellraw {target} {{"text": "{message}","color":"{colour}"}}')

        else:
            for msg in message:
                self.execute(f'tellraw {target} {{"text": "{msg}","color":"{colour}"}}')
