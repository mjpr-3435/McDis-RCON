from ..pm_functions import *
from ..modules import *

from ..loader import _, config, panel
from ..app_flask import app

class FlaskServerManager:
    def __init__(self):
        self.active_downloads = {}
        self.running = False
        self.thread = None
        self.server = None
        self.ip = config['Flask']['IP']
        self.port = config['Flask']['Port']

    def run_app(self):
        self.server = make_server(self.ip, self.port, app)
        self.server.serve_forever()

    def generate_id(self, filepath : str):
        encoded_filepath = filepath.encode()
        id = hashlib.sha256(encoded_filepath).hexdigest()
        id += f'.{random.randint(20000, 30000)}'

        return id

    def download_link(self, filepath: str, user : str):
        id = self.generate_id(filepath)

        while id in self.active_downloads.keys(): 
            id = self.generate_id(filepath)

        self.active_downloads[id] = {'user' : user, 'file': filepath}
        asyncio.create_task(self.remove_link(id))

        return f'http://{config["Flask"]["IP"]}:{config["Flask"]["Port"]}/file_request?id={id}'
    
    async def start(self):
        if not self.running:
            self.thread = threading.Thread(target=self.run_app)
            self.thread.start()
            
            await asyncio.sleep(1)

            try:
                requests.get(f"http://{self.ip}:{self.port}")  
            except Exception as e:
                print(_("Error while loading app flask: {}").format(e))
                
                return 0

            self.running = True
            return 1
        
        return 0

    async def stop(self):
        self.server.shutdown()
        self.running = False
        self.active_downloads = {}

    async def remove_link(self, id: str):
        await asyncio.sleep(60)
        if id in self.active_downloads.keys():
            self.active_downloads.pop(id)
