import discord
import json
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import json_to_dict, dict_to_json
    
webhook = None

async def load(server: Server):
    global webhook
    
    path_file = os.path.join(server.path_plugins_configs,'chatbridge.json')
    dict = {'Webhook URL' : ''}
    
    if not os.path.exists(path_file):
        dict_to_json(path_file, dict)
        
    config = json_to_dict(path_file)

    webhook_url = config['Webhook URL']

    try:
        webhook = await discord.Webhook.from_url(url = webhook_url, client = server.client).fetch()
    except:
        server.add_log('Error en la configuración del Chatbridge. No se ha encontrado el webhook.')

async def on_discord_message(server: Server, message: discord.Message):
    global webhook

    if webhook == None: return

    elif message.author.bot : return

    elif message.channel.id == webhook.channel.id:
        msg = message.content.replace('\n', ' ').replace('"',"'")
        server.send_response('@a', f'[DIS] <{message.author.display_name}> {msg}')

async def on_player_message(server: Server, player: str, message: str):
    global webhook

    if webhook == None: return
  
    send_to_servers(server, f'[{server.name}] <{player}> {message}')
        
    await webhook.send(f'{message}', username = f'[{server.name}] {player}', avatar_url = f'https://mc-heads.net/head/{player.lower()}.png')

async def on_player_join(server: Server, player: str):
    global webhook

    if webhook == None: return

    send_to_servers(server, f'[{server.name}] {player} ha entrado al servidor')
        
    await webhook.send(f'[{server.name}] {player} ha entrado al servidor')
        
async def on_player_left(server: Server, player: str):
    global webhook

    if webhook == None: return

    send_to_servers(server, f'[{server.name}] {player} ha salido del servidor')
        
    await webhook.send(f'[{server.name}] {player} ha salido del servidor')

async def on_already_started(server: Server):
    global webhook

    if webhook == None: return

    send_to_servers(server, f'[{server.name}] Servidor abierto!')
        
    await webhook.send(f'[{server.name}] Servidor abierto!')

async def on_stopped(server: Server):
    global webhook

    if webhook == None: return

    send_to_servers(server, f'[{server.name}] Servidor detenido')
        
    await webhook.send(f'[{server.name}] Servidor detenido')

async def on_crash(server: Server):
    global webhook

    if webhook == None: return

    send_to_servers(server, f'[{server.name}] El servidor crasheó')
        
    await webhook.send(f'[{server.name}] El servidor crasheó')

def send_to_servers(server: Server, msg: str):
    msg = msg.replace("\n","").replace('"',"'")

    for server in server.client.servers:
        if server.name != server.name and server.online_players:
            server.send_response('@a', msg)  