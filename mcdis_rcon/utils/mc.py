import hashlib
import uuid

import requests


def mc_uuid(player: str, *, online: bool = True) -> str:
    if online:
        try:
            response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return str(uuid.UUID(data['id']))
        except Exception:
            return '00000000-0000-0000-0000-000000000000'
        return '00000000-0000-0000-0000-000000000000'
    else:
        hashed = hashlib.md5(f'OfflinePlayer:{player}'.encode()).digest()
        byte_array = list(hashed)
        byte_array[6] = hashed[6] & 0x0F | 0x30
        byte_array[8] = hashed[8] & 0x3F | 0x80

        hash_modified = bytes(byte_array)
        offline_player_uuid = str(uuid.UUID(hash_modified.hex()))

        return offline_player_uuid


def online_uuid_to_name(uuid: str) -> str:
    try:
        response = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}', timeout=5)
        if response.status_code == 200:
            return str(response.json().get('name', 'unknown'))
        return 'unknown'
    except Exception:
        return 'unknown'
