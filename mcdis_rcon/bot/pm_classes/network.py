from ..pm_functions import *
from ..modules import *

from ..loader import _, config, panel
from .process import Process

class Network(Process):
    def __init__(self, name: str, client: commands.Bot, process_config: dict):
        super().__init__(name, client, process_config)

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
    
    def         on_start            (self):
        self.already_started = True
