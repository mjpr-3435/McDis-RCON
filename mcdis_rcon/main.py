from .modules import *

def start():
    locales_dir = os.path.join(package_path, 'locales')
    try:
        for language in allowed_languages[1:]:
            po_dir_path = os.path.join(locales_dir, language, 'LC_MESSAGES')
            po = polib.pofile(os.path.join(po_dir_path, 'app.po'))
            po.save_as_mofile(os.path.join(po_dir_path, 'app.mo'))
    except KeyError as error:
        pass
    
    print('Initializing McDis RCON...')
    from .classes import McDisClient
    McDisClient()