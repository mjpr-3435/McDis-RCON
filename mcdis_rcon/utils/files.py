from ..modules import *

def read_properties(file_path : str):
    if not os.path.exists(file_path): return {}

    properties = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                properties[key] = value
    return properties

def read_dat_files(file_path : str): 
    return nbtlib.load(file_path)

def show_dat_files(*, file_path : str = None, nbt = None): 
    if file_path: nbt = nbtlib.load(file_path)
    
    if nbt != None:
        formatted_output = json.dumps(dat_to_dict(nbt), indent=4)
        print(formatted_output)

def dat_to_dict(nbt):
    if isinstance(nbt, nbtlib.tag.Compound):
        return {key: dat_to_dict(value) for key, value in nbt.items()}
    elif isinstance(nbt, nbtlib.tag.List):
        return [dat_to_dict(item) for item in nbt]
    elif isinstance(nbt, nbtlib.tag.IntArray):
        return list(nbt)
    else:
        return nbt

def read_file(file_path: str) -> str:
    with open(file_path, 'r', encoding = 'utf-8') as file:
        return file.read()

def write_in_file(file_path: str, content: str):
    with open(file_path, 'w') as file:
        for line in content.split('\n'):
            file.write(line + '\n')

def read_yml(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping = 2, sequence = 4, offset=2)
        yaml.preserve_quotes = True

        return yaml.load(file)

def is_valid_path_name(folder_name) -> bool:
    pattern = r'^[A-Za-z0-9._\- ]+$'

    if re.match(pattern, folder_name):
        return True
    return False

def mcdis_path(path: str) -> str:
    return 'McDis' if path == '.' else os.path.join('McDis', path)

def un_mcdis_path(path: str) -> str:
    return '.' if path == 'McDis' else path.removeprefix(f'McDis{os.sep}')

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
    if counter: counter[0], counter[1] = 0, elements_on(source)
    
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

def elements_on(path: str, *, include_files: bool = True, include_dirs: bool = True, recursive: bool = True):
    if not os.path.isdir(path):
        return 1

    total = 0

    if recursive:
        for root, dirs, files in os.walk(path):
            if include_dirs:
                total += len(dirs)
            if include_files:
                total += len(files)
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and include_files:
                    total += 1
                elif entry.is_dir() and include_dirs:
                    total += 1

    return total
