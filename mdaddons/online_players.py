import discord
import json
import os

from mcdis_rcon.bot.classes import Server
from mcdis_rcon.utils import hover, extras

link_thumbnail = ''
embed_colour = 0x2f3136 
channel_id = 0

async def load(self: Server):
    global link_thumbnail, channel_id
    
    path_file = os.path.join(self.path_plugins_config, 'online_players.json')
    dictionary = {
        'Thumbnail'   : '',
        'Channel ID' : 0
        }
    
    if not os.path.exists(path_file):
        os.makedirs(self.path_plugins_config, exist_ok = True)
        with open(path_file, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, ensure_ascii = False, indent = 4)
    
    with open(path_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    link_thumbnail = config['Thumbnail']
    channel_id = config['Channel ID']

    if not isinstance(self.client.get_channel(channel_id), discord.TextChannel):
        self.add_log('Plugin Online Players. El canal debe ser un canal de texto.')
        channel_id = 0

async def on_message(self: Server, message: discord.Message):
    global embed_colour, link_thumbnail, channel_id

    if message.author.bot : return
    if not message.channel.id == channel_id: return
    elif message.content.lower() == f'{self.prefix}online':
        embed = discord.Embed(
            title = 'Usuarios conectados:',
            colour = embed_colour 
            )
        
        online_players = ''
        for server in self.servers:
            online_players += f'`[{server.name}]`: '
            online_players += ', '.join(server.online_players)
            online_players += '\n\n'
        
        embed.description = online_players
        embed.set_thumbnail(url=link_thumbnail)
        
        await message.channel.send(embed=embed)
    
    elif message.content.lower() == f'{self.prefix}bots':
        embed = discord.Embed(
            title = 'Bots conectados:',
            colour = embed_colour 
            )
        
        bots = ''
        for server in self.servers:
            bots += f'`[{server.name}]`: '
            bots += ', '.join(server.bots)
            bots += '\n\n'
        
        embed.description = bots
        embed.set_thumbnail(url=link_thumbnail)
        
        await message.channel.send(embed=embed)