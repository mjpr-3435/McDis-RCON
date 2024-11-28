from ..modules import *
from ..utils import *

from .McDisClient import McDisClient

class FlaskManager (Flask):
    def __init__(self, client: McDisClient):
        super().__init__(__name__)
        self.active_downloads       = {}
        self.shutdown_requests      = {}
        self.is_running             = False
        self.temporary_links        = True
        self.one_time_links         = True
        self.ip                     = client.config['Flask']['IP'] if client.config['Flask']['Allow'] else '——'
        self.port                   = client.config['Flask']['Port'] if client.config['Flask']['Allow'] else '——'
        self.addres                 = f'http://{self.ip}:{self.port}'
        self.client                 = client
        self._log_queue             = None
        self._server                = None
        
        self.add_url_rule('/favicon.ico'    , view_func = self._favicon)
        self.add_url_rule('/file_request'   , view_func = self._download_file   , methods = ['GET'])
        self.add_url_rule('/shutdown'       , view_func = self._shutdown        , methods = ['GET'])
        self.handle_http_exception = self._handler

    def         _handler                (self, exception):
        if exception.code == 404:
            log = f'Unusual connection attempt to: {request.path} with args: {request.args}'
            self._log_queue.put(self.log_format(log))
        return super().handle_http_exception(exception)
    
    def         _favicon                (self):
        return send_from_directory(
            os.path.join(package_path, 'extras'),
            'mcdis.ico',
            mimetype = 'image/vnd.microsoft.icon'
        )

    def         _download_file          (self):
        id = request.args.get('id')
        if id in self.active_downloads.keys():
            file_path = self.active_downloads[id]['file']
            user = self.active_downloads[id]['user']
            file_path = os.path.join(self.client.cwd, file_path)

            log = f'Link requested by: {user} -> Used. Requested file: {file_path}'
            self._log_queue.put(self.log_format(log))

            if self.one_time_links: 
                self.active_downloads.pop(id)
                log = f'Link with id {id} was removed'
                self._log_queue.put(self.log_format(log))
            
            return send_file(file_path, as_attachment = True)
        return abort(404)

    def         _shutdown               (self):
        id = request.args.get('id')
        if id in self.shutdown_requests.keys():
            user = self.shutdown_requests[id]['user']
            
            log = f'Shutdown link requested by: {user} -> Used'
            self._log_queue.put(self.log_format(log))

            log = f'Shutdown signal received'
            self._log_queue.put(self.log_format(log))

            return redirect(f'/shutdown?id={id}')
        return abort(404)

    def         _run_app                (self):
        self.is_running = True
        self._log_queue = queue.Queue()

        self._server = make_server(self.ip, self.port, self)
        self._server.serve_forever()
        
        self.is_running = False
        self._log_queue = None
        self.active_downloads = {}

    def         _is_valid_addres        (self):
        try:
            sock = socket.create_connection((self.ip, self.port), timeout=5)
            sock.close()
        except:
            asyncio.create_task(self.client.error_report(
                title = 'Flask: Invalid Adress',
                error = traceback.format_exc()
            ))
            return False
        else:
            return True

    ###         Manager Logic       ###

    async def   start                   (self):
        if self.is_running or not self._is_valid_addres(): return

        threading.Thread(target = self._run_app).start()

        asyncio.create_task(self._relay_console())

    def         stop               (self):
        self._server.shutdown()
    
    def         shutdown_link           (self, user : str):
        id = self._generate_id()

        while id in self.shutdown_requests: 
            id = self._generate_id()

        self.shutdown_requests[id] = {'user': user}

        link = f'{self.addres}/shutdown?id={id}'
        log = f'{user} requested a shutdown link. The generated link is: {link}'
        self._log_queue.put(self.log_format(log))

        return link
     
    ###         Download Logic      ###
    
    async def   _remove_link            (self, id: str):
        await asyncio.sleep(60)

        if id in self.active_downloads.keys():
            self.active_downloads.pop(id)
            log = f'Link with id {id} was removed'
            self._log_queue.put(self.log_format(log))
    
    def         _generate_id            (self):
        current_time = datetime.now().isoformat(timespec='microseconds')

        encoded_time = current_time.encode()
        id = hashlib.sha256(encoded_time).hexdigest()

        id += f'.{random.randint(20000, 30000)}'

        return id

    def         download_link           (self, file_path: str, user : str):
        id = self._generate_id()

        while id in self.active_downloads.keys(): 
            id = self._generate_id()

        self.active_downloads[id] = {'user' : user, 'file': file_path}
        if self.temporary_links: asyncio.create_task(self._remove_link(id))

        link = f'{self.addres}/file_request?id={id}'
        log = f'{user} requested the file located at {file_path}. The generated link is: {link}'
        self._log_queue.put(self.log_format(log))

        return link
  
    ###         Utils               ###

    def         clean_active_links      (self):
        if not self.is_running: return

        self.active_downloads = {}
        log = f'Active links have been removed.'
        self._log_queue.put(self.log_format(log))
    
    def         log_format              (self, log: str, type: str = 'INFO'):
        return f'[McDis] [Flask] [{datetime.now().strftime("%H:%M:%S")}]: {log}'
    
    async def   send_to_console         (self, message : str):
        mrkd = f'```md\n{truncate(message, 1990)}\n```'
        remote_console = await thread(f'Console Flask', self.client.panel)

        await remote_console.send(mrkd)

    async def   _relay_console          (self):
        remote_console      = await thread(f'Console Flask', self.client.panel)
        await remote_console.send('```\n[Flask Running]\n```')

        while self.is_running:
            if not self._log_queue.empty():
                log = self._log_queue.get()
                await remote_console.send(f'```md\n{log}```')

                if 'Shutdown signal received' in log: 
                    self.stop()
                    break
                
            await asyncio.sleep(0.5)
            
        await remote_console.send('```\n[Flask Stopped]\n```')