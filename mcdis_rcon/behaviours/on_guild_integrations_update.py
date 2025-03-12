from ..modules import *
from ..classes import McDisClient

class on_guild_integrations_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_integrations_update(self, guild: discord.Guild):
        await self.client.call_mdextras('on_guild_integrations_update', (guild,))

async def setup(client: McDisClient):
    await client.add_cog(on_guild_integrations_update(client))