import asyncio
import threading
import os

from datetime import datetime
from mcdis_rcon.utils import hover_and_suggest, extras
from mcdis_rcon.classes import Server

class mdplugin():
    def __init__(self, server: Server):
        self.server = server

    async def on_player_command(self, player: str, message: str):
        zips = [x for x in os.listdir(self.server.path_bkps) if x.endswith('.zip')]

        if not player in self.server.admins:
            return
        
        elif self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'gb help'          , 'Muestra los comandos del backup manager.')

        elif self.server.is_command(message, 'gb help'):
            self.server.show_command(player, 'bkps'             , 'Lista los backups del servidor.')
            self.server.show_command(player, 'mk-bkp'           , 'Crea un backup con la lógica de McDis.')
            self.server.show_command(player, 'del-bkp <name>'   , 'Elimina el backup <name>.zip.')
            self.server.show_command(player, 'load-bkp <name>'  , 'Carga el backup <name>.zip.')
        
        elif self.server.is_command(message, 'mk-bkp'):
            self.server.stop()

            while self.server.is_running():
                await asyncio.sleep(0.1)

            await self.server.send_to_console('Creating backup...')

            task = threading.Thread(target = self.server.make_bkp)
            task.start()
                
            while task.is_alive():
                await asyncio.sleep(0.5)

            await self.server.send_to_console('Backup created.')

            self.server.start()

        elif self.server.is_command(message, 'load-bkp'):
            zip = message.removeprefix(f'{self.server.prefix}load-bkp').strip() + '.zip'

            if zip in zips:
                self.server.stop()

                while self.server.is_running():
                    await asyncio.sleep(0.1)

                await self.server.send_to_console(f'Unpacking the backup {zip}...')

                task = threading.Thread(target = self.server.unpack_bkp, args = (zip,))
                task.start()
                    
                while task.is_alive():
                    await asyncio.sleep(0.5)

                await self.server.send_to_console(f'Backup {zip} unpacked.')

                self.server.start()

            else:
                self.server.send_response(player, '✖ No hay un backup con ese nombre.')

        elif self.server.is_command(message, 'del-bkp'):
            zip = message.removeprefix(f'{self.server.prefix}del-bkp').strip() + '.zip'

            if zip in zips:
                os.remove(os.path.join(self.server.path_bkps, zip))
                self.show_bkps(player)
                self.server.send_response(player, f'✔ Backup {zip} eliminado.')
            else:
                self.server.send_response(player, '✖ No hay un backup con ese nombre.')
        
        elif self.server.is_command(message, 'bkps'):
            self.show_bkps(player)

    def show_bkps(self, player : str):
        zips = [x for x in os.listdir(self.server.path_bkps) if x.endswith('.zip')]
        zips.sort()
        
        if not zips:
            self.server.send_response(player, 'No se han creado backups.')
            return
        
        self.server.send_response(player, 'Backups disponibles:')

        for zip in zips:
            date = datetime.fromtimestamp(os.path.getctime(os.path.join(self.server.path_bkps, zip))).strftime("%Y-%m-%d %H:%M:%S")

            dummy = [
            hover_and_suggest('[>] ' , color = 'green', suggest = f'!!load-bkp {zip.removesuffix(".zip")}', hover = 'Load backup'),
            hover_and_suggest('[x] ' , color = 'red', suggest = f'!!del-bkp {zip.removesuffix(".zip")}', hover = 'Del backup'),
            f'{{"text":"{zip} [{date}]"}}'
            ]

            self.server.execute(f'tellraw {player} {extras(dummy)}')