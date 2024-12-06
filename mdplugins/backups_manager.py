import asyncio
import threading
import zipfile
import json
import time
import os
import re

from datetime import datetime
from mcdis_rcon.utils import hover_and_suggest, extras
from mcdis_rcon.classes import Server

admins = []

async def load(server: Server):
    global admins

    path_file = os.path.join(server.path_plugins_configs, 'backups_manager.json')
    dictionary = {
        'Admins' : []
        }

    if not os.path.exists(path_file):
        os.makedirs(server.path_plugins_configs, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    admins = config['Admins']

async def on_player_command(server: Server, player: str, message: str):
    zips = [x for x in os.listdir(server.path_bkps) if x.endswith('.zip')]

    if not player in admins:
        return
    
    elif server.is_command(message, 'help'):
        server.show_command(player, 'gb help'          , 'Muestra los comandos del backups manager.')

    elif server.is_command(message, 'gb help'):
        server.show_command(player, 'bkps'             , 'Lista los backups del servidor.')
        server.show_command(player, 'mk-bkp'           , 'Crea un backup con la lógica de McDis.')
        server.show_command(player, 'del-bkp <name>'   , 'Elimina el backup <name>.zip.')
        server.show_command(player, 'load-bkp <name>'  , 'Carga el backup <name>.zip.')
    
    elif server.is_command(message, 'mk-bkp'):
        server.stop()

        while server.is_running():
            await asyncio.sleep(0.1)

        await server.send_to_console('Creating backup...')

        task = threading.Thread(target = server.make_bkp)
        task.start()
            
        while task.is_alive():
            await asyncio.sleep(0.5)

        await server.send_to_console('Backup created.')

        server.start()

    elif server.is_command(message, 'load-bkp'):
        zip = message.removeprefix(f'{server.prefix}load-bkp').strip() + '.zip'

        if zip in zips:
            server.stop()

            while server.is_running():
                await asyncio.sleep(0.1)

            await server.send_to_console(f'Unpacking the backup {zip}...')

            task = threading.Thread(target = server.unpack_bkp, args = (zip,))
            task.start()
                
            while task.is_alive():
                await asyncio.sleep(0.5)

            await server.send_to_console(f'Backup {zip} unpacked.')

            server.start()

        else:
            server.send_response(player, '✖ No hay un backup con ese nombre.')

    elif server.is_command(message, 'del-bkp'):
        zip = message.removeprefix(f'{server.prefix}del-bkp').strip() + '.zip'

        if zip in zips:
            os.remove(os.path.join(server.path_bkps, zip))
            show_bkps(server, player)
            server.send_response(player, f'✔ Backup {zip} eliminado.')
        else:
            server.send_response(player, '✖ No hay un backup con ese nombre.')
    
    elif server.is_command(message, 'bkps'):
        show_bkps(server, player)

def show_bkps(server: Server, player : str):
    zips = [x for x in os.listdir(server.path_bkps) if x.endswith('.zip')]
    zips.sort()
    
    if not zips:
        server.send_response(player, 'No se han creado backups.')
        return
    
    server.send_response(player, 'Backups disponibles:')

    for zip in zips:
        date = datetime.fromtimestamp(os.path.getctime(os.path.join(server.path_bkps, zip))).strftime("%Y-%m-%d %H:%M:%S")

        dummy = [
        hover_and_suggest('[>] ' , color = 'green', suggest = f'!!load-bkp {zip.removesuffix(".zip")}', hoover = 'Load backup'),
        hover_and_suggest('[x] ' , color = 'red', suggest = f'!!del-bkp {zip.removesuffix(".zip")}', hoover = 'Del backup'),
        f'{{"text":"{zip} [{date}]"}}'
        ]

        server.execute(f'tellraw {player} {extras(dummy)}')