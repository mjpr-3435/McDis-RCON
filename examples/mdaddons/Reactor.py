import discord

from mcdis_rcon.classes import McDisClient

class mdaddon():
    def __init__(self, client: McDisClient):
        self.client = client

    async def on_message(self, message: discord.Message):
        if message.author.bot: False

        elif message.channel.id == self.client.panel.id:
            await message.add_reaction('✅')