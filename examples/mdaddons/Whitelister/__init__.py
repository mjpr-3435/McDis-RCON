import discord
import os

from mcdis_rcon.classes import McDisClient, Server
from mcdis_rcon.utils import isAdmin

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client

        self.config = { 'ChannelID': 0,
                        'MainServer': ''}

    async def on_message(self, message: discord.Message):
        if  message.channel.id == self.config['ChannelID']      and\
            isAdmin(message.author)                             and\
            self.client.is_command(message.content, 'add user'):
            
            player = message.content.removeprefix(f'{self.client.prefix}add user').strip()
            server : Server = next(filter(lambda x: x.name == self.config['MainServer'], self.client.servers), None)

            if not player or not server or not server.is_running() or player.count(' '): 
                await message.add_reaction('❌')
                return

            server.execute(f'whitelist add {player}')
            await message.add_reaction('✅')