from ..modules import *
from ..classes import McDisClient

class on_message(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_message(self, message: discord.Message):
        await self.client.panel_interface(message)
        await self.client.call_addons('on_message', (self.client, message))
    
async def setup(client: McDisClient):
    await client.add_cog(on_message(client))
