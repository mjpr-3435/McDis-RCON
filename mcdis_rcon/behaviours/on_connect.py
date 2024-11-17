from ..modules import *
from ..classes import McDisClient

class on_connect(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_connect(self):
        await self.client.call_addons('on_connect', (self.client))

async def setup(client: McDisClient):
    await client.add_cog(on_connect(client))