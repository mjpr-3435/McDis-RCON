from ..modules import *
from ..classes import McDisClient

class on_guild_emojis_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji]):
        await self.client.call_addons('on_guild_emojis_update', (self.client, guild, before, after))

async def setup(client: McDisClient):
    await client.add_cog(on_guild_emojis_update(client))