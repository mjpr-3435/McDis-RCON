import requests
import hashlib
import uuid

def mc_uuid(player: str, *, online : bool = True):
    if online:
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}')

        if response.status_code == 200:
            data = response.json()
            return uuid.UUID(data['id'])
    else:
        hash = hashlib.md5(f"OfflinePlayer:{player}".encode('utf-8')).digest()
        byte_array = [byte for byte in hash]
        byte_array[6] = hash[6] & 0x0f | 0x30
        byte_array[8] = hash[8] & 0x3f | 0x80

        hash_modified = bytes(byte_array)
        offline_player_uuid = uuid.UUID(hash_modified.hex())

        return offline_player_uuid

def online_uuid_to_name(uuid : str):
    response = requests.get(f"https://api.mojang.com/user/profiles/{uuid.replace('-', '')}/names")

    if response.status_code == 200:
        current_name = response.json()[-1]["name"]
        return current_name
    else:
        return 'Not Found'