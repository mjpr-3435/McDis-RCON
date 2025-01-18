import os 
import asyncio

from datetime import datetime

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import hover_and_run, extras, read_file, write_in_file, thread, hover_and_suggest

class mdplugin():
    def __init__(self, server: Server):
        self.server                     = server
        self.log_thread                 = None
        self.foundation_date            = '2021-05-12'
        self.channel                    = self.server.client.get_channel(914533677411754024)
        self.players_text_path          = os.path.join(self.server.path_plugins, 'logger', 'players_log.txt')
        self.bots_text_path             = os.path.join(self.server.path_plugins, 'logger', 'bots_log.txt')

        os.makedirs(os.path.join(self.server.path_plugins, 'logger'), exist_ok = True)
        if not os.path.exists(self.players_text_path): write_in_file(self.players_text_path, '')
        if not os.path.exists(self.bots_text_path): write_in_file(self.bots_text_path, '')
        
        asyncio.create_task(self.aux_load())

    async def aux_load (self):
        self.log_thread = await thread('Ae Logs', self.channel, public = True)

    async def on_player_join(self, player: str):
        self.show_motd(player)

        if not self.log_thread: 
            return
        elif player in self.server.online_players:
            self.add_player_log(player)
        elif player in self.server.bots:
            self.add_bot_log(player)

    async def on_player_command(self, player: str, message: str):
                
        if self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'join-motd', 'Muestra el banner de entrada.')
            
        elif self.server.is_command(message, 'join-motd'):
            self.show_motd(player)

        if not self.log_thread: 
            return
        
        elif self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, "logger help", "Muestra los comandos del logger")

        elif self.server.is_command(message, 'logger help'):
            self.server.show_command(player, "logs", "Muestra los últimos registros del servidor.")
            self.server.show_command(player, "add log", "Añade un registro.")
            
        elif self.server.is_command(message, 'logs'):
            await self.show_logs(player)

        elif self.server.is_command(message, 'add log'):
            new_log = message.replace(f'{self.server.prefix}add log','').strip()
            new_log = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {player}: {new_log}'
            if new_log != '':
                await self.log_thread.send(new_log)
                self.server.send_response(player, '✔ Registro añadido.')
            
                await self.show_logs(player)
            else:
                self.server.send_response(player, '✖ No enviaste nada para registrar.')

    def show_motd(self, player: str):
        join_messages = self.join_message()

        for message in join_messages:
            message = message.replace('\n','')
            self.server.execute(f'tellraw {player} {message}')

    def join_message(self):
        years = int(((datetime.today()-datetime.strptime(self.foundation_date, "%Y-%m-%d")).days)//365.25)
        days = int((datetime.today()-datetime.strptime(self.foundation_date, "%Y-%m-%d")).days%365.25)
                
        if years == 0:
            active_days = f'Tiempo activo: {days} días'
        elif days == 0:
            active_days = f'Tiempo activo: {years} años'
        else:
            active_days = f'Tiempo activo: {years} años {days} días'
        
        join_messages = [   '{"text" : "§f§lAeternum §9§lNetwork §f"}',

                            '{"text" : "--------------------------"}',

                            extras([hover_and_run('§l[SMP] ', color = 'white', command = '/server SMP', hover = '/server SMP'),
                                    hover_and_run('§l[CMP] ', color = 'white', command = '/server CMP', hover = '/server CMP'),
                                    hover_and_run('§l[MMP] ', color = 'white', command = '/server MMP', hover = '/server MMP')], 
                                    text= 'Servers: ', color = 'white'),

                            f'{{"text" : "{active_days}"}}',

                            '{"text" : "--------------------------"}',

                            f'{{"text" : "MCDIS: !!mdhelp       MCDR: !!help", "color" : "gray"}}']
        return join_messages
    
    def         add_player_log          (self, player : str):
        players = read_file(self.players_text_path).strip().split('\n')
        bots = read_file(self.bots_text_path).strip().split('\n')
        
        if player in bots:
            bots.remove(player)
            write_in_file(self.bots_text_path, bots)

        if player in players: return
        
        write_in_file(self.players_text_path, '\n'.join(players + [player]))
    
    def         add_bot_log             (self, bot : str):
        players = read_file(self.players_text_path).strip().split('\n')
        bots = read_file(self.bots_text_path).strip().split('\n')
        
        if bot in players:
            players.remove(bot)
            write_in_file(self.players_text_path, players)

        if bot in bots: return

        write_in_file(self.bots_text_path, '\n'.join(bots + [bot]))
    
    async def   show_logs               (self, player : str):
        logs = [log async for log in self.log_thread.history(limit = None, oldest_first = True)]
        if not logs[1:]:
            self.server.send_response(player, 'No hay registros para mostrar.')
            return

        self.server.send_response(player, 'Ae logs (Últimos 5):')
        
        for i in range(1, min(len(logs[1:]), 5) + 1):
            self.server.send_response(player, f'• {logs[i].content.capitalize()}')

    
    
