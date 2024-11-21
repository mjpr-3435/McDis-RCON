from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class FlaskManager (Flask):
    def __init__(self, client: McDisClient):
        super().__init__(__name__)
        self.active_downloads   = {}
        self.is_running         = False
        self.ip                 = client.config['Flask']['IP']
        self.port               = client.config['Flask']['Port']
        self._client            = client
        self._server            = None
        
        self.add_url_rule('/favicon.ico' , view_func = self._favicon)
        self.add_url_rule('/file_request', view_func = self._download_file, methods = ['GET'])

    def         _favicon                 (self):
        return send_from_directory(
            os.path.join(package_path, 'extras'),
            'mcdis.ico',
            mimetype = 'image/vnd.microsoft.icon'
        )

    def         _download_file           (self):
        id = request.args.get('id')
        if id in self.active_downloads.keys():
            filepath = self.active_downloads[id]['file']
            user = self.active_downloads[id]['user']
            filepath = os.path.join(self._client.cwd, filepath)
            self.active_downloads.pop(id)

            print(f'Link requested by: {user} -> Used')

            return send_file(filepath, as_attachment = True)
        return abort(404)
        
    def         _run_app                 (self):
        self._server = make_server(self.ip, self.port, self)
        self._server.serve_forever()

    ###         Manager Logic       ###

    async def   start                   (self):
        if self.is_running: return
        
        threading.Thread(target = self._run_app).start()
        
        await asyncio.sleep(1)

        try:
            requests.get(f"http://{self.ip}:{self.port}")  
        except Exception as error:
            await self._client.error_report(
                title = 'Flask: start()',
                error = error)
        else:
            self.is_running = True

    async def   stop                    (self):
        self._server.shutdown()
        self.is_running = False
        self.active_downloads = {}

    ###         Download Logic      ###
    
    async def   _remove_link           (self, id: str):
        await asyncio.sleep(60)

        if id in self.active_downloads.keys():
            self.active_downloads.pop(id)
    
    def         _generate_id           (self, filepath : str):
        encoded_filepath = filepath.encode()
        id = hashlib.sha256(encoded_filepath).hexdigest()
        id += f'.{random.randint(20000, 30000)}'

        return id

    def         download_link           (self, filepath: str, user : str):
        id = self._generate_id(filepath)

        while id in self.active_downloads.keys(): 
            id = self._generate_id(filepath)

        self.active_downloads[id] = {'user' : user, 'file': filepath}
        asyncio.create_task(self._remove_link(id))

        return f'http://{self._client.config["Flask"]["IP"]}:{self._client.config["Flask"]["Port"]}/file_request?id={id}'
   