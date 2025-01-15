import asyncio
import zipfile
import json
import os
import re

from mcdis_rcon.utils import read_dat_files, mc_uuid, sct, hover_and_suggest, extras
from mcdis_rcon.classes import Server

target = ''

async def on_player_command(server: Server, player: str, message: str):
    global target
    
    if server.is_command(message, 'help'):
        server.show_command(player, 'finder pos1', 'Establece la posición 1.')
        server.show_command(player, 'finder pos2', 'Establece la posición 2.')

    elif server.is_command(message, 'finder pos1'):
        target = player
        server.execute(f'data get entity {player}')

    elif server.is_command(message, 'finder pos2'):
        target = player
        server.execute(f'data get entity {player}')


async def listener_events(server: Server, log : str):
    global target

    if not 'INFO]:' in log: 
        pass

    elif f'{target} has the following entity data' in log and target:
        match = re.search(r"has the following entity data: (.*)", log)
        data = match.group(1)
        raw_pos = data[data.find('Pos:'):]
        raw_pos = raw_pos[raw_pos.find('[') + 1 : raw_pos.find(']')].split(',')
        raw_dim = data[data.find('Dimension:'):]
        dim     = raw_dim[raw_dim.find('"') + 1 : raw_dim.find(',')-1].split(':')[1]
        
        x = int(float(raw_pos[0].strip()[:-1])) if float(raw_pos[0].strip()[:-1]) >= 0 else int(float(raw_pos[0].strip()[:-1]) - 1)
        y = int(float(raw_pos[1].strip()[:-1]))
        z = int(float(raw_pos[2].strip()[:-1])) if float(raw_pos[2].strip()[:-1]) >= 0 else int(float(raw_pos[2].strip()[:-1]) - 1)

        nbt = f'{{BlockState:{{Name:"minecraft:gray_stained_glass"}}, Glowing:1b, Invisible:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,NoGravity:1b,Time:1,DropItem:0b,HurtEntities:0b, Tags:["{target}p1"]}}'

        server.execute(f'summon minecraft:falling_block {x} {y} {z} {nbt}')
        await asyncio.sleep(10)
        server.execute(f'kill @e[tag={target}p1]')

        target = ''