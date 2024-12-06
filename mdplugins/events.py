import re
import os
import json

from mcdis_rcon.classes import Server

config = dict()

async def load(server: Server):
    global config
    
    path_file = os.path.join(server.path_plugins_configs,'events.json')
    dictionary = {"omit crash report relay" : False}
    
    if not os.path.exists(path_file):
        os.makedirs(server.path_plugins_configs, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    if not hasattr(server, 'bots'): server.bots = []
    if not hasattr(server, 'online_players'): server.online_players = []

async def listener_events(server: Server, log : str):
    global config

    if 'INFO]: ' in log:
        if any([f'<{player}>' in log for player in server.online_players]):
            player = log[log.index('<') + 1:log.index('>')]
            message = log[log.index('>') + 1:].strip()

            await server.call_plugins('on_player_message', (server, player, message))
            
            if not message.startswith(f'{server.prefix}'): return
            
            await server.call_plugins('on_player_command', (server, player, message))

        elif 'logged in with entity id' in log:
            match = re.search(r"(.*?) logged in with entity id", log)
            player_and_ip = match.group(1).strip().split(' ')[-1]
            player = player_and_ip.split('[')[0]
            local = player_and_ip.removeprefix(player) == '[local]'
            
            if local:
                server.bots.append(player)
            else:
                server.online_players.append(player)

            await server.call_plugins('on_player_join', (server, player))

        elif log.endswith('left the game'):
            match = re.search(r"(.*?) left the game", log)
            player = match.group(1).strip().split(' ')[-1]
            
            if player in server.bots: server.bots.remove(player)
            elif player in server.online_players: server.online_players.remove(player)

            await server.call_plugins('on_player_left', (server, player))

        elif 'Starting minecraft server' in log:
            server.bots = []
            server.online_players = []
            await server.call_plugins('on_started', (server,))

        elif log.endswith('For help, type "help"'):
            await server.call_plugins('on_already_started', (server,))
            
        elif log.endswith('Stopping server'):
            await server.call_plugins('on_stopped', (server,))
        
        elif log.endswith('ThreadedAnvilChunkStorage: All dimensions are saved'):
            await server.call_plugins('on_already_stopped', (server,))

    elif 'ERROR]: ' in log:
        if  log.endswith('Considering it to be crashed, server will forcibly shutdown.'): 
            if config['omit crash report relay']:
                server.stop_relaying(server.log_format('Crash detected. Finalizing relay...'))
            
            await server.call_plugins('on_crash', (server,))