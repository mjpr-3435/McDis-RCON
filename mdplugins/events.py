import re
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import dict_to_json, json_to_dict

class mdplugin():
    def __init__    (self, server: Server):
        self.server = server
        
        dict = {"omit crash report relay" : False,
                "Admins"                  : []}

        path_file = os.path.join(self.server.path_plugins_configs,'events.json')
        if not os.path.exists(path_file): dict_to_json(path_file, dict)
        self.config = json_to_dict(path_file)

        self.server.admins = self.config['Admins']
        if not hasattr(server, 'bots'): self.server.bots = []
        if not hasattr(server, 'online_players'): self.server.online_players = []

    async def listener_events           (self, log : str):
        if 'INFO]: ' in log:
            if any([f'<{player}>' in log for player in self.server.online_players]):
                player = log[log.index('<') + 1:log.index('>')]
                message = log[log.index('>') + 1:].strip()

                await self.server.call_plugins('on_player_message', (player, message))
                
                if not message.startswith(f'{self.server.prefix}'): return
                
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
                player = match.group(1).strip().split(' ')[-1]
                
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
                await self.server.call_plugins('on_stopped')
            
            elif log.endswith('ThreadedAnvilChunkStorage: All dimensions are saved'):
                self.server.bots = []
                self.server.online_players = []
                await self.server.call_plugins('on_already_stopped')

        elif 'ERROR]: ' in log:
            if  log.endswith('Considering it to be crashed, server will forcibly shutdown.'): 
                if self.config['omit crash report relay']:
                    self.server.stop_relaying(self.server.log_format('Crash detected. Finalizing relay...'))
                
                await self.server.call_plugins('on_crash')   