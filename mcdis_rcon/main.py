from .modules import *

def run():
    locales_dir = os.path.join(package_path, 'locales')
    for language in allowed_languages[1:]:
        po_dir_path = os.path.join(locales_dir, language, 'LC_MESSAGES')
        po = polib.pofile(os.path.join(po_dir_path, 'app.po'))
        po.save_as_mofile(os.path.join(po_dir_path, 'app.mo'))
    
    print('Initializing McDis RCON...')
    from .classes import McDisClient
    McDisClient()