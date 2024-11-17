import re
import os
import json

from mcdis_rcon.bot.classes import Server

config = dict()

async def load(self: Server):
    global config
    
    path_file = os.path.join(self.path_plugins_config,'events.json')
    dictionary = {"omit crash report relay" : False}
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    if not hasattr(self, 'bots'): self.bots = []
    if not hasattr(self, 'online_players'): self.online_players = []

async def listener_events(self: Server, log : str):
    global config

    if 'INFO]' in log:
        if any([f'<{player}>' in log for player in self.online_players]):
            player = log[log.index('<') + 1:log.index('>')]
            message = log[log.index('>') + 1:].strip()

            await self.call_plugins('on_player_message', (self, player, message))
            
            if not message.startswith(f'{self.prefix}'): return
            
            await self.call_plugins('on_player_command', (self, player, message))

        elif 'logged in with entity id' in log:
            match = re.search(r"(.*?) logged in with entity id", log)
            player_and_ip = match.group(1).strip().split(' ')[-1]
            player = player_and_ip.split('[')[0]
            local = player_and_ip.removeprefix(player) == '[local]'
            
            if local:
                self.bots.append(player)
            else:
                self.online_players.append(player)

            await self.call_plugins('on_player_join', (self, player))

        elif log.endswith('left the game'):
            match = re.search(r"(.*?) left the game", log)
            player = match.group(1).strip().split(' ')[-1]
            
            if player in self.bots: self.bots.remove(player)
            elif player in self.online_players: self.online_players.remove(player)

            await self.call_plugins('on_player_left', (self, player))

        elif 'Starting minecraft server' in log:
            self.bots = []
            self.online_players = []
            await self.call_plugins('on_started', (self,))

        elif log.endswith('For help, type "help"'):
            self.already_started = True
            await self.call_plugins('on_already_started', (self,))
            
        elif log.endswith('Stopping server'):
            await self.call_plugins('on_stopped', (self,))
        
        elif log.endswith('ThreadedAnvilChunkStorage: All dimensions are saved'):
            await self.call_plugins('on_already_stopped', (self,))

    elif 'ERROR]: ' in log:
        if  log.endswith('Considering it to be crashed, server will forcibly shutdown.'): 
            if config['omit crash report relay']:
                self.stop_relaying(self.log_format('Crash detected. Finalizing relay...'))
            
            await self.call_plugins('on_crash', (self,))