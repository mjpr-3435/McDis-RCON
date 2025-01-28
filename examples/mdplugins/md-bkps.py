import asyncio
import threading
import zipfile
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
            self.server.show_command(player, 'bk help'          , 'Muestra los comandos del backup manager.')

        elif self.server.is_command(message, 'bk help'):
            self.server.show_command(player, 'bkps'             , 'Lista los backups del servidor.')
            self.server.show_command(player, 'mk-bkp'           , 'Crea un backup con la lógica de McDis.')
            self.server.show_command(player, 'del-bkp <name>'   , 'Elimina el backup <name>.zip.')
            self.server.show_command(player, 'load-bkp <name>'  , 'Carga el backup <name>.zip.')
        
        elif self.server.is_command(message, 'mk-bkp'):
            self.server.stop()

            while self.server.is_running():
                await asyncio.sleep(0.1)

            discord_message = await self.server.send_to_console('Creating backup...')

            counter = [0,0]
            reports = {'error': False}
            
            make_bkp = self.server.client.error_wrapper(
                error_title = f'{self.server.name}: make_bkp()',
                reports = reports
                )(self.server.make_bkp)

            task = threading.Thread(
                target = make_bkp, 
                kwargs = {'counter' : counter})
            task.start()
            
            while task.is_alive():
                if counter[1] == 0: 
                    await asyncio.sleep(0.1)
                else:
                    show = '```md\n[md-bkps]: [{}/{}] files have been compressed...\n```'\
                        .format(counter[0], counter[1])
                    await discord_message.edit(
                        content = show)
                    await asyncio.sleep(0.5)
            
            if reports['error']:
                msg = '```md\n[md-bkps]: ✖ An error occurred while compressing files.\n```'
            else:
                msg = '```md\n[md-bkps]: ✔ The files have been successfully compressed.\n```'

            await discord_message.edit(content = msg)

            self.server.start()

        elif self.server.is_command(message, 'load-bkp'):
            zip = message.removeprefix(f'{self.server.prefix}load-bkp').strip() + '.zip'

            if zip in zips:
                self.server.stop()

                while self.server.is_running():
                    await asyncio.sleep(0.1)
                    
                discord_message = await self.server.send_to_console(f'Unpacking the backup {zip}...')

                counter = [0,0]
                reports = {'error': False}
                
                unpack_bkp = self.server.client.error_wrapper(
                    error_title = f'{self.server.name}: unpack_bkp()',
                    reports = reports
                    )(self.server.unpack_bkp)

                task = threading.Thread(
                    target = unpack_bkp, 
                    args = (zip,),
                    kwargs = {'counter' : counter})
                task.start()
                
                while task.is_alive():
                    if counter[1] == 0: 
                        await asyncio.sleep(0.1)
                    else:
                        show = '```md\n[md-bkps]: [{}/{}] files have been unpacked...\n```'\
                            .format(counter[0], counter[1])
                        await discord_message.edit(
                            content = show)
                        await asyncio.sleep(0.5)
                
                if reports['error']:
                    msg = '```md\n[md-bkps]: ✖ An error occurred while unpacking files.\n```'
                else:
                    msg = '```md\n[md-bkps]: ✔ The files have been successfully unpacked.\n```'

                await discord_message.edit(content = msg)

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
            file = os.path.join(self.server.path_bkps, zip)
            
            with zipfile.ZipFile(file, 'r') as zipf:
                log_filename = 'backup_log.txt'

                if log_filename in zipf.namelist():
                    with zipf.open(log_filename) as log_file:
                        log_content = log_file.read().decode('utf-8')
                        
                        lines = log_content.splitlines()
                        for line in lines:
                            if line.startswith('Backup created on:'):
                                date_str = line.replace('Backup created on:', '').strip()
                                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                                break
                else:
                    date = "Date not found in log"

            dummy = [
            hover_and_suggest('[>] ' , color = 'green', suggest = f'!!load-bkp {zip.removesuffix(".zip")}', hover = 'Load backup'),
            hover_and_suggest('[x] ' , color = 'red', suggest = f'!!del-bkp {zip.removesuffix(".zip")}', hover = 'Del backup'),
            f'{{"text":"{zip} [{date}]"}}'
            ]

            self.server.execute(f'tellraw {player} {extras(dummy)}')