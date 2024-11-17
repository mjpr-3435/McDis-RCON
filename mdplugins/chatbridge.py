import discord
import json
import os

from mcdis_rcon.bot.classes import Server

send_to = lambda server, x: server.send_response('@a', x)
webhook = None

async def load(self: Server):
    global webhook
    
    path_file = os.path.join(self.path_plugins_config,'chatbridge.json')
    dictionary = {'Webhook URL' : ''}
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    webhook_url = config['Webhook URL']

    try:
        webhook = await discord.Webhook.from_url(url = webhook_url, client = self.client).fetch()
    except:
        self.add_log('Error en la configuración del Chatbridge. No se ha encontrado el webhook.')

async def on_discord_message(self: Server, message: discord.Message):
    global webhook

    if webhook == None: return

    elif message.author.bot : return

    elif message.channel.id == webhook.channel.id:

        msg = message.content.replace('\n', ' ')

        send_to(self, f'[DIS] <{message.author.display_name}> {msg}')

async def on_player_message(self: Server, player: str, message: str):
    global webhook

    if webhook == None: return

    for server in self.servers: 
        if server.name != self.name: 
            send_to(server, f'[{self.name}] <{player}> {message}')
        
    await webhook.send(f'{message}', username = f'[{self.name}] {player}', avatar_url = f'https://mc-heads.net/head/{player.lower()}.png')

async def on_player_join(self: Server, player: str):
    global webhook

    if webhook == None: return

    for server in self.servers:
        if server.name != self.name:
            send_to(server, f'[{self.name}] {player} ha entrado al servidor')
        
    await webhook.send(f'[{self.name}] {player} ha entrado al servidor')
        
async def on_player_left(self: Server, player: str):
    global webhook

    if webhook == None: return

    for server in self.servers:
        if server.name != self.name:
            send_to(server, f'[{self.name}] {player} ha salido del servidor')
        
    await webhook.send(f'[{self.name}] {player} ha salido del servidor')

async def on_already_started(self: Server):
    global webhook

    if webhook == None: return

    for server in self.servers:
        if server.name != self.name:
            send_to(server, f'[{self.name}] Servidor abierto!')
        
    await webhook.send(f'[{self.name}] Servidor abierto!')

async def on_stopped(self: Server):
    global webhook

    if webhook == None: return

    for server in self.servers:
        if server.name != self.name:
            send_to(server, f'[{self.name}] Servidor detenido')
        
    await webhook.send(f'[{self.name}] Servidor detenido')

async def on_crash(self: Server):
    global webhook

    if webhook == None: return

    for server in self.servers:
        if server.name != self.name:
            send_to(server, f'[{self.name}] El servidor crasheó')
        
    await webhook.send(f'[{self.name}] El servidor crasheó')