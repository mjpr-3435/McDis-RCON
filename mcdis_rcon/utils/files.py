import os
import json
import nbtlib

def read_properties(file_path : str):
    if not os.path.exists(file_path): return {}

    properties = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                properties[key] = value
    return properties

def read_dat_files(file_path : str): return nbtlib.load(file_path)

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
