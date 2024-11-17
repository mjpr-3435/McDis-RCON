from ..modules import *
from ..classes import McDisClient

class on_guild_unavailable(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_unavailable(self, guild: discord.Guild):
        await self.client.call_addons('on_guild_unavailable', (self.client, guild))

async def setup(client: McDisClient):
    await client.add_cog(on_guild_unavailable(client))