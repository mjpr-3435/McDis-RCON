import discord

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client

        self.config = { 'Thumbnail'     : '',
                        'Embed Colour'  : 0x2f3136,
                        'ChannelID'     : 0}

    async def on_message(self, message: discord.Message):
        description = ''
        
        if message.channel.id != self.config['ChannelID']:
            return
        
        elif self.client.is_command(message.content, 'online'):
            for server in self.client.servers:
                description += f'`[{server.name}]`: '
                description += ', '.join(server.online_players) if hasattr(server, 'online_players') else ''
                description += '\n\n'

            await message.channel.send(embed = self.list_embed('Usuarios conectados:', description))
        
        elif self.client.is_command(message.content, 'bots'):
            for server in self.client.servers:
                description += f'`[{server.name}]`: '
                description += ', '.join(server.bots) if hasattr(server, 'bots') else ''
                description += '\n\n'
        
            await message.channel.send(embed = self.list_embed('Bots:', description))

    def list_embed(self, title: str, description: str):
        embed = discord.Embed(
                title = title,
                colour = self.config['Embed Colour'],
                description = description)
        
        embed.set_thumbnail(url = self.config['Thumbnail'])
        
        return embed