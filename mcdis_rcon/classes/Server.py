from ..modules import *
from ..utils import *

from .Process import Process, ProcessConfig
from .McDisClient import McDisClient

class Server(Process):
    def __init__(self, name: str, client: McDisClient, config: ProcessConfig):
        super().__init__(name, client, config)