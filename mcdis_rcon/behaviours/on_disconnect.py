from ..modules import *
from ..classes import McDisClient

class on_disconnect(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_disconnect(self):
        await self.client.call_mdextras('on_disconnect')

async def setup(client: McDisClient):
    await client.add_cog(on_disconnect(client))