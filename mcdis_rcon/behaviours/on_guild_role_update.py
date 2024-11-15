from ..modules import *
from ..classes import McDisClient

class on_guild_role_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        await self.client.call_addons('on_guild_role_update', (self.client, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_guild_role_update(client))