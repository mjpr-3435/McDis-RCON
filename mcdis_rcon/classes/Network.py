from .McDisClient import McDisClient
from .Process import Process, ProcessConfig


class Network(Process):
    def __init__(self, name: str, client: McDisClient, config: ProcessConfig) -> None:
        super().__init__(name, client, config)
