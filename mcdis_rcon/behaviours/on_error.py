from ..modules import *
from ..classes import McDisClient

class on_error(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_error(self, event, *args, **kwargs):
        await self.client.call_mdextras('on_error', (event, args, kwargs))

async def setup(client: McDisClient):
    await client.add_cog(on_error(client))