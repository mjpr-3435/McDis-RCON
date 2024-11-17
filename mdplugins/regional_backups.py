import asyncio
import zipfile
import json
import time
import os
import re

from datetime import datetime
from mcdis_rcon.utils import hover_and_suggest, extras
from mcdis_rcon.bot.classes import Server

targets = []
waiting = {}
files_to_zip = {}
creating_bkp = False
admins = []

async def load(self: Server):
    global admins

    path_file = os.path.join(self.path_plugins_config, 'regional_backups.json')
    dictionary = {
        'Admins' : []
        }
    
    os.makedirs(os.path.join(self.path_plugins, 'reg-bkps'), exist_ok = True)

    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding = 'utf-8') as file:
        config = json.load(file)

    admins = config['Admins']

async def on_player_command(self: Server, player: str, message: str):
    global targets, files_to_zip, waiting, creating_bkp
    
    reg_bkps_dir = os.path.join(self.path_plugins, 'reg-bkps')
    zips = [x for x in os.listdir(reg_bkps_dir) if x.endswith('.zip')]

    if not player in admins:
        return
    
    elif self.is_command(message, 'help'):
        self.show_command(player, 'rb help'           , 'Muestra los comandos del regional backup.')

    elif self.is_command(message, 'rb help'):
        self.show_command(player, 'rb clear'          , 'Limpia tu lista.')
        self.show_command(player, 'rb list'           , 'Muestra tu lista de regiones.')
        self.show_command(player, 'rb add'            , 'Añade a tu lista una región.')
        self.show_command(player, 'rb del <index>'    , 'Elimina la región de índice <index> de tu lista.')
        self.show_command(player, 'rb mk-bkp <name>'  , 'Crea un reg-bkp <name>.zip con las regiones añadidas.')
        self.show_command(player, 'rb bkps'           , 'Lista los backups creados.')
        self.show_command(player, 'rb load-bkp <name>', 'Carga el reg-bkp <name>.zip.')
        self.show_command(player, 'rb del-bkp <name>' , 'Elimina el reg-bkp <name>.zip.')

    elif self.is_command(message, 'rb add'):
        self.execute(f'data get entity {player}')
        targets.append(player)
    
    elif self.is_command(message, 'rb del'):
        index = int(message.removeprefix(f'{self.prefix}rb del'))
        if not player in files_to_zip.keys(): 
            self.send_response(player, 'Lista vacía.')
        elif not any(len(files_to_zip[player][dim]) for dim in ['overworld', 'the_nether', 'the_end']): 
            self.send_response(player, 'Lista vacía.')
        else:
            i = 0
            for dim in files_to_zip[player].keys():
                for reg in files_to_zip[player][dim]:
                    i += 1
                    if index == i:
                        files_to_zip[player][dim].remove(reg)
            show_list(self, player)
    
    elif self.is_command(message, 'rb load-bkp'):
        zip = message.removeprefix(f'{self.prefix}rb load-bkp').strip() + '.zip'

        if zip in zips:
            self.stop()

            while self.state() != 'Closed':
                await asyncio.sleep(0.1)

            await self.send_to_console(f'Unpacking reg-bkp {zip}...')

            source = os.path.join(self.path_plugins, 'reg-bkps', zip)
            destination = os.path.join(self.path_server, 'world')

            with zipfile.ZipFile(source, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    zip_ref.extract(file, destination)

            await self.send_to_console(f'Reg-bkp {zip} unpacked.')

            self.start()

        else:
            self.send_response(player, '✖ No hay un reg-bkp con ese nombre.')

    elif self.is_command(message, 'rb del-bkp'):
        zip = message.removeprefix(f'{self.prefix}rb del-bkp').strip() + '.zip'

        if zip in zips:
            os.remove(os.path.join(reg_bkps_dir, zip))
            show_bkps(self, player)
            self.send_response(player, f'✔ reg-bkp {zip} eliminado.')
        else:
            self.send_response(player, '✖ No hay un reg-bkp con ese nombre.')

    elif self.is_command(message, 'rb list'):
        show_list(self, player)
    
    elif self.is_command(message, 'rb bkps'):
        show_bkps(self, player)

    elif self.is_command(message, 'rb clear'):
        files_to_zip[player] = {'overworld':[],
                                'the_nether':[],
                                'the_end':[]}
        show_list(self, player)

    elif self.is_command(message, 'rb mk-bkp'):
        name = message.removeprefix(f'{self.prefix}rb mk-bkp').strip()
        destination = os.path.join(reg_bkps_dir, f'{name}.zip')
        os.makedirs(os.path.dirname(destination), exist_ok = True)

        if not files_to_zip: 
            self.send_response(player, '✖ No has agregado ninguna región.')
            return
        elif not name: 
            self.send_response(player, '✖ Debes proveer un nombre.')
            return
        elif creating_bkp: 
            self.send_response(player, '✖ Alguien más está creando un backup ahorita.')
            return
        
        creating_bkp = True
        waiting[player] = True

        self.execute('save-off')
        self.execute('save-all')

        while waiting[player]:
            await asyncio.sleep(1)

        self.send_response(player, f'Creando {name}.zip...')
        with zipfile.ZipFile(destination, 'w') as zipf:
            for dim in files_to_zip[player].keys():
                if dim == 'overworld':
                    entities, region, poi = 'entities', 'region', 'poi'
                elif dim == 'the_nether':
                    entities, region, poi = os.path.join('DIM-1','entities'), os.path.join('DIM-1','region'), os.path.join('DIM-1','poi')
                elif dim == 'the_end':
                    entities, region, poi = os.path.join('DIM1','entities'), os.path.join('DIM1','region'), os.path.join('DIM1','poi')
                
                for reg in files_to_zip[player][dim]:
                    file_path = os.path.join(self.path_server, 'world', region, reg)
                    zipf.write(file_path, os.path.join(region, reg))
                    file_path = os.path.join(self.path_server, 'world', poi, reg)
                    zipf.write(file_path, os.path.join(poi, reg))
                    file_path = os.path.join(self.path_server, 'world', entities, reg)
                    zipf.write(file_path, os.path.join(entities, reg))

        self.execute('save-on')
        self.send_response(player, f'✔ reg-bkp {name}.zip creado.')
        self.add_log(f'reg-bkp {name}.zip created')
        creating_bkp = False

async def listener_events(self: Server, log : str):
    global targets, files_to_zip, waiting

    if not 'INFO]:' in log: 
        pass

    elif any(f'{x} has the following entity data' in log for x in targets):
        match = re.search(r"(.*?) has the following entity data: (.*)", log)
        player = match.group(1).strip().split(' ')[-1]
        data = match.group(2)
        raw_pos = data[data.find('Pos:'):]
        raw_pos = raw_pos[raw_pos.find('[') + 1 : raw_pos.find(']')].split(',')
        raw_dim = data[data.find('Dimension:'):]
        dim     = raw_dim[raw_dim.find('"') + 1 : raw_dim.find(',')-1].split(':')[1]
        pos     = tuple(float(x.strip()[:-1]) for x in raw_pos)
        reg     = pos_to_region(pos)

        if not player in files_to_zip.keys(): files_to_zip[player] = {'overworld':[],
                                                                      'the_nether':[],
                                                                      'the_end':[]}

        if not reg in files_to_zip[player][dim]: files_to_zip[player][dim].append(reg)

        show_list(self, player)
        targets.remove(player)
        
    elif log.endswith('Saved the game'):
        for key in waiting.keys():
            waiting[key] = False

def show_list(self: Server, player : str):
    if not player in files_to_zip.keys():
        self.send_response(player, 'Lista vacía.')
        return
    
    msg = []
    i = 0
    for dim in files_to_zip[player].keys():
        for reg in files_to_zip[player][dim]:
            i += 1
            msg .append(f'{i} • {dim} : {reg}')
    
    if len(msg):
        msg.insert(0, f'{player}, region list:')
    else:
        msg = 'Lista vacía.'
    self.send_response(player, msg)

def show_bkps(self: Server, player : str):
    reg_bkps_dir = os.path.join(self.path_plugins, 'reg-bkps')
    zips = [x for x in os.listdir(reg_bkps_dir) if x.endswith('.zip')]

    if not zips:
        self.send_response(player, 'No se han creado backups.')
        return
    
    self.send_response(player, 'Reg-bkps disponibles:')

    for zip in zips:
        date = datetime.fromtimestamp(os.path.getctime(os.path.join(reg_bkps_dir, zip))).strftime("%Y-%m-%d %H:%M:%S")

        dummy = [
        hover_and_suggest('[>] ' , color = 'green', suggest = f'!!rb load-bkp {zip[:-4]}', hoover = 'Load reg-bkp'),
        hover_and_suggest('[⥁] ', color = 'aqua', suggest = f'!!rb mk-bkp {zip[:-4]}', hoover = 'Remake reg-bkp'),
        hover_and_suggest('[x] ' , color = 'red', suggest = f'!!rb del-bkp {zip[:-4]}', hoover = 'Del reg-bkp'),
        f'{{"text":"{zip} [{date}]"}}'
        ]

        self.execute(f'tellraw {player} {extras(dummy)}')

def pos_to_region(pos : tuple):
    r_x = int(pos[0] // (32*16))
    r_z = int(pos[2] // (32*16))

    return f"r.{r_x}.{r_z}.mca"