from ..modules import *
from ..classes import McDisClient

class on_raw_bulk_message_delete(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

    @commands.Cog.listener()
    
    async def on_raw_bulk_message_delete(self, payload: discord.RawBulkMessageDeleteEvent):
        await self.client.call_addons('on_raw_bulk_message_delete', (payload,))

async def setup(client: McDisClient):
    await client.add_cog(on_raw_bulk_message_delete(client))