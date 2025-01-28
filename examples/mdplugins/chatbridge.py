import discord
import asyncio
import os

from mcdis_rcon.classes import Server
from mcdis_rcon.utils import json_to_dict, dict_to_json

class mdplugin():
    def __init__(self, server: Server):
        self.server                     = server
        self.webhook : discord.Webhook  = None
        self.config                     = {'Webhook URL' : ''}

        asyncio.create_task(self.load())

    async def load(self):
        try:
            self.webhook = await discord.Webhook.from_url(url = self.config['Webhook URL'], client = self.server.client).fetch()
        except:
            self.server.add_log('Error en la configuración del Chatbridge. No se ha encontrado el webhook.')

    async def on_discord_message    (self, message: discord.Message):
        if self.webhook == None: return

        elif message.author.bot : return

        elif message.channel.id == self.webhook.channel.id:
            if not hasattr(self.server, 'online_players') or not hasattr(self.server, 'bots'): return
            elif not (self.server.online_players + self.server.bots): return

            msg = message.content.replace('\n', ' ').replace('"',"'")
            self.server.send_response('@a', f'[DIS] <{message.author.display_name}> {msg}')

    async def on_player_message     (self, player: str, message: str):

        if self.webhook == None: return
    
        self.send_to_servers(f'[{self.server.name}] <{player}> {message}')
            
        await self.webhook.send(f'{message}', username = f'[{self.server.name}] {player}', avatar_url = f'https://mc-heads.net/head/{player.lower()}.png')

    async def on_player_join        (self, player: str):
        if self.webhook == None: return

        self.send_to_servers(f'[{self.server.name}] {player} ha entrado al servidor')
            
        await self.webhook.send(f'[{self.server.name}] {player} ha entrado al servidor')
            
    async def on_player_left        (self, player: str):
        if self.webhook == None: return

        self.send_to_servers(f'[{self.server.name}] {player} ha salido del servidor')
            
        await self.webhook.send(f'[{self.server.name}] {player} ha salido del servidor')

    async def on_already_started    (self):
        if self.webhook == None: return

        self.send_to_servers(f'[{self.server.name}] Servidor abierto!')
            
        await self.webhook.send(f'[{self.server.name}] Servidor abierto!')

    async def on_stopped            (self):
        if self.webhook == None: return

        self.send_to_servers(f'[{self.server.name}] Servidor detenido')
            
        await self.webhook.send(f'[{self.server.name}] Servidor detenido')

    async def on_crash              (self):
        if self.webhook == None: return

        self.send_to_servers(f'[{self.server.name}] El servidor crasheó')
            
        await self.webhook.send(f'[{self.server.name}] El servidor crasheó')

    def send_to_servers(self, msg: str):
        msg = msg.replace("\n","").replace('"',"'")

        for server in self.server.client.servers:
            if not hasattr(server, 'online_players') or not hasattr(server, 'bots'):
                continue
            
            if server.name != self.server.name and (server.online_players + server.bots):
                server.send_response('@a', msg)  