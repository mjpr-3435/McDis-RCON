from ..modules import *

def is_valid_path_name(folder_name) -> bool:
    pattern = r'^[A-Za-z0-9._\- ]+$'

    if re.match(pattern, folder_name):
        return True
    return False

def mcdis_path(path: str) -> str:
    return 'McDis' if path == '.' else os.path.join('McDis', path)

def un_mcdis_path(path: str) -> str:
    return '.' if path == 'McDis' else path.removeprefix(f'McDis{os.sep}')
   
def is_valid_mcdis_dir(path: str):
    from ..loader import _
    
    real_path = un_mcdis_path(path)
    new_path = os.path.join(cwd, real_path)
    
    if not path.split(os.sep)[0] == 'McDis':
        return _('✖ The path must be a McDis path. E.g.: `McDis/Backups`.')
    if not cwd in new_path:
        return _('✖ You must work within the directory where McDis is running.')
    elif not os.path.exists(real_path):
        return _('✖ The path must exist.')
    elif not os.path.isdir(real_path):
        return _('✖ The path must be a directory.')
    
    return True

def get_path_size(path: str, *, string = True) -> Union[str, int]:
    if not os.path.exists(path): return 'Not Found' if string else 0
    
    total = 0
    
    try:
        if not os.path.isdir(path):
            total = os.path.getsize(path)
        
        else:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_path_size(entry.path, string = False)
        
        if string:
            magnitude = ['B', 'KB', 'MB', 'GB', 'TB']
            i = int(math.log(total, 1024)) if total != 0 else 0

            return f'{total / (1024 ** (i)) :.1f} {magnitude[i]}'
        else: 
            return total

    except:
        return 'Error' if string else 0

def make_zip(source : str, destination : str, counter : list = None):
    if counter: counter[0], counter[1] = 0, files_on(source)
    
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                zipf.write(dir_path, os.path.relpath(dir_path, source) + '/')
                if counter: counter[0] += 1
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source))
                if counter: counter[0] += 1

def unpack_zip(source: str, destination: str, counter: list = None):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        if counter:
            counter[0], counter[1] = 0, total_files

        for file in zip_ref.namelist():
            zip_ref.extract(file, destination)
            if counter: counter[0] += 1

def files_on(path : str, *, files : bool = True, dirs : bool = True):
    if not os.path.isdir(path): return 1

    total = 0
    for root, dirs, files in os.walk(path):
        if dirs: total += len(dirs)
        if files: total += len(files)

    return total