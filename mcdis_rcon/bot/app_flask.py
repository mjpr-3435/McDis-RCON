from .pm_functions import *
from .modules import *

from .loader import _, config, panel

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(package_path, 'extras'), 'mcdis.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/file_request', methods=['GET'])
def download_file():
    id = request.args.get('id')
    from .pm_loader import flask_manager
    
    if id in flask_manager.active_downloads.keys():
        filepath = flask_manager.active_downloads[id]['file']
        user = flask_manager.active_downloads[id]['user']
        filepath = os.path.join(cwd, filepath)
        flask_manager.active_downloads.pop(id)

        print(f'Link requested by: {user} -> Used')

        return send_file(filepath, as_attachment = True)
    return abort(404)

