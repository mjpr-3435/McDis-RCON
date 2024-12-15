from .modules import *

def run():
    print(f'Initializing McDis RCON v{mcdis_vers}...')
    from .classes.McDisClient import McDisClient
    McDisClient()

def update_po():
    locales_dir = os.path.join(package_path, 'locales')
    for language in allowed_languages[1:]:
        po_dir_path = os.path.join(locales_dir, language, 'LC_MESSAGES')
        po = polib.pofile(os.path.join(po_dir_path, 'app.po'))
        po.save_as_mofile(os.path.join(po_dir_path, 'app.mo'))