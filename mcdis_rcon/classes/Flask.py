from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class FlaskManager (Flask):
    def __init__(self, client: McDisClient):
        super().__init__(__name__)
        self.active_downloads   = {}
        self.running            = False
        self.thread             = None
        self.server             = None
        self.client             = client
        self.ip                 = client.config['Flask']['IP']
        self.port               = client.config['Flask']['Port']
        
        self.add_url_rule('/favicon.ico' , view_func = self.favicon)
        self.add_url_rule('/file_request', view_func = self.download_file, methods = ['GET'])

    def favicon(self):
        return send_from_directory(
            os.path.join(package_path, 'extras'),
            'mcdis.ico',
            mimetype = 'image/vnd.microsoft.icon'
        )

    def download_file(self):
        id = request.args.get('id')
        if id in self.active_downloads.keys():
            filepath = self.active_downloads[id]['file']
            user = self.active_downloads[id]['user']
            filepath = os.path.join(cwd, filepath)
            self.active_downloads.pop(id)

            print(f'Link requested by: {user} -> Used')

            return send_file(filepath, as_attachment=True)
        return abort(404)
        
    def run_app(self):
        self.server = make_server(self.ip, self.port, self)
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

        return f'http://{self.client.config["Flask"]["IP"]}:{self.client.config["Flask"]["Port"]}/file_request?id={id}'
    
    async def start(self):
        if not self.running:
            self.thread = threading.Thread(target=self.run_app)
            self.thread.start()
            
            await asyncio.sleep(1)

            try:
                requests.get(f"http://{self.ip}:{self.port}")  
            except Exception as e:
                print(self.client._("Error while loading app flask: {}").format(e))
                
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