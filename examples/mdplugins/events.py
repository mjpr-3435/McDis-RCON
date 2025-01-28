import re
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import read_file, write_in_file

class mdplugin():
    def __init__    (self, server: Server):
        self.server                 = server
        self.players_text_path      = os.path.join(self.server.path_plugins, 'logger', 'players_log.txt')
        self.bots_text_path         = os.path.join(self.server.path_plugins, 'logger', 'bots_log.txt')
        self.config                 = { "omit crash report relay" : False,
                                        "Admins"                  : ['KassiuLo']}

        self.server.admins = self.config['Admins']
        if not hasattr(server, 'stop_signal_received'): self.server.stop_signal_received = False
        if not hasattr(server, 'bots'): self.server.bots = []
        if not hasattr(server, 'online_players'): self.server.online_players = []

        os.makedirs(os.path.join(self.server.path_plugins, 'logger'), exist_ok = True)
        if not os.path.exists(self.players_text_path): write_in_file(self.players_text_path, '')
        if not os.path.exists(self.bots_text_path): write_in_file(self.bots_text_path, '')

    async def   listener_events         (self, log : str):
        if 'INFO]: ' in log:
            if any([f'<{player}>' in log for player in self.server.online_players]):
                player = log[log.index('<') + 1:log.index('>')]
                message = log[log.index('>') + 1:].strip()

                await self.server.call_plugins('on_player_message', (player, message))
                
                if not message.startswith(self.server.prefix): return
                
                await self.server.call_plugins('on_player_command', (player, message))

            elif 'logged in with entity id' in log:
                match = re.search(r"(.*?) logged in with entity id", log)
                player_and_ip = match.group(1).strip().split(' ')[-1]
                player = player_and_ip.split('[')[0]
                local = player_and_ip.removeprefix(player) == '[local]'
                
                if local:
                    self.server.bots.append(player)
                else:
                    self.server.online_players.append(player)

                await self.server.call_plugins('on_player_join', (player,))
            
            elif log.endswith('left the game'):
                match = re.search(r"(.*?) left the game", log)
                formated_player = match.group(1).strip().split(' ')[-1]
                player = next(filter(lambda x: x in formated_player, self.server.bots + self.server.online_players), None)
                
                if player in self.server.bots: self.server.bots.remove(player)
                elif player in self.server.online_players: self.server.online_players.remove(player)

                await self.server.call_plugins('on_player_left', (player,))

            elif 'Starting minecraft server' in log:
                self.server.bots = []
                self.server.online_players = []
                await self.server.call_plugins('on_started')

            elif log.endswith('For help, type "help"'):
                await self.server.call_plugins('on_already_started')
                
            elif log.endswith('Stopping server'):
                self.server.stop_signal_received = True
                await self.server.call_plugins('on_stopped')
            
            elif log.endswith('ThreadedAnvilChunkStorage: All dimensions are saved') and self.server.stop_signal_received:
                self.server.bots = []
                self.server.online_players = []
                self.server.stop_signal_received = False
                await self.server.call_plugins('on_already_stopped')

        elif 'ERROR]: ' in log:
            if  log.endswith('Considering it to be crashed, server will forcibly shutdown.'): 
                if self.config['omit crash report relay']:
                    self.server.stop_relaying(self.server.log_format('Crash detected. Finalizing relay...'))
                
                await self.server.call_plugins('on_crash') 

    async def   on_player_join          (self, player: str):
        if player in self.server.online_players:
            self.add_player_log(player)
        elif player in self.server.bots:
            self.add_bot_log(player)
    
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