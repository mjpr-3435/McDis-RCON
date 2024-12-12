from ..modules import *
from ..classes import McDisClient

class on_message_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_message_delete(self, message: discord.Message):
        await self.client.call_addons('on_message_delete', (message,))

async def setup(client: McDisClient):
    await client.add_cog(on_message_delete(client))