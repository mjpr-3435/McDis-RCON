from ..modules import *
from ..classes import McDisClient

class on_raw_integration_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_integration_delete(self, payload: discord.RawIntegrationDeleteEvent):
        await self.client.call_addons('on_raw_integration_delete', (self.client, payload))

async def setup(client: McDisClient):
    await client.add_cog(on_raw_integration_delete(client))