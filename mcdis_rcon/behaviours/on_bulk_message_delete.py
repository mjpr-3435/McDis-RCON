from ..modules import *
from ..classes import McDisClient

class on_bulk_message_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_bulk_message_delete(self, messages : list[discord.Message]):
        await self.client.call_addons('on_bulk_message_delete', (messages,))

async def setup(client: McDisClient):
    await client.add_cog(on_bulk_message_delete(client))