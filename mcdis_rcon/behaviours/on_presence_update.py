from ..modules import *
from ..classes import McDisClient

class on_presence_update(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        await self.client.call_mdextras('on_presence_update', (before, after))

async def setup(client: McDisClient):
    await client.add_cog(on_presence_update(client))