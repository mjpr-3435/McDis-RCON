from ..modules import *
from ..utils import *

from .Process import Process
from .McDisClient import McDisClient

class Network(Process):
    def __init__(self, name: str, client: McDisClient, config: dict):
        super().__init__(name, client, config)
