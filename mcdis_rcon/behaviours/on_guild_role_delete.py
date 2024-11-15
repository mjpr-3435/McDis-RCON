from ..modules import *
from ..classes import McDisClient

class on_guild_role_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_guild_role_delete(self, role: discord.Role):
        await self.client.call_addons('on_guild_role_delete', (self.client, role))

async def setup(client: commands.Bot):
    await client.add_cog(on_guild_role_delete(client))