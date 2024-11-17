from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class FlaskManager (Flask):
    def __init__(self, client: McDisClient):
        super().__init__(__name__)
        self.active_downloads   = {}
        self.is_running         = False
        self.client             = client
        self.ip                 = client.config['Flask']['IP']
        self.port               = client.config['Flask']['Port']
        
        self.add_url_rule('/favicon.ico' , view_func = self.__favicon)
        self.add_url_rule('/file_request', view_func = self.__download_file, methods = ['GET'])

        self.start()

    def         __favicon                 (self):
        return send_from_directory(
            os.path.join(package_path, 'extras'),
            'mcdis.ico',
            mimetype = 'image/vnd.microsoft.icon'
        )

    def         __download_file           (self):
        id = request.args.get('id')
        if id in self.active_downloads.keys():
            filepath = self.active_downloads[id]['file']
            user = self.active_downloads[id]['user']
            filepath = os.path.join(self.client.cwd, filepath)
            self.active_downloads.pop(id)

            print(f'Link requested by: {user} -> Used')

            return send_file(filepath, as_attachment = True)
        return abort(404)
        
    def         __run_app                 (self):
        make_server(self.ip, self.port, self).serve_forever()

    ###         Manager Logic       ###

    async def   start                   (self):
        if self.is_running: return
        
        threading.Thread(target = self.__run_app).start()
        
        await asyncio.sleep(1)

        try:
            requests.get(f"http://{self.ip}:{self.port}")  
        except Exception as error:
            self.client.error_report(
                title = 'Flask',
                error = self.client._('Error while loading app flask: {}').format(error))
        else:
            self.is_running = True

    async def   stop                    (self):
        self.server.shutdown()
        self.is_running = False
        self.active_downloads = {}

    ###         Download Logic      ###
    
    async def   __remove_link           (self, id: str):
        await asyncio.sleep(60)

        if id in self.active_downloads.keys():
            self.active_downloads.pop(id)
    
    def         __generate_id           (self, filepath : str):
        encoded_filepath = filepath.encode()
        id = hashlib.sha256(encoded_filepath).hexdigest()
        id += f'.{random.randint(20000, 30000)}'

        return id

    def         download_link           (self, filepath: str, user : str):
        id = self.__generate_id(filepath)

        while id in self.active_downloads.keys(): 
            id = self.__generate_id(filepath)

        self.active_downloads[id] = {'user' : user, 'file': filepath}
        asyncio.create_task(self.__remove_link(id))

        return f'http://{self.client.config["Flask"]["IP"]}:{self.client.config["Flask"]["Port"]}/file_request?id={id}'
   