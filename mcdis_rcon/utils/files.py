import json
import math
import os
import re
import shutil
import subprocess
import zipfile
from collections.abc import Callable, Mapping, Sequence
from typing import Any, cast

import nbtlib  # type: ignore[import-untyped]
import ruamel.yaml


def load_nbt_file(file_path: str) -> Any:
    nbtlib_module = cast(Any, nbtlib)
    load = cast(Callable[[str], Any], nbtlib_module.load)
    return load(file_path)


def read_properties(file_path: str) -> dict[str, str]:
    if not os.path.exists(file_path):
        return {}

    properties: dict[str, str] = {}
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                properties[key] = value
    return properties


def read_dat_files(file_path: str) -> Any:
    return load_nbt_file(file_path)


def show_dat_files(*, file_path: str | None = None, nbt: Any = None) -> None:
    if file_path:
        nbt = load_nbt_file(file_path)

    if nbt is not None:
        formatted_output = json.dumps(dat_to_dict(nbt), indent=4)
        print(formatted_output)


def dat_to_dict(nbt: Any) -> Any:
    if isinstance(nbt, nbtlib.tag.Compound):
        compound = cast(Mapping[str, Any], nbt)
        return {key: dat_to_dict(value) for key, value in compound.items()}
    elif isinstance(nbt, nbtlib.tag.List):
        nbt_list = cast(Sequence[Any], nbt)
        return [dat_to_dict(item) for item in nbt_list]
    elif isinstance(nbt, nbtlib.tag.IntArray):
        return list(nbt)
    else:
        return nbt


def read_file(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as file:
        return file.read()


def write_in_file(file_path: str, content: str) -> None:
    with open(file_path, 'w') as file:
        for line in content.split('\n'):
            file.write(line + '\n')


def read_yml(file_path: str) -> Any:
    with open(file_path) as file:
        yaml_loader = ruamel.yaml.YAML()
        yaml_loader.indent(mapping=2, sequence=4, offset=2)
        yaml_loader.preserve_quotes = True

        yaml_loader_any = cast(Any, yaml_loader)
        load = cast(Callable[[Any], Any], yaml_loader_any.load)
        return load(file)


def is_valid_path_name(folder_name: str) -> bool:
    pattern = r'^[A-Za-z0-9._\- ]+$'
    return bool(re.match(pattern, folder_name))


def mcdis_path(path: str) -> str:
    return 'McDis' if path == '.' else os.path.join('McDis', path)


def un_mcdis_path(path: str) -> str:
    return '.' if path == 'McDis' else path.removeprefix(f'McDis{os.sep}')


def get_path_size(path: str, *, string: bool = True) -> str | int:
    try:
        result = subprocess.run(
            ['du', '-sb', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        total = int(result.stdout.split()[0])

        if string:
            magnitude = ['B', 'KB', 'MB', 'GB', 'TB']
            i = int(math.log(total, 1024)) if total != 0 else 0
            return f'{total / (1024**i):.1f} {magnitude[i]}'
        else:
            return total

    except Exception:
        return 'Error' if string else 0


def copy_dir(source: str, destination: str, counter: list[int] | None = None) -> None:
    if counter:
        counter[0], counter[1] = 0, elements_on(source)

    def copy_with_counter(src: str, dst: str) -> str:
        shutil.copy2(src, dst)
        if counter:
            counter[0] += 1
        return dst

    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        copy_function=copy_with_counter,
    )


def make_zip(source: str, destination: str, counter: list[int] | None = None) -> None:
    if counter:
        counter[0], counter[1] = 0, elements_on(source)

    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                zipf.write(dir_path, os.path.relpath(dir_path, source) + '/')
                if counter:
                    counter[0] += 1
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source))
                if counter:
                    counter[0] += 1


def unpack_zip(source: str, destination: str, counter: list[int] | None = None) -> None:
    with zipfile.ZipFile(source, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())

        if counter:
            counter[0], counter[1] = 0, total_files

        for file in zip_ref.namelist():
            zip_ref.extract(file, destination)
            if counter:
                counter[0] += 1


def elements_on(path: str, *, include_files: bool = True, include_dirs: bool = True, recursive: bool = True) -> int:
    if not os.path.isdir(path):
        return 1

    total = 0

    if recursive:
        for _root, dirs, files in os.walk(path):
            if include_dirs:
                total += len(dirs)
            if include_files:
                total += len(files)
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and include_files or entry.is_dir() and include_dirs:
                    total += 1

    return total


def dict_to_json(path_file: str, dictionary: dict[str, Any]) -> None:
    with open(path_file, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)


def json_to_dict(path_file: str) -> Any:
    with open(path_file, encoding='utf-8') as file:
        return json.load(file)
