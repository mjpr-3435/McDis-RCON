import asyncio
import zipfile
import json
import time
import os
import re

from datetime import datetime
from mcdis_rcon.utils import hover_and_suggest, extras, json_to_dict, dict_to_json
from mcdis_rcon.classes import Server

class mdplugin():
    def __init__(self, server: Server):
        self.server = server
        self.server         = server
        self.targets        = []
        self.waiting        = {}
        self.files_to_zip   = {}
        self.creating_bkp   = False

    async def on_player_command(self, player: str, message: str):
        reg_bkps_dir = os.path.join(self.server.path_plugins, 'reg-bkps')
        os.makedirs(reg_bkps_dir, exist_ok = True)

        zips = [x for x in os.listdir(reg_bkps_dir) if x.endswith('.zip')]

        if not player in self.server.admins:
            return
        
        elif self.server.is_command(message, 'help'):
            self.server.show_command(player, 'rb help'           , 'Muestra los comandos del regional backup.')

        elif self.server.is_command(message, 'rb help'):
            self.server.show_command(player, 'rb clear'          , 'Limpia tu lista.')
            self.server.show_command(player, 'rb list'           , 'Muestra tu lista de regiones.')
            self.server.show_command(player, 'rb add'            , 'Añade a tu lista una región.')
            self.server.show_command(player, 'rb del <index>'    , 'Elimina la región de índice <index> de tu lista.')
            self.server.show_command(player, 'rb mk-bkp <name>'  , 'Crea un reg-bkp <name>.zip con las regiones añadidas.')
            self.server.show_command(player, 'rb bkps'           , 'Lista los backups creados.')
            self.server.show_command(player, 'rb load-bkp <name>', 'Carga el reg-bkp <name>.zip.')
            self.server.show_command(player, 'rb del-bkp <name>' , 'Elimina el reg-bkp <name>.zip.')

        elif self.server.is_command(message, 'rb add'):
            self.server.execute(f'data get entity {player}')
            self.targets.append(player)
        
        elif self.server.is_command(message, 'rb del'):
            index = int(message.removeprefix(f'{self.server.prefix}rb del'))
            if not player in self.files_to_zip.keys(): 
                self.server.send_response(player, 'Lista vacía.')
            elif not any(len(self.files_to_zip[player][dim]) for dim in ['overworld', 'the_nether', 'the_end']): 
                self.server.send_response(player, 'Lista vacía.')
            else:
                i = 0
                for dim in self.files_to_zip[player].keys():
                    for reg in self.files_to_zip[player][dim]:
                        i += 1
                        if index == i:
                            self.files_to_zip[player][dim].remove(reg)
                self.show_list(player)
        
        elif self.server.is_command(message, 'rb load-bkp'):
            zip = message.removeprefix(f'{self.server.prefix}rb load-bkp').strip() + '.zip'

            if zip in zips:
                self.server.stop()

                while self.server.is_running():
                    await asyncio.sleep(0.1)

                await self.server.send_to_console(f'Unpacking reg-bkp {zip}...')

                source = os.path.join(self.server.path_plugins, 'reg-bkps', zip)
                destination = os.path.join(self.server.path_files, 'server', 'world')

                with zipfile.ZipFile(source, 'r') as zip_ref:
                    for file in zip_ref.namelist():
                        zip_ref.extract(file, destination)

                await self.server.send_to_console(f'Reg-bkp {zip} unpacked.')

                self.server.start()

            else:
                self.server.send_response(player, '✖ No hay un reg-bkp con ese nombre.')

        elif self.server.is_command(message, 'rb del-bkp'):
            zip = message.removeprefix(f'{self.server.prefix}rb del-bkp').strip() + '.zip'

            if zip in zips:
                os.remove(os.path.join(reg_bkps_dir, zip))
                self.show_bkps(player)
                self.server.send_response(player, f'✔ reg-bkp {zip} eliminado.')
            else:
                self.server.send_response(player, '✖ No hay un reg-bkp con ese nombre.')

        elif self.server.is_command(message, 'rb list'):
            self.show_list(player)
        
        elif self.server.is_command(message, 'rb bkps'):
            self.show_bkps(player)

        elif self.server.is_command(message, 'rb clear'):
            self.files_to_zip[player] = {'overworld':[],
                                    'the_nether':[],
                                    'the_end':[]}
            self.show_list(player)

        elif self.server.is_command(message, 'rb mk-bkp'):
            name = message.removeprefix(f'{self.server.prefix}rb mk-bkp').strip()
            destination = os.path.join(reg_bkps_dir, f'{name}.zip')
            os.makedirs(os.path.dirname(destination), exist_ok = True)

            if not self.files_to_zip: 
                self.server.send_response(player, '✖ No has agregado ninguna región.')
                return
            elif not name: 
                self.server.send_response(player, '✖ Debes proveer un nombre.')
                return
            elif self.creating_bkp: 
                self.server.send_response(player, '✖ Alguien más está creando un backup ahorita.')
                return
            
            self.creating_bkp = True
            self.waiting[player] = True

            self.server.execute('save-off')
            self.server.execute('save-all')

            while self.waiting[player]:
                await asyncio.sleep(1)

            self.server.send_response(player, f'Creando {name}.zip...')
            with zipfile.ZipFile(destination, 'w') as zipf:
                for dim in self.files_to_zip[player].keys():
                    if dim == 'overworld':
                        entities, region, poi = 'entities', 'region', 'poi'
                    elif dim == 'the_nether':
                        entities, region, poi = os.path.join('DIM-1','entities'), os.path.join('DIM-1','region'), os.path.join('DIM-1','poi')
                    elif dim == 'the_end':
                        entities, region, poi = os.path.join('DIM1','entities'), os.path.join('DIM1','region'), os.path.join('DIM1','poi')
                    
                    for reg in self.files_to_zip[player][dim]:
                        file_path = os.path.join(self.server.path_files, 'server', 'world', region, reg)
                        zipf.write(file_path, os.path.join(region, reg))
                        file_path = os.path.join(self.server.path_files, 'server', 'world', poi, reg)
                        zipf.write(file_path, os.path.join(poi, reg))
                        file_path = os.path.join(self.server.path_files, 'server', 'world', entities, reg)
                        zipf.write(file_path, os.path.join(entities, reg))

            self.server.execute('save-on')
            self.server.send_response(player, f'✔ reg-bkp {name}.zip creado.')
            self.server.add_log(f'reg-bkp {name}.zip created')
            self.creating_bkp = False

    async def listener_events(self, log : str):
        if not 'INFO]:' in log: 
            pass

        elif any(f'{x} has the following entity data' in log for x in self.targets):
            match = re.search(r"(.*?) has the following entity data: (.*)", log)
            player = match.group(1).strip().split(' ')[-1]
            data = match.group(2)
            raw_pos = data[data.find('Pos:'):]
            raw_pos = raw_pos[raw_pos.find('[') + 1 : raw_pos.find(']')].split(',')
            raw_dim = data[data.find('Dimension:'):]
            dim     = raw_dim[raw_dim.find('"') + 1 : raw_dim.find(',')-1].split(':')[1]
            pos     = tuple(float(x.strip()[:-1]) for x in raw_pos)
            reg     = self.pos_to_region(pos)

            if not player in self.files_to_zip.keys(): self.files_to_zip[player] = {'overworld':[],
                                                                        'the_nether':[],
                                                                        'the_end':[]}

            if not reg in self.files_to_zip[player][dim]: self.files_to_zip[player][dim].append(reg)

            self.show_list(player)
            self.targets.remove(player)
            
        elif log.endswith('Saved the game'):
            for key in self.waiting.keys():
                self.waiting[key] = False

    def show_list(self, player : str):
        if not player in self.files_to_zip.keys():
            self.server.send_response(player, 'Lista vacía.')
            return
        
        msg = []
        i = 0
        for dim in self.files_to_zip[player].keys():
            for reg in self.files_to_zip[player][dim]:
                i += 1
                msg .append(f'{i} • {dim} : {reg}')
        
        if len(msg):
            msg.insert(0, f'{player}, region list:')
        else:
            msg = 'Lista vacía.'
        self.server.send_response(player, msg)

    def show_bkps(self, player : str):
        reg_bkps_dir = os.path.join(self.server.path_plugins, 'reg-bkps')
        zips = [x for x in os.listdir(reg_bkps_dir) if x.endswith('.zip')]
        zips.sort()
        
        if not zips:
            self.server.send_response(player, 'No se han creado backups.')
            return
        
        self.server.send_response(player, 'Reg-bkps disponibles:')

        for zip in zips:
            date = datetime.fromtimestamp(os.path.getctime(os.path.join(reg_bkps_dir, zip))).strftime("%Y-%m-%d %H:%M:%S")

            dummy = [
            hover_and_suggest('[>] ' , color = 'green', suggest = f'!!rb load-bkp {zip.removesuffix(".zip")}', hoover = 'Load reg-bkp'),
            hover_and_suggest('[⥁] ', color = 'aqua', suggest = f'!!rb mk-bkp {zip.removesuffix(".zip")}', hoover = 'Remake reg-bkp'),
            hover_and_suggest('[x] ' , color = 'red', suggest = f'!!rb del-bkp {zip.removesuffix(".zip")}', hoover = 'Del reg-bkp'),
            f'{{"text":"{zip} [{date}]"}}'
            ]

            self.server.execute(f'tellraw {player} {extras(dummy)}')

    def pos_to_region(self, pos : tuple):
        r_x = int(pos[0] // (32*16))
        r_z = int(pos[2] // (32*16))

        return f"r.{r_x}.{r_z}.mca"