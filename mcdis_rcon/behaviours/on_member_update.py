from ..modules import *
from ..classes import McDisClient

class on_member_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        await self.client.call_addons('on_member_update', (self.client, before, after))

async def setup(client: commands.Bot):
    await client.add_cog(on_member_update(client))