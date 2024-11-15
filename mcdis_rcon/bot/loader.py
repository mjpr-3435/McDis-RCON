from .pm_functions import *
from .modules import *

config : dict                               = {}
panel  : discord.TextChannel                = None
_      : gettext.GNUTranslations.gettext    = None

def start():
    global _, config

    print('Initializing McDis RCON...')
    load_config()

    from .client import run_client
    run_client()

def load_config():
    global _, config

    try:
        with open('md_config.yml', "r+") as file:
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping = 2, sequence = 4, offset = 2)
            yaml.preserve_quotes = True

            config = yaml.load(file)

    except Exception as error:
        print('The file \'md_config.yml\' could not be opened.')
        print(f'Error: {error}')
        os._exit(0)

    try:
        if      not isinstance(config['Bot Token'], str):
            print('The \'Bot Token\' variable must be a string.')
            os._exit(0)

        elif    not isinstance(config['Panel ID'], int):
            print('The \'Panel ID\' variable must be an integer.')
            os._exit(0)

        elif    not config['Language'] in allowed_languages:
            print(f'The \'Language\' variable must be one of the following: {", ".join(allowed_languages)}.')
            os._exit(0)

        elif    not isinstance(config['Backups'], int):
            print(f'The \'Backups\' variable must be an integer between 1 and 5.')
            os._exit(0)

        elif    not config['Backups'] in list(range(1,6)):
            print(f'The \'Backups\' variable must be between 1 and 5, not {config["Backups"]}.')
            os._exit(0)

        elif    not isinstance(config['Booleans']['upload overwrite'], bool):
            print('The \'Booleans: upload overwrite\' variable must be a boolean.')
            os._exit(0)

        elif    not isinstance(config['Booleans']['allow flask'], bool):
            print('The \'Booleans: allow flask\' variable must be a boolean.')
            os._exit(0)
        
        if      not config['Booleans']['allow flask']: 
            pass

        elif    not isinstance(config['Flask']['IP'], str):
            print('The \'Flask: IP\' variable must be a string.')
            os._exit(0)

        elif    not isinstance(config['Flask']['Port'], int):
            print('The \'Flask: Port\' variable must be an integer.')
            os._exit(0)
        
        names = []
        
        for process_type in config['Processes']:
            if config['Processes'][process_type] == None: 
                config['Processes'][process_type] = []
                continue

            for process in config['Processes'][process_type]:
                process_config = config['Processes'][process_type][process]

                if not isinstance(process, str):
                    print(f'{process}: The process names must be string.')
                    os._exit(0)

                elif len(process) > 40:
                    print(f'{process}: The process name must not exceed 40 characters.')
                    os._exit(0)

                elif process in ['.mdbackups', '.mdaddons']:
                    print(f'{process}:  A process cannot be named \'.mdbackups\' or \'.mdaddons\'.')
                    os._exit(0)
                
                elif process.lower() in names:
                    print(f'You can\'t have two processes with the same name: {process}')
                    os._exit(0)

                elif not is_valid_path_name(process):
                    print(f'{process}: Process names can only contain letters, numbers, periods (.), hyphens (-), underscores (_), and spaces.')
                    os._exit(0)

                elif process_type == 'Servers' and not isinstance(process_config['mcdreforged'], bool):
                    print(f'{process}: The \'mcdreforged\' variable must be a boolean.')
                    os._exit(0)

                elif not isinstance(process_config['start_command'], str):
                    print(f'{process}: The \'start_command\' variable must be a string.')
                    os._exit(0)
                
                elif not isinstance(process_config['stop_command'], str):
                    print(f'{process}: The \'start_command\' variable must be a string.')
                    os._exit(0)

                elif not all([isinstance(x,str) for x in process_config['relay_blacklist']]):
                    print(f'{process}: The \'relay_blacklist\' variable must be a list of strings.')
                    os._exit(0)
                
                names.append(process.lower())
                    
    except KeyError as error:
        print(f'Key not found: {error}.\nYour \'md_config.yml\' file is incomplete.\nPlease try requesting another one using \'mcdis init\'.')
        os._exit(0)
    
    
    locales_dir = os.path.join(package_path, 'locales')
    try:
        if config['Booleans']['dev']:
            for language in allowed_languages[1:]:
                po_dir_path = os.path.join(locales_dir, language, 'LC_MESSAGES')
                po = polib.pofile(os.path.join(po_dir_path, 'app.po'))
                po.save_as_mofile(os.path.join(po_dir_path, 'app.mo'))
    except KeyError as error:
        pass

    if config['Language'] != 'en':
        lang = gettext.translation('app', localedir = locales_dir, languages = [config['Language']])
    else:
        lang = gettext.NullTranslations()

    lang.install()
    _ = lang.gettext

    print(_('Your configuration has been loaded successfully.'))

def find_panel(client : commands.Bot):
    global panel, config, _

    panel_id = config['Panel ID']
    panel = client.get_channel(panel_id)
        
    if panel == None: 
        print(_('Error: Channel with id {} not found.').format(panel_id))
        os._exit(0)
    elif not isinstance(panel, discord.TextChannel): 
        print(_('Error: The panel channel must be a text channel.'))
        os._exit(0)
