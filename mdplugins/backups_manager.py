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

async def load(self: Server):
    global admins

    path_file = os.path.join(self.path_plugins_config, 'backups_manager.json')
    dictionary = {
        'Admins' : []
        }

    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    admins = config['Admins']

async def on_player_command(self: Server, player: str, message: str):
    zips = [x for x in os.listdir(self.path_bkps) if x.endswith('.zip')]

    if not player in admins:
        return
    
    elif self.is_command(message, 'help'):
        self.show_command(player, 'gb help'          , 'Muestra los comandos del backups manager.')

    elif self.is_command(message, 'gb help'):
        self.show_command(player, 'bkps'             , 'Lista los backups del servidor.')
        self.show_command(player, 'mk-bkp'           , 'Crea un backup con la lógica de McDis.')
        self.show_command(player, 'del-bkp <name>'   , 'Elimina el backup <name>.zip.')
        self.show_command(player, 'load-bkp <name>'  , 'Carga el backup <name>.zip.')
    
    elif self.is_command(message, 'mk-bkp'):
        self.stop()

        while self.state() != 'Closed':
            await asyncio.sleep(0.1)

        await self.send_to_console('Creating backup...')

        task = threading.Thread(target = self.make_bkp)
        task.start()
            
        while task.is_alive():
            await asyncio.sleep(0.5)

        await self.send_to_console('Backup created.')

        self.start()

    elif self.is_command(message, 'load-bkp'):
        zip = message.removeprefix(f'{self.prefix}load-bkp').strip() + '.zip'

        if zip in zips:
            self.stop()

            while self.state() != 'Closed':
                await asyncio.sleep(0.1)

            await self.send_to_console(f'Unpacking the backup {zip}...')

            task = threading.Thread(target = self.unpack_bkp, args = (zip,))
            task.start()
                
            while task.is_alive():
                await asyncio.sleep(0.5)

            await self.send_to_console(f'Backup {zip} unpacked.')

            self.start()

        else:
            self.send_response(player, '✖ No hay un backup con ese nombre.')

    elif self.is_command(message, 'del-bkp'):
        zip = message.removeprefix(f'{self.prefix}del-bkp').strip() + '.zip'

        if zip in zips:
            os.remove(os.path.join(self.path_bkps, zip))
            show_bkps(self, player)
            self.send_response(player, f'✔ Backup {zip} eliminado.')
        else:
            self.send_response(player, '✖ No hay un backup con ese nombre.')
    
    elif self.is_command(message, 'bkps'):
        show_bkps(self, player)

def show_bkps(self: Server, player : str):
    zips = [x for x in os.listdir(self.path_bkps) if x.endswith('.zip')]

    if not zips:
        self.send_response(player, 'No se han creado backups.')
        return
    
    self.send_response(player, 'Backups disponibles:')

    for zip in zips:
        date = datetime.fromtimestamp(os.path.getctime(os.path.join(self.path_bkps, zip))).strftime("%Y-%m-%d %H:%M:%S")

        dummy = [
        hover_and_suggest('[>] ' , color = 'green', suggest = f'!!load-bkp {zip.removesuffix(".zip")}', hoover = 'Load backup'),
        hover_and_suggest('[x] ' , color = 'red', suggest = f'!!del-bkp {zip.removesuffix(".zip")}', hoover = 'Del backup'),
        f'{{"text":"{zip} [{date}]"}}'
        ]

        self.execute(f'tellraw {player} {extras(dummy)}')